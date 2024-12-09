"""
Tests for the enhanced documentation scraper.
"""
import os
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

from scraper import DocScraper
from config import Config

@pytest.fixture
def mock_firecrawl_client():
    with patch("scraper.FirecrawlApp") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def config():
    return Config(
        scraping={
            "base_url": "https://docs.example.com",
            "api_key": "test-key",
            "formats": ["markdown"]
        },
        output={"directory": "test_output"}
    )

@pytest.mark.asyncio
async def test_crawl_site(mock_firecrawl_client, config):
    """Test crawling functionality."""
    # Setup
    mock_data = [
        {"markdown": "# Page 1", "metadata": {"title": "Page 1"}},
        {"markdown": "# Page 2", "metadata": {"title": "Page 2"}}
    ]
    mock_response = MagicMock()
    mock_response.data = mock_data
    mock_response.next = None
    mock_firecrawl_client.crawl_url.return_value = mock_response
    
    # Execute
    scraper = DocScraper(config)
    result = await scraper.crawl_site()
    
    # Assert
    assert result == mock_data
    mock_firecrawl_client.crawl_url.assert_called_once()

@pytest.mark.asyncio
async def test_scrape_url(mock_firecrawl_client, config):
    """Test single URL scraping."""
    # Setup
    mock_result = {
        "markdown": "# Test Content",
        "metadata": {"title": "Test Page", "description": "Test description"},
        "code_blocks": ["def test(): pass"]
    }
    mock_firecrawl_client.scrape_url.return_value = mock_result
    
    # Execute
    scraper = DocScraper(config)
    result = await scraper.scrape_url("https://docs.example.com/test")
    
    # Assert
    assert result == mock_result
    mock_firecrawl_client.scrape_url.assert_called_once()

@pytest.mark.asyncio
async def test_save_results(mock_firecrawl_client, config, tmp_path):
    """Test saving results to files."""
    # Setup
    config.output.directory = str(tmp_path)
    mock_result = {
        "markdown": "# Test Content",
        "metadata": {
            "title": "Test Page",
            "description": "Test description",
            "sourceURL": "https://docs.example.com/test"
        }
    }
    
    # Execute
    scraper = DocScraper(config)
    scraper.save_results(mock_result)
    
    # Assert
    saved_files = list(tmp_path.glob("*.md"))
    assert len(saved_files) == 1
    content = saved_files[0].read_text()
    assert "# Test Content" in content
    assert "Test Page" in content
    assert "https://docs.example.com/test" in content

@pytest.mark.asyncio
async def test_full_scrape_flow(mock_firecrawl_client, config, tmp_path):
    """Test the complete scraping flow."""
    # Setup
    config.output.directory = str(tmp_path)
    mock_data = [{
        "markdown": "# Test Content",
        "metadata": {
            "title": "Test Page",
            "description": "Test description",
            "sourceURL": "https://docs.example.com/test"
        }
    }]
    mock_response = MagicMock()
    mock_response.data = mock_data
    mock_response.next = None
    mock_firecrawl_client.crawl_url.return_value = mock_response
    
    # Execute
    scraper = DocScraper(config)
    results = await scraper.crawl_site()
    scraper.save_results(results)
    
    # Assert
    saved_files = list(tmp_path.glob("*.md"))
    assert len(saved_files) == 1
    content = saved_files[0].read_text()
    assert "# Test Content" in content
    assert "Test Page" in content
    assert "https://docs.example.com/test" in content