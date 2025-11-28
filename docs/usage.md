
# Usage Guide

## Running the Full Extraction

The simplest way to extract all data from the dissertation:

```bash
python main.py
```

This will:
1. Load the PDF (680 pages)
2. Extract all text
3. Identify chapters
4. Analyze music features
5. Generate ML dataset schema
6. Export results to `output/` directory

## Using Individual Components

### PDF Extraction

```python
from src.pdf_extractor import DissertationExtractor

# Initialize extractor
extractor = DissertationExtractor("path/to/dissertation.pdf")

# Extract all text
extracted_text = extractor.extract_all_text()

# Extract specific page range
page_range = extractor.extract_page_range(start=100, end=200)

# Identify chapters
chapters = extractor.identify_chapters()

# Find music keywords
keywords = extractor.find_music_keywords()

# Export results
extractor.export_to_json("output/extracted.json")
extractor.export_to_dataframe().to_csv("output/pages.csv")
```

### Dataset Building

```python
from src.dataset_builder import ThaiJazzDatasetBuilder

builder = ThaiJazzDatasetBuilder()

# Load extracted data
with open("output/dissertation_extracted.json") as f:
    data = json.load(f)

# Build dataset from extracted text
analysis_df = builder.build_from_extracted_data(data)

# Generate feature catalog
catalog = builder.generate_feature_catalog()

# Export dataset
builder.export_dataset("output/dataset")
```

### Interactive Exploration

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# View summary
print(explorer.summary())

# Search content
results = explorer.search_content("improvisation")

# Get specific content types
thai_pages = explorer.get_thai_music_pages()
jazz_pages = explorer.get_jazz_pages()
fusion_pages = explorer.get_fusion_pages()

# Get feature statistics
stats = explorer.get_feature_statistics()

# Export subset
explorer.export_subset(pages=[1, 2, 3], output_path="subset.json")
```

### Phin Dataset

```python
from src.phin_dataset_builder import PhinDatasetBuilder

builder = PhinDatasetBuilder()

# Build individual datasets
tuning_df = builder.build_tuning_dataset()
lai_df = builder.build_lai_dataset()
artist_df = builder.build_artist_dataset()
technique_df = builder.build_technique_dataset()

# Export all datasets
builder.export_all()
```

## Output Files

After running the extraction, you'll find:

```
output/
├── dissertation_extracted.json  # Full text extraction
├── dissertation_pages.csv       # Page-by-page breakdown
├── dissertation_analysis.csv    # Feature analysis
├── dataset/
│   ├── schema.json             # ML dataset schema
│   ├── feature_catalog.csv     # Music feature catalog
│   └── feature_catalog.json    # Feature catalog (JSON)
└── phin_dataset/
    ├── phin_tuning.csv/json    # Tuning systems
    ├── phin_lai_patterns.csv/json  # Melodic patterns
    ├── phin_artists.csv/json   # Master performers
    ├── phin_techniques.csv/json    # Playing techniques
    └── phin_ml_schema.json     # ML feature schema
```

## Advanced Usage

### Custom Progress Callback

```python
def my_progress(current, total):
    print(f"Processing page {current} of {total}")

extractor.extract_all_text(progress_callback=my_progress)
```

### Filtering by Keywords

```python
# Find all references to Thai modes (thang)
thang_refs = explorer.get_thang_references()

# Find improvisation examples
improv_examples = explorer.get_improvisation_examples()
```

### Working with Specific Features

```python
# Get pages with specific feature
mfcc_pages = explorer.get_pages_with_feature('mfcc')
rhythm_pages = explorer.get_pages_with_feature('rhythm')
```

## Next Steps

- Review the [API Reference](./api-reference.md) for detailed method documentation
- Explore the [Dataset Schema](./dataset-schema.md) to understand the ML dataset structure
- Check out [Examples](./examples.md) for common use cases
