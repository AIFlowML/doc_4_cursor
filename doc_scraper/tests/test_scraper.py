import pytest
from pathlib import Path
from doc_scraper.scraper import DocsScraper, ScraperSettings

def test_scraper_settings():
    """Test scraper settings initialization."""
    settings = ScraperSettings(
        base_url="https://docs.example.com",
        save_dir=Path("test_docs"),
        output_file=Path("test_docs/output.md"),
        max_workers=3
    )
    assert str(settings.base_url) == "https://docs.example.com/"
    assert settings.save_dir == Path("test_docs")
    assert settings.output_file == Path("test_docs/output.md")
    assert settings.max_workers == 3
    assert settings.timeout == 10  # default value
    assert settings.retry_attempts == 3  # default value

def test_clean_content():
    """Test content cleaning functionality."""
    settings = ScraperSettings(
        base_url="https://docs.example.com",
        save_dir=Path("test_docs"),
        output_file=Path("test_docs/output.md")
    )
    scraper = DocsScraper(settings)
    
    content = """
    Table of Contents
    Some real content here
    On this page
    More content
    5 min read
    """
    
    cleaned = scraper.clean_content(content)
    assert "Table of Contents" not in cleaned
    assert "On this page" not in cleaned
    assert "5 min read" not in cleaned
    assert "Some real content here" in cleaned
    assert "More content" in cleaned 