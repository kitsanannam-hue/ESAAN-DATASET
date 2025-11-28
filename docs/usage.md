
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
5. Extract musical notation
6. Generate ML dataset schema
7. Export results to `output/` directory

## Web Dashboard

Start the interactive web dashboard:

```bash
python app.py
# Or click the Run button in Replit
```

The dashboard provides:
- Dataset statistics and summaries
- Thai music content exploration
- Jazz content exploration
- Phin dataset visualization
- Musical notation browser

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
from src.builders.phin_dataset_builder import PhinDatasetBuilder

builder = PhinDatasetBuilder()

# Build individual datasets
tuning_df = builder.build_tuning_dataset()
lai_df = builder.build_lai_dataset()
artist_df = builder.build_artist_dataset()
technique_df = builder.build_technique_dataset()

# Export all datasets
builder.export_all()
```

### Thai-Jazz ML Features

```python
from src.builders.thai_jazz_ml_builder import ThaiJazzMLBuilder

builder = ThaiJazzMLBuilder()

# Build feature datasets
features_df = builder.build_thai_jazz_features()
hybrid_df = builder.build_hybridization_techniques()
scale_df = builder.build_scale_mapping()

# Export all
builder.export_all()
```

### Musical Notation Extraction

```python
from src.extractors.music_notation_extractor import MusicNotationExtractor

extractor = MusicNotationExtractor()

# Extract from dissertation
extractor.extract_from_dissertation("path/to/pdf")

# Get specific notation types
western_notes = extractor.get_western_notation()
scale_degrees = extractor.get_scale_degrees()
lai_modes = extractor.get_lai_modes()

# Export dataset
extractor.export_dataset()
```

### Data Quality Checking

```python
from src.analyzers.data_quality_checker import DataQualityChecker

checker = DataQualityChecker()

# Check all datasets
report = checker.check_all_datasets()

# Clean data
checker.clean_datasets()

# Validate specific dataset
is_valid = checker.validate_dataset("phin_tuning")
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
├── phin_dataset/
│   ├── phin_tuning.csv/json    # Tuning systems
│   ├── phin_lai_patterns.csv/json  # Melodic patterns
│   ├── phin_artists.csv/json   # Master performers
│   ├── phin_techniques.csv/json    # Playing techniques
│   └── phin_ml_schema.json     # ML feature schema
├── ml_dataset/
│   ├── thai_jazz_features.csv/json  # Thai-Jazz features
│   ├── hybridization_techniques.csv/json  # Fusion techniques
│   ├── thai_jazz_scale_mapping.csv/json  # Scale mappings
│   └── ml_audio_features_schema.json  # Audio features schema
└── music_notation_dataset/
    ├── notations.csv/json       # All musical notations
    ├── compositions.json        # Compositions found
    └── notation_summary.json    # Summary statistics
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
