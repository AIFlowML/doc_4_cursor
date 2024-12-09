# Doc Scraper Project

This repository contains a powerful documentation scraping tool that helps you extract and process documentation from various websites. The tool is available as a Python package `doc-scraper`.

## Project Structure

```
doc_scraper/
├── doc_scraper/
│   ├── __init__.py
│   ├── cli.py
│   ├── scraper.py
│   └── config/
│       └── sites_config.yaml
├── tests/
│   └── test_scraper.py
├── setup.py
├── README.md
└── LICENSE
```

## Development Setup

1. Clone the repository:
```bash
git clone git@github.com:AIFlowML/doc_4_cursor.git
cd doc_4_cursor
```

2. Set up the environment:

Using conda:
```bash
conda env create -f environment.yml
conda activate doc-scraper
```

Or using venv:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

3. Install in development mode:
```bash
pip install -e .
```

## Running Tests

The project uses pytest for testing. To run the tests:

1. Install test dependencies:
```bash
pip install pytest pytest-cov
```

2. Run tests with coverage:
```bash
pytest tests/ --cov=doc_scraper
```

3. Run specific test file:
```bash
pytest tests/test_scraper.py -v
```

## Testing the CLI

After installation, you can test the CLI commands:

1. Check version:
```bash
doc-scraper version
```

2. Test scraping with example site:
```bash
doc-scraper scrape https://docs.example.com --output-dir ./test_output
```

3. Test with custom config:
```bash
doc-scraper scrape https://docs.example.com --config ./my_config.yaml
```

## Logging

The scraper logs information to:
- Console (INFO level)
- `logs/scraper.log` file (DEBUG level)

Log files are rotated at 1MB with 2 backup files maintained.

## Common Issues

If you encounter any issues:

1. Check the logs in `logs/scraper.log`
2. Ensure you have the correct permissions for the output directory
3. Verify your internet connection
4. Check if the target website is accessible

## Contributing

1. Fork the repository from [AIFlowML/doc_4_cursor](https://github.com/AIFlowML/doc_4_cursor)
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests to ensure everything works
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 