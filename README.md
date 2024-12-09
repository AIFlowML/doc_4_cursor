# Documentation Scraping Tools

This repository contains a collection of tools for scraping and processing documentation from various sources.

## Packages

### 1. Doc Scraper FC (Firecrawl)

A powerful documentation scraper built on top of Firecrawl, designed for efficient extraction and processing of web-based documentation.

#### Installation and Setup

```bash
# Clone the repository
git clone https://github.com/AIFlowML/doc_4_cursor.git
cd doc_4_cursor

# Create and activate conda environment
conda create -n doc-scraper python=3.10
conda activate doc-scraper

# Install Firecrawl scraper
cd doc_scraper_fc
pip install -e .

# Configure API key
cp .env_example .env
# Edit .env and add your Firecrawl API key
```

#### Usage

```bash
# Basic URL scraping
python run_scraper.py https://docs.example.com --output ./scraped_docs

# Crawl entire documentation site
python run_scraper.py https://docs.example.com --output ./scraped_docs --crawl

# Run tests
pytest tests/ -v
```

### 2. Doc Scraper (Classic)

A traditional web scraping tool using BeautifulSoup and other Python libraries for documentation extraction.

#### Installation and Setup

```bash
# Using the same conda environment
cd doc_scraper
pip install -e .
```

#### Usage

```bash
# Basic scraping
python scrape_phidata.py --output ./docs

# Run tests
pytest tests/ -v
```

## Development

### Environment Setup

```bash
# Create conda environment
conda create -n doc-scraper python=3.10
conda activate doc-scraper

# Install development dependencies for both packages
cd doc_scraper_fc
pip install -e ".[dev]"
cd ../doc_scraper
pip install -e ".[dev]"
```

### Running Tests

```bash
# Test Firecrawl scraper
cd doc_scraper_fc
pytest tests/ -v --cov=doc_scraper_fc

# Test classic scraper
cd ../doc_scraper
pytest tests/ -v --cov=doc_scraper
```

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy .
```

## Project Structure

```
doc_4_cursor/
├── doc_scraper_fc/         # Firecrawl-based scraper
│   ├── doc_scraper_fc/     # Package source
│   ├── tests/             # Test files
│   ├── config/            # Configuration files
│   └── README.md         # Package documentation
│
└── doc_scraper/           # Classic scraper
    ├── doc_scraper/      # Package source
    ├── tests/            # Test files
    └── README.md        # Package documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Run tests and ensure they pass
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 