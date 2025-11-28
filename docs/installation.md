
# Installation Guide

## System Requirements

- Python 3.11 or higher
- PyMuPDF (fitz) library
- pandas library

## Installation on Replit

This project is ready to run on Replit with all dependencies pre-configured.

1. Open the Repl
2. Dependencies are automatically installed via `pyproject.toml`
3. Run `python main.py` to start extraction

## Local Installation

If running locally, install dependencies:

```bash
# Install required Python packages
pip install pymupdf pandas

# Or use the project dependencies
pip install -r pyproject.toml
```

## Verify Installation

```python
from src.pdf_extractor import DissertationExtractor
from src.dataset_builder import ThaiJazzDatasetBuilder
from src.dataset_explorer import DatasetExplorer

print("All modules imported successfully!")
```

## Troubleshooting

### PyMuPDF Installation Issues

If you encounter issues with PyMuPDF:

```bash
pip install --upgrade pymupdf
```

### Memory Issues

For large PDF processing:
- Ensure at least 2GB RAM available
- Process pages in batches if needed
- Use the `small=True` parameter for smaller datasets

## Next Steps

Once installed, proceed to the [Usage Guide](./usage.md) to learn how to use the extractor.
