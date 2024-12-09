"""
Enhanced documentation scraper using Firecrawl.
"""
import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

from firecrawl import FirecrawlApp
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

from config import Config

# Load environment variables
load_dotenv()

class DocScraper:
    """Enhanced documentation scraper with Firecrawl integration."""
    
    def __init__(self, config: Config):
        """Initialize the scraper with configuration."""
        self.config = config
        self.api_key = config.scraping.api_key
        if not self.api_key:
            raise ValueError("API key not found in configuration")
        
        self.app = FirecrawlApp(api_key=self.api_key)
        self.output_dir = Path(config.output.directory or "scraped_docs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def scrape_url(self, url: str, formats: List[str] = None) -> Dict:
        """
        Scrape a single URL with specified formats.
        
        Args:
            url: The URL to scrape
            formats: List of formats to return (e.g., ['markdown', 'html'])
        """
        try:
            params = {
                'formats': formats or self.config.scraping.formats,
                'onlyMainContent': True,
                'removeBase64Images': True
            }
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description=f"Scraping {url}...", total=None)
                result = self.app.scrape_url(url, params=params)
            
            return result
        except Exception as e:
            print(f"[red]Error scraping {url}: {str(e)}[/red]")
            return None

    async def crawl_site(
        self, 
        url: Optional[str] = None,
        max_pages: Optional[int] = None,
        max_depth: Optional[int] = None,
        include_paths: Optional[List[str]] = None,
        exclude_paths: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Crawl a website and scrape its pages.
        
        Args:
            url: Base URL to crawl (defaults to config.scraping.base_url)
            max_pages: Maximum number of pages to crawl
            max_depth: Maximum depth to crawl
            include_paths: List of URL patterns to include
            exclude_paths: List of URL patterns to exclude
        """
        try:
            url = url or self.config.scraping.base_url
            params = {
                'limit': max_pages or self.config.scraping.max_pages,
                'maxDepth': max_depth or self.config.scraping.max_depth,
                'includePaths': include_paths or self.config.patterns.include,
                'excludePaths': exclude_paths or self.config.patterns.exclude,
                'scrapeOptions': {
                    'formats': self.config.scraping.formats,
                    'onlyMainContent': True,
                    'removeBase64Images': True
                }
            }
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description=f"Crawling {url}...", total=None)
                
                # Start crawl job
                crawl_job = self.app.crawl_url(url, params=params, poll_interval=10)
                
                # Get results
                results = []
                while True:
                    if not crawl_job.next:
                        results.extend(crawl_job.data)
                        break
                    results.extend(crawl_job.data)
                    crawl_job = self.app.get_crawl_status(crawl_job.next)
            
            return results
        except Exception as e:
            print(f"[red]Error crawling {url}: {str(e)}[/red]")
            return []

    def save_results(self, results: Union[Dict, List[Dict]], base_filename: str = "docs") -> None:
        """
        Save scraping results to files.
        
        Args:
            results: Scraping results to save
            base_filename: Base name for output files
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if isinstance(results, dict):
            results = [results]
        
        for i, result in enumerate(results):
            if not result:
                continue
                
            # Extract content
            markdown = result.get('markdown', '')
            metadata = result.get('metadata', {})
            source_url = metadata.get('sourceURL', f'page_{i}')
            
            # Create filename
            filename = f"{base_filename}_{timestamp}_{i}.md"
            filepath = self.output_dir / filename
            
            # Add metadata header
            content = f"""---
title: {metadata.get('title', 'Untitled')}
source_url: {source_url}
date_scraped: {timestamp}
---

{markdown}
"""
            
            # Save to file
            try:
                filepath.write_text(content)
                print(f"[green]Saved content to {filepath}[/green]")
            except Exception as e:
                print(f"[red]Error saving to {filepath}: {str(e)}[/red]")

async def main(url: str, output_dir: Optional[Path] = None, is_crawl: bool = False):
    """Main entry point for the scraper."""
    config = Config(
        scraping={"base_url": url},
        output={"directory": str(output_dir) if output_dir else None}
    )
    scraper = DocScraper(config)
    
    try:
        if is_crawl:
            results = await scraper.crawl_site()
        else:
            results = await scraper.scrape_url(url)
        
        if results:
            scraper.save_results(results)
            print("[green]Scraping completed successfully![/green]")
        else:
            print("[yellow]No results found.[/yellow]")
            
    except Exception as e:
        print(f"[red]Error during scraping: {str(e)}[/red]")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced documentation scraper")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--output", "-o", help="Output directory", type=Path)
    parser.add_argument("--crawl", "-c", help="Crawl the site instead of single page scrape", action="store_true")
    
    args = parser.parse_args()
    asyncio.run(main(args.url, args.output, args.crawl)) 