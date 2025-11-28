
# Cross-Cultural Music ML Dataset Extractor

## Overview

This project analyzes the PhD dissertation "Machine Learning Dataset for Cross-Cultural Music" (680 pages) by Tanarat Chaichana. It extracts and structures data for creating ML datasets focused on Thai-Jazz fusion music research.

## Features

- **PDF Text Extraction**: Extract text from all 680 pages using PyMuPDF
- **Chapter Detection**: Automatically identify chapter structure
- **Keyword Analysis**: Find music-related keywords (Thai music, Jazz, cross-cultural, ML)
- **Feature Cataloging**: Build comprehensive music feature catalogs
- **Dataset Schema**: Define ML dataset schema for Thai-Jazz fusion
- **Phin Dataset**: Specialized dataset for Thai Phin instrument research
- **Interactive Explorer**: Tools for exploring and querying extracted data

## Quick Start

```bash
# Run full extraction pipeline
python main.py

# Explore the dataset interactively
python src/dataset_explorer.py
```

## Project Structure

```
/
├── main.py                          # Main entry point
├── src/
│   ├── pdf_extractor.py            # PDF text extraction
│   ├── dataset_builder.py          # ML dataset schema builder
│   ├── dataset_explorer.py         # Interactive exploration tools
│   └── phin_dataset_builder.py     # Phin instrument dataset
├── output/
│   ├── dissertation_extracted.json  # Full extracted text
│   ├── dissertation_pages.csv       # Page-by-page data
│   ├── dissertation_analysis.csv    # Feature analysis
│   ├── dataset/                     # ML dataset files
│   └── phin_dataset/                # Phin-specific dataset
└── attached_assets/
    └── [PhD Dissertation PDF]
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
