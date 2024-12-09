import os
import re
import time
import logging
import logging.handlers
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from typing import Set, List, Dict, Optional
from urllib.parse import urljoin, urlparse

import requests
import yaml
import typer
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pydantic_settings import BaseSettings
from pydantic import HttpUrl, Field
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Configure logging with both file and console handlers."""
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "scraper.log"

    # Create formatters and handlers
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler with rotation (1MB per file, keep 2 backup files)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024*1024, backupCount=2
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger

logger = setup_logging()
console = Console()

class ScraperSettings(BaseSettings):
    """Settings for the documentation scraper."""
    base_url: HttpUrl = Field(..., description="Base URL to scrape")
    save_dir: Path = Field(default=Path("scraped_docs"), description="Directory to save scraped docs")
    output_file: Path = Field(default=None, description="Output file path")
    max_workers: int = Field(default=5, description="Maximum number of concurrent workers")
    timeout: int = Field(default=10, description="Request timeout in seconds")
    retry_attempts: int = Field(default=3, description="Number of retry attempts")
    delay_between_requests: float = Field(default=1.0, description="Delay between requests in seconds")

class DocsScraper:
    """Documentation scraper with concurrent processing and progress tracking."""
    
    def __init__(self, settings: ScraperSettings):
        self.settings = settings
        self.visited_links = set()
        self.session = requests.Session()
        self.content_lock = threading.Lock()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn()
        )

    def fetch_page(self, url):
        """Fetch a page with retry logic."""
        for attempt in range(self.settings.retry_attempts):
            try:
                response = self.session.get(url, timeout=self.settings.timeout)
                response.raise_for_status()
                return response.text
            except Exception as e:
                if attempt == self.settings.retry_attempts - 1:
                    logger.error(f"Failed to fetch {url}: {e}")
                    raise
                time.sleep(self.settings.delay_between_requests)

    def process_page(self, url: str) -> Set[str]:
        """Process a single page and extract links."""
        try:
            html = self.fetch_page(url)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract content using selectors
            content = ""
            for selector in ["article", ".markdown-body", "#content-wrapper", ".docs-content"]:
                element = soup.select_one(selector)
                if element:
                    content = str(element)
                    break
            
            if not content:
                logger.warning(f"No content found for {url}")
                return set()

            # Convert to markdown
            markdown = md(content)
            
            # Clean content
            markdown = self.clean_content(markdown)
            
            # Save content
            with self.content_lock:
                self.save_content(url, markdown)
            
            # Extract links
            return self.extract_links(soup)
            
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            return set()

    def clean_content(self, content: str) -> str:
        """Clean the content using patterns from config."""
        patterns = [
            r"Table of Contents",
            r"On this page",
            r"Share this page",
            r"Last modified",
            r"Edit this page",
            r"\d+\s*min read",
            r"Previous\s+Next"
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, "", content, flags=re.IGNORECASE)
        
        return content.strip()

    def save_content(self, url: str, content: str):
        """Save the processed content."""
        try:
            with open(self.settings.output_file, "a", encoding="utf-8") as f:
                title = f"# {url.split('/')[-1].replace('-', ' ').title()}"
                f.write(f"\n\n{title}\n\n{content}\n")
            logger.info(f"Successfully appended: {title} (Content length: {len(content)} characters)")
        except Exception as e:
            logger.error(f"Error saving content for {url}: {e}")

    def extract_links(self, soup: BeautifulSoup) -> Set[str]:
        """Extract valid links from the page."""
        links = set()
        base_url = str(self.settings.base_url)
        
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.startswith(("http", "https")):
                href = urljoin(base_url, href)
            
            if href.startswith(base_url) and href not in self.visited_links:
                links.add(href)
        
        return links

    def scrape(self):
        """Main scraping function with concurrent processing."""
        to_visit = {str(self.settings.base_url)}
        self.visited_links = set()
        
        with self.progress:
            while to_visit:
                with ThreadPoolExecutor(max_workers=self.settings.max_workers) as executor:
                    future_to_url = {
                        executor.submit(self.process_page, url): url 
                        for url in list(to_visit)[:self.settings.max_workers]
                    }
                    
                    for future in as_completed(future_to_url):
                        url = future_to_url[future]
                        to_visit.remove(url)
                        self.visited_links.add(url)
                        
                        try:
                            new_links = future.result()
                            to_visit.update(new_links - self.visited_links)
                            logger.info(f"Processed: {len(self.visited_links)}, To visit: {len(to_visit)}")
                        except Exception as e:
                            logger.error(f"Error processing {url}: {e}")

def main(url: str, output_dir: Optional[str] = None):
    """CLI entry point."""
    settings_data = {}
    if output_dir:
        settings_data["save_dir"] = Path(output_dir)
    
    settings = ScraperSettings(
        base_url=url,
        **settings_data
    )
    
    # Ensure save directory exists
    settings.save_dir.mkdir(parents=True, exist_ok=True)
    
    # Set output file
    if not settings.output_file:
        domain = urlparse(url).netloc.split(".")[0]
        settings.output_file = settings.save_dir / f"{domain}_docs.md"
    
    with console.status("[bold green]Initializing scraper...") as status:
        scraper = DocsScraper(settings)
        status.update("[bold yellow]Scraping documentation...")
        scraper.scrape()
        status.update("[bold green]Scraping complete!")
        
    console.print(f"\nDocumentation saved at: {settings.output_file}")

if __name__ == "__main__":
    typer.run(main) 