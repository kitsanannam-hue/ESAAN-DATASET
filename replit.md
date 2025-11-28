# Cross-Cultural Music ML Dataset Extractor

## Overview
This project analyzes the PhD dissertation "Machine Learning Dataset for Cross-Cultural Music" (680 pages) by Tanarat Chaichana. It extracts and structures data for creating ML datasets focused on Thai-Jazz fusion music research.

## Project Architecture

```
/
├── main.py                          # Main entry point - runs full extraction
├── src/
│   ├── pdf_extractor.py            # PDF text extraction using PyMuPDF
│   ├── dataset_builder.py          # ML dataset schema and feature builder
│   └── dataset_explorer.py         # Interactive dataset exploration tools
├── output/
│   ├── dissertation_extracted.json  # Full extracted text (JSON)
│   ├── dissertation_pages.csv       # Page-by-page data
│   ├── dissertation_analysis.csv    # Feature analysis results
│   └── dataset/
│       ├── schema.json              # ML dataset schema
│       ├── feature_catalog.csv      # Music feature catalog
│       └── feature_catalog.json     # Feature catalog (JSON)
└── attached_assets/
    └── [PhD Dissertation PDF]       # Source document
```

## Key Features

### PDF Extraction (pdf_extractor.py)
- Extracts text from all 680 pages using PyMuPDF
- Identifies chapter structure
- Finds music-related keywords (Thai music, Jazz, cross-cultural, ML)
- Detects tables and figures
- Exports to JSON and CSV formats

### Dataset Builder (dataset_builder.py)
- Defines ML dataset schema for Thai-Jazz fusion
- Catalogs music features:
  - Thai Traditional: thang (modes), luk_tok (rhythm), ornaments, scale_structure
  - Jazz Modern: chord_types, scales_modes, rhythm_patterns, improvisation
  - Cross-Cultural Fusion: melody_integration, harmony_adaptation, rhythm_fusion
- Specifies audio features: MFCC, spectral, temporal, harmonic
- Defines annotation types: melodic, harmonic, rhythmic, structural

### Dataset Explorer (dataset_explorer.py)
- Interactive exploration of extracted data
- Search across all pages
- Filter by content type (Thai music, Jazz, fusion, ML)
- View feature statistics
- Export subsets of data

## Usage

### Run Full Extraction
```bash
python main.py
```

### Explore Dataset
```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Get summary
print(explorer.summary())

# Search content
results = explorer.search_content("improvisation")

# Get Thai music pages
thai_pages = explorer.get_thai_music_pages()

# Get Jazz pages
jazz_pages = explorer.get_jazz_pages()

# Get fusion pages
fusion_pages = explorer.get_fusion_pages()
```

### View Feature Catalog
```python
catalog = explorer.get_feature_catalog()
schema = explorer.get_schema()
```

## Dissertation Analysis Results

- **Total Pages**: 680
- **Tables**: 1
- **Figures**: 423
- **Chapters**: 87 sections identified

### Keyword Coverage
- Thai Music: 177 pages
- Jazz: 263 pages
- Cross-Cultural: 116 pages
- ML Dataset: 120 pages
- Music Theory: 261 pages

### Extracted Features
- Improvisation: 94 instances
- Rhythm: 52 instances
- Thai Mode (Thang): 42 instances
- Jazz Chord: 15 instances
- Ornamentation: 9 instances
- Harmony: 7 instances
- Melody: 3 instances

## ML Dataset Schema

The dataset schema supports:

### Audio Features
- Spectral: MFCC, spectral centroid, bandwidth, rolloff, chroma
- Temporal: tempo, beat frames, onset strength
- Harmonic: tonnetz, harmonic-percussive ratio
- Rhythm: tempo, beat histogram, rhythm pattern

### Annotation Types
- Melodic: pitch contour, ornament type, phrase boundary
- Harmonic: chord label, key, mode
- Rhythmic: beat position, accent pattern, tempo variation
- Structural: section label, form, transition type

## Phin Dataset (พิณ)

A specialized dataset for Thai Phin instrument research:

### Files in output/phin_dataset/
- `phin_tuning.csv/json` - 13 tuning systems for 2/3/4 string phin
- `phin_lai_patterns.csv/json` - 5 melodic patterns (ลาย)
- `phin_artists.csv/json` - 2 master performers
- `phin_techniques.csv/json` - 5 playing techniques
- `phin_ml_schema.json` - ML feature schema for audio analysis
- `phin_dataset_complete.json` - Combined dataset

### Usage
```python
from src.phin_dataset_builder import PhinDatasetBuilder

builder = PhinDatasetBuilder()
builder.load_phin_pages("/tmp/phin_pages_raw.json")
dataset = builder.export_all()

# Access individual datasets
tuning_df = builder.build_tuning_dataset()
lai_df = builder.build_lai_dataset()
```

## Dependencies
- Python 3.11
- PyMuPDF (fitz) - PDF text extraction
- pandas - Data manipulation and export

## Recent Changes
- **2025-11-28**: Initial extraction and dataset creation
  - Implemented PDF extraction with PyMuPDF
  - Created ML dataset schema for Thai-Jazz fusion
  - Built dataset explorer for interactive analysis
  - Extracted 680 pages with keyword analysis

## User Preferences
- Thai language support enabled
- Focus on cross-cultural music research
- ML dataset structure for audio feature extraction
