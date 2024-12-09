"""
Command-line interface for the enhanced documentation scraper.
"""
import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from scraper import main as scraper_main
from config import load_config
from logs import setup_logging

# Initialize logger and console
logger = setup_logging()
console = Console()

app = typer.Typer(
    help="Enhanced documentation scraper with LLM-optimized output using Firecrawl"
)

@app.command()
def scrape(
    url: str = typer.Argument(..., help="URL of the documentation site to scrape"),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir", "-o",
        help="Directory to save scraped documentation"
    ),
    config_file: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to custom configuration file"
    ),
    batch_size: Optional[int] = typer.Option(
        None,
        "--batch-size", "-b",
        help="Number of URLs to process in parallel"
    ),
    max_depth: Optional[int] = typer.Option(
        None,
        "--max-depth", "-d",
        help="Maximum depth for crawling"
    ),
    javascript: Optional[bool] = typer.Option(
        None,
        "--javascript/--no-javascript", "-j/-nj",
        help="Enable/disable JavaScript rendering"
    )
):
    """
    Scrape documentation from a website and format it for LLMs.
    """
    try:
        # Load configuration
        config = load_config(config_file) if config_file else load_config()
        
        # Override configuration with CLI options
        if batch_size is not None:
            config.scraping.batch_size = batch_size
        if max_depth is not None:
            config.scraping.max_depth = max_depth
        if javascript is not None:
            config.scraping.javascript = javascript
        
        # Run scraper
        asyncio.run(scraper_main(url, output_dir))
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def version():
    """Show the version of doc-scraper-fc."""
    from . import __version__
    console.print(f"doc-scraper-fc version: {__version__}")

if __name__ == "__main__":
    app() 