# Doc Scraper

A powerful documentation scraping tool that helps you extract and process documentation from various websites.

## Features

- Configurable website scraping with custom selectors
- Clean and format documentation content
- Support for multiple documentation sites
- Progress tracking and logging
- Concurrent processing for faster scraping
- Customizable output formats

## Installation

```bash
pip install doc-scraper
```

## Quick Start

1. Clone the repository:
```bash
git clone git@github.com:AIFlowML/doc_4_cursor.git
cd doc_4_cursor
```

2. Create a configuration file (sites_config.yaml):

```yaml
default:
  base_url: "https://docs.example.com"
  save_dir: "./scraped_docs"
  max_workers: 5
  timeout: 10
  retry_attempts: 3
  delay_between_requests: 1.0

example_site:
  selectors:
    content: ["article", ".markdown-body"]
    title: ["h1", "title"]
    description: "meta[name='description']"
  include_patterns:
    - "/docs/"
    - "/guides/"
  exclude_patterns:
    - "/api/"
    - "/changelog/"
  clean_patterns:
    - "regex:\\^Table of Contents"
    - "regex:\\^On this page"
```

2. Run the scraper:

```bash
doc-scraper scrape https://docs.example.com
```

## Configuration

The scraper can be configured using a YAML file. See the example configuration above for the basic structure.

### Site Configuration

- `base_url`: The base URL of the documentation site
- `save_dir`: Directory to save scraped documentation
- `max_workers`: Number of concurrent workers for scraping
- `timeout`: Request timeout in seconds
- `retry_attempts`: Number of retry attempts for failed requests
- `delay_between_requests`: Delay between requests in seconds

### Selectors

- `content`: List of CSS selectors for main content
- `title`: List of CSS selectors for page title
- `description`: CSS selector for meta description

### Patterns

- `include_patterns`: List of URL patterns to include
- `exclude_patterns`: List of URL patterns to exclude
- `clean_patterns`: List of patterns to clean from content

## Testing

### Running Tests

The project uses pytest for testing. To run the tests:

1. Install test dependencies:
```bash
pip install pytest pytest-cov
```

2. Run tests with coverage:
```bash
pytest tests/ --cov=doc_scraper
```

### Testing the CLI

After installation, test the CLI commands:

1. Check version:
```bash
doc-scraper version
```

2. Test scraping:
```bash
doc-scraper scrape https://docs.example.com --output-dir ./test_output
```

### Logging

The scraper logs information to:
- Console (INFO level)
- `logs/scraper.log` file (DEBUG level)

Log files are rotated at 1MB with 2 backup files maintained.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository from [AIFlowML/doc_4_cursor](https://github.com/AIFlowML/doc_4_cursor)
2. Create your feature branch
3. Run tests to ensure everything works
4. Commit your changes
5. Push to the branch
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 