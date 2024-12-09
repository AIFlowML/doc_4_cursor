# Doc Scraper FC (Firecrawl)

A powerful documentation scraper built on top of Firecrawl, designed to efficiently extract and process documentation from websites. This tool specializes in creating clean, structured markdown content suitable for documentation systems, knowledge bases, and LLM training.

## Features

- **Powered by Firecrawl**: Utilizes Firecrawl's robust web scraping capabilities
- **Smart Content Extraction**: Automatically identifies and extracts main content while removing noise
- **Flexible Output**: Save as individual files, merged documentation, or both
- **Metadata Support**: Preserves metadata and structure from source documentation
- **Configurable**: Extensive YAML configuration for customizing behavior
- **Clean Markdown**: Generates clean, well-structured markdown suitable for various use cases

## Installation

```bash
# Clone the repository
git clone https://github.com/AIFlowML/doc_4_cursor.git
cd doc_4_cursor/doc_scraper_fc

# Create and activate conda environment
conda create -n doc-scraper python=3.10
conda activate doc-scraper

# Install package in development mode
pip install -e .
```

## Configuration

1. Create a `.env` file in the package directory:
```bash
cp .env_example .env
```

2. Add your Firecrawl API key to `.env`:
```bash
FIRECRAWL_API_KEY=your-api-key
```

3. (Optional) Customize the configuration in `config/default_config.yaml`

## Usage

### Command Line Interface

```bash
# Basic URL scraping
python run_scraper.py https://docs.example.com --output ./scraped_docs

# Crawl entire documentation site
python run_scraper.py https://docs.example.com --output ./scraped_docs --crawl

# Specify custom configuration
python run_scraper.py https://docs.example.com --config path/to/config.yaml
```

### Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_scraper.py -v

# Run tests with coverage
pytest tests/ --cov=doc_scraper_fc
```

### Example Scripts

The package includes example scripts to demonstrate usage:

1. Basic scraping script (`run_scraper.py`):
```bash
# Single URL scraping
python run_scraper.py https://docs.example.com

# Site crawling with custom output directory
python run_scraper.py https://docs.example.com --output ./docs --crawl
```

2. Test scraping script (`test_scrape.py`):
```bash
# Test scraping with default configuration
python test_scrape.py

# Test with custom configuration
python test_scrape.py --config custom_config.yaml
```

### Output Options

The scraper supports two output modes that can be used simultaneously:

1. Individual Files:
```yaml
output:
  save_individual_pages: true
  directory: "scraped_docs"
  add_timestamps: true
```

2. Merged Documentation:
```yaml
output:
  save_merged_file: true
  merged_file_prefix: "merged_docs"
```

### Advanced Configuration

The scraper can be extensively configured through YAML:

```yaml
scraping:
  max_pages: 10
  max_depth: 2
  formats:
    - markdown
  options:
    onlyMainContent: true
    removeBase64Images: true

patterns:
  include: 
    - "/docs/"
    - "/guide/"
  exclude:
    - "/blog/"
    - "/changelog/"
```

## Development

1. Set up development environment:
```bash
# Create conda environment
conda create -n doc-scraper python=3.10
conda activate doc-scraper

# Install development dependencies
pip install -e ".[dev]"
```

2. Run code quality tools:
```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy .
```

3. Run tests:
```bash
# Run tests with coverage
pytest tests/ --cov=doc_scraper_fc

# Generate coverage report
pytest tests/ --cov=doc_scraper_fc --cov-report=html
```

## Troubleshooting

1. API Key Issues:
```bash
# Check if .env file is being loaded
python run_scraper.py --debug

# Verify API key is set
echo $FIRECRAWL_API_KEY
```

2. Output Directory Issues:
```bash
# Create output directory
mkdir -p scraped_docs

# Check permissions
ls -la scraped_docs
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Run tests and ensure they pass
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [Firecrawl](https://docs.firecrawl.dev/)
- Inspired by the need for better documentation scraping tools