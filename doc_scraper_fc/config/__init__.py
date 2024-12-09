"""
Configuration management for the documentation scraper.
"""
import os
import yaml
from pathlib import Path
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from rich import print

from pydantic import BaseModel, Field, ConfigDict

def find_env_file() -> Path:
    """Find the closest .env file starting from the current directory."""
    current_dir = Path(__file__).resolve().parent
    package_dir = current_dir.parent
    
    # First check in the package directory
    env_file = package_dir / '.env'
    if env_file.exists():
        print(f"[green]Found .env file in package directory: {env_file}[/green]")
        return env_file
    
    # If not found, look in parent directories
    root_dir = package_dir
    while root_dir.parent != root_dir:  # Stop at filesystem root
        env_file = root_dir / '.env'
        if env_file.exists():
            print(f"[yellow]Found .env file in parent directory: {env_file}[/yellow]")
            return env_file
        root_dir = root_dir.parent
    
    print("[red]No .env file found[/red]")
    return package_dir / '.env'

# Load environment variables from the closest .env file
env_file = find_env_file()
load_dotenv(env_file)

class ScrapingConfig(BaseModel):
    """Scraping configuration settings."""
    model_config = ConfigDict(protected_namespaces=())
    
    api_key: str = Field(default_factory=lambda: os.getenv("FIRECRAWL_API_KEY", ""))
    base_url: str = Field(default="", description="Base URL to scrape")
    max_depth: int = Field(3, description="Maximum crawling depth")
    max_pages: int = Field(10, description="Maximum number of pages to crawl")
    batch_size: int = Field(10, description="Number of URLs to process in parallel")
    formats: List[str] = Field(default_factory=lambda: ["markdown"])
    javascript: bool = Field(True, description="Enable JavaScript rendering")
    timeout: int = Field(30000, description="Request timeout in milliseconds")
    mobile: bool = Field(False, description="Enable mobile device emulation")
    location: Dict[str, Any] = Field(
        default_factory=lambda: {
            "country": "US",
            "languages": ["en-US"]
        }
    )

class ExtractionConfig(BaseModel):
    """Content extraction configuration."""
    model_config = ConfigDict(protected_namespaces=())
    
    prompt: str = Field(
        default="Extract and structure the documentation content with clear sections, "
                "code examples, key concepts, and important notes."
    )
    extraction_schema: Dict[str, Any] = Field(default_factory=dict, alias="schema")
    clean_patterns: List[str] = Field(default_factory=list)
    selectors: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "title": ["h1", "title"],
            "content": ["article", ".markdown-body", "main .content"],
            "code_blocks": ["pre code", ".highlight"],
            "metadata": ["meta[name='description']", ".last-updated"]
        }
    )

class PatternsConfig(BaseModel):
    """URL pattern configuration."""
    model_config = ConfigDict(protected_namespaces=())
    
    include: List[str] = Field(default_factory=lambda: ["/docs/", "/guide/", "/api/"])
    exclude: List[str] = Field(default_factory=lambda: ["/blog/", "/changelog/"])

class OutputConfig(BaseModel):
    """Output configuration."""
    model_config = ConfigDict(protected_namespaces=())
    
    directory: Optional[str] = None
    template: str = Field(
        default=(
            "# {title}\n\n"
            "{description}\n\n"
            "{content}\n\n"
            "## Code Examples\n"
            "{code_blocks}\n\n"
            "---\n"
            "Source: {url}"
        )
    )

class Config(BaseModel):
    """Main configuration."""
    model_config = ConfigDict(protected_namespaces=())
    
    scraping: ScrapingConfig = Field(default_factory=ScrapingConfig)
    extraction: ExtractionConfig = Field(default_factory=ExtractionConfig)
    patterns: PatternsConfig = Field(default_factory=PatternsConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)

def load_config() -> Config:
    """Load configuration with API key from .env file."""
    # Load default config from YAML
    config_path = Path(__file__).resolve().parent / "default_config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
            return Config(**config_data)
    
    return Config() 