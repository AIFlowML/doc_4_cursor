"""Test script for the documentation scraper."""
import asyncio
from pathlib import Path
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import yaml
from datetime import datetime
from rich import print

# Check .env file location
def find_env_file():
    """Find and print the location of the .env file being used."""
    current_dir = Path(__file__).resolve().parent
    env_file = current_dir / '.env'
    if env_file.exists():
        print(f"[green]Using .env file from: {env_file}[/green]")
        return env_file
    
    # Look in parent directories
    root_dir = current_dir
    while root_dir.parent != root_dir:
        env_file = root_dir / '.env'
        if env_file.exists():
            print(f"[yellow]Using .env file from parent directory: {env_file}[/yellow]")
            return env_file
        root_dir = root_dir.parent
    
    print("[red]No .env file found[/red]")
    return None

# Find and load .env file
env_file = find_env_file()
if env_file:
    load_dotenv(env_file)

def load_config(config_path="config/default_config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
        # Handle environment variables
        if '${FIRECRAWL_API_KEY}' in str(config):
            api_key = os.getenv('FIRECRAWL_API_KEY')
            if not api_key:
                raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
            config['scraping']['api_key'] = api_key
            
        return config

def create_markdown_section(title, url, content):
    """Create a markdown section with proper formatting."""
    return "\n".join([
        f"## {title}",
        f"Source: {url}",
        "",
        content,
        "",
        "---",
        ""
    ])

def create_markdown_file(title, url, content, timestamp=None):
    """Create a markdown file with metadata."""
    lines = [
        "---",
        f"title: {title}",
        f"source_url: {url}",
        f"date_scraped: {timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "---",
        "",
        content
    ]
    return "\n".join(lines)

async def test_scrape():
    """Test basic scraping functionality."""
    # Load configuration
    config = load_config()
    
    # Setup variables from config
    base_url = config['scraping']['base_url']
    output_dir = Path(config['output']['directory'])
    output_dir.mkdir(exist_ok=True)
    
    test_urls = [
        f"{base_url}/introduction",
        f"{base_url}/api-reference/introduction",
        f"{base_url}/sdks/python"
    ]
    
    # Initialize Firecrawl
    api_key = config['scraping']['api_key']
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY not found in environment variables")
    
    app = FirecrawlApp(api_key=api_key)
    
    # Prepare merged content if needed
    merged_content = []
    
    # Test single URL scraping
    print("\nTesting single URL scraping...")
    for url in test_urls:
        try:
            print(f"\nScraping {url}...")
            result = app.scrape_url(url, params={
                'formats': config['scraping']['formats'],
                **config['scraping']['options']
            })
            
            if result:
                title = result.get('metadata', {}).get('title', 'Untitled')
                content = result.get('markdown', '')
                
                # Add to merged content if enabled
                if config['output']['save_merged_file']:
                    section = create_markdown_section(title, url, content)
                    merged_content.append(section)
                    print(f"✓ Added content to merged file from {url}")
                
                # Save individual file if enabled
                if config['output']['save_individual_pages']:
                    filename = url.split('/')[-1] or 'index'
                    if config['output']['add_timestamps']:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{filename}_{timestamp}"
                    
                    output_file = output_dir / f"{filename}.md"
                    
                    # Create content with or without metadata
                    if config['output']['add_metadata']:
                        file_content = create_markdown_file(title, url, content)
                    else:
                        file_content = content
                    
                    output_file.write_text(file_content)
                    print(f"✓ Saved individual file to {output_file}")
        
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
    
    # Test site crawling
    print("\n\nTesting site crawling...")
    try:
        # Start crawl job
        print("Starting crawl job...")
        crawl_response = app.crawl_url(
            base_url,
            params={
                'limit': config['scraping']['max_pages'],
                'maxDepth': config['scraping']['max_depth'],
                'scrapeOptions': {
                    'formats': config['scraping']['formats'],
                    **config['scraping']['options']
                }
            }
        )
        
        if isinstance(crawl_response, dict):
            # Handle immediate response with data
            if 'data' in crawl_response:
                results = crawl_response['data']
                print(f"Processing {len(results)} crawled pages...")
                
                for result in results:
                    if not result:
                        continue
                    
                    # Extract content and metadata
                    content = result.get('markdown', '')
                    metadata = result.get('metadata', {})
                    source_url = metadata.get('sourceURL', '')
                    title = metadata.get('title', 'Untitled')
                    
                    if not source_url:
                        continue
                    
                    # Add to merged content if enabled
                    if config['output']['save_merged_file']:
                        section = create_markdown_section(title, source_url, content)
                        merged_content.append(section)
                        print(f"✓ Added content to merged file from {source_url}")
                    
                    # Save individual file if enabled
                    if config['output']['save_individual_pages']:
                        # Create filename from URL
                        filename = source_url.replace(base_url, '').strip('/').replace('/', '_') or 'index'
                        if config['output']['add_timestamps']:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"{filename}_{timestamp}"
                        
                        output_file = output_dir / f"crawl_{filename}.md"
                        
                        # Create content with or without metadata
                        if config['output']['add_metadata']:
                            file_content = create_markdown_file(title, source_url, content)
                        else:
                            file_content = content
                        
                        output_file.write_text(file_content)
                        print(f"✓ Saved individual file to {output_file}")
                
                print("\n✓ Crawling completed successfully")
            else:
                print("Error: No data in crawl response")
                print("Response:", crawl_response)
        else:
            print("Error: Invalid crawl response format")
            print("Response:", crawl_response)
        
        # Save merged content if enabled
        if config['output']['save_merged_file'] and merged_content:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            merged_filename = f"{config['output']['merged_file_prefix']}_{timestamp}.md"
            output_file = output_dir / merged_filename
            
            # Create final document
            header = "\n".join([
                "# Firecrawl Documentation",
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Base URL: {base_url}",
                "",
                "---",
                ""
            ])
            
            final_content = header + "\n".join(merged_content)
            
            # Save to file
            output_file.write_text(final_content)
            print(f"\n✓ Saved merged documentation to {output_file}")
        
    except Exception as e:
        print(f"Error during crawling: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_scrape()) 