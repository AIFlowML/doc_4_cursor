from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="doc_scraper",
    version="0.1.0",
    author="Igor Lessio",
    author_email="igor@aiflow.ml",
    description="A tool for scraping documentation websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIFlowML/doc_4_cursor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "markdownify>=0.11.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "rich>=10.0.0",
        "typer>=0.9.0",
        "PyYAML>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "doc-scraper=doc_scraper.cli:app",
        ],
    },
    include_package_data=True,
    package_data={
        "doc_scraper": ["config/*.yaml"],
    },
) 