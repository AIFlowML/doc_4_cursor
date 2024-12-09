"""
Doc Scraper FC - A documentation scraper using Firecrawl
"""

__version__ = "0.1.0"

from .scraper import DocScraper
from config import Config, load_config

__all__ = ["DocScraper", "Config", "load_config"] 