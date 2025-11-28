
# Cross-Cultural Music ML Dataset Extractor

## Overview

This project analyzes the PhD dissertation "Machine Learning Dataset for Cross-Cultural Music" (680 pages) by Tanarat Chaichana. It extracts and structures data for creating ML datasets focused on Thai-Jazz fusion music research.

## Features

- **PDF Text Extraction**: Extract text from all 680 pages using PyMuPDF
- **Chapter Detection**: Automatically identify chapter structure
- **Musical Notation Extraction**: Extract and analyze musical notation, scales, and chord progressions
- **Keyword Analysis**: Find music-related keywords (Thai music, Jazz, cross-cultural, ML)
- **Feature Cataloging**: Build comprehensive music feature catalogs
- **Dataset Schema**: Define ML dataset schema for Thai-Jazz fusion
- **Phin Dataset**: Specialized dataset for Thai Phin instrument research
- **Data Quality Checking**: Automated data validation and cleaning
- **Interactive Explorer**: Tools for exploring and querying extracted data
- **Web Dashboard**: Flask-based web interface for dataset exploration

## Quick Start

```bash
# Run full extraction pipeline
python main.py

# Start web dashboard
python app.py

# Or use the Run button (starts Web Dashboard workflow)
```

## Project Structure

```
/
├── app.py                           # Flask web dashboard
├── main.py                          # Main extraction pipeline
├── config/
│   ├── __init__.py
│   └── settings.py                  # Configuration settings
├── src/
│   ├── extractors/
│   │   ├── pdf_extractor.py         # PDF text extraction
│   │   └── music_notation_extractor.py  # Musical notation extraction
│   ├── analyzers/
│   │   ├── music_theory_analyzer.py # Music theory analysis
│   │   └── data_quality_checker.py  # Data validation
│   ├── builders/
│   │   ├── dataset_builder.py       # ML dataset schema builder
│   │   ├── phin_dataset_builder.py  # Phin instrument dataset
│   │   └── thai_jazz_ml_builder.py  # Thai-Jazz ML features
│   └── explorers/
│       └── dataset_explorer.py      # Interactive exploration tools
├── data/
│   ├── raw/dissertations/           # Source PDF files
│   └── processed/                   # Processed data
├── output/
│   ├── dissertation_extracted.json  # Full extracted text
│   ├── dissertation_pages.csv       # Page-by-page data
│   ├── dissertation_analysis.csv    # Feature analysis
│   ├── dataset/                     # ML dataset files
│   ├── phin_dataset/                # Phin-specific dataset
│   ├── ml_dataset/                  # Thai-Jazz ML features
│   └── music_notation_dataset/      # Musical notation data
├── scripts/
│   ├── export_all_datasets.py       # Export all datasets
│   ├── validate_data.py             # Data validation script
│   └── setup_project.py             # Project setup
├── templates/
│   └── index.html                   # Web dashboard template
├── static/                          # Web assets (CSS, JS, images)
├── tests/                           # Unit tests
└── docs/                            # Documentation
```

## Documentation

- [Installation & Setup](./installation.md)
- [Usage Guide](./usage.md)
- [API Reference](./api-reference.md)
- [Dataset Schema](./dataset-schema.md)
- [Phin Dataset](./phin-dataset.md)
- [Examples](./examples.md)

## Results

After processing the 680-page dissertation, the extraction yields:

- **177 pages** with Thai music content
- **263 pages** with Jazz content
- **116 pages** with cross-cultural fusion content
- **120 pages** with ML-related content
- **423 figures** and **1 table** identified
- **87 chapters/sections** detected

## License

This project is for research and educational purposes.
