import typer
from pathlib import Path
from typing import Optional
from rich.console import Console

from .scraper import main as scraper_main

app = typer.Typer(help="Documentation scraper CLI")
console = Console()

@app.command()
def scrape(
    url: str = typer.Argument(..., help="URL of the documentation site to scrape"),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir", "-o",
        help="Directory to save scraped documentation"
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to configuration file"
    )
):
    """
    Scrape documentation from a website.
    """
    try:
        scraper_main(url, str(output_dir) if output_dir else None)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def version():
    """Show the version of doc-scraper."""
    from . import __version__
    console.print(f"doc-scraper version: {__version__}")

if __name__ == "__main__":
    app() 