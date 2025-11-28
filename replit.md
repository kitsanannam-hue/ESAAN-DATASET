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

## Web Dashboard

The project includes an interactive web dashboard for exploring the dataset:

### Features
- **Statistics Overview**: View total features, pages analyzed, and content distribution
- **Interactive Search**: Search across all 680 dissertation pages
- **Data Visualizations**: Charts showing feature categories, page distribution, notation types, and regional coverage
- **Feature Catalog**: Browse and filter all extracted musical features by category
- **Thai-Jazz Connections**: View relationships between Thai musical techniques and Jazz equivalents
- **Phin Dataset**: Explore tuning systems, Lai patterns, and master artists
- **AI Analysis** (requires OpenAI API key): Get AI-powered insights about musical concepts and fusion suggestions
- **Export Data**: Download datasets in JSON or CSV format

### Running the Dashboard
```bash
gunicorn --bind 0.0.0.0:5000 --reload app:app
```

## API Endpoints

### Dataset Endpoints
- `GET /api/summary` - Dataset statistics
- `GET /api/search?q=<query>` - Search content
- `GET /api/feature-catalog` - All features
- `GET /api/features/filter?category=<cat>&search=<term>` - Filter features
- `GET /api/features/categories` - All categories
- `GET /api/relationships` - Thai-Jazz technique connections

### Visualization Endpoints
- `GET /api/visualization/category-distribution` - Feature category chart data
- `GET /api/visualization/page-analysis` - Page content distribution
- `GET /api/visualization/notation-types` - Notation type distribution
- `GET /api/visualization/regional-coverage` - Regional coverage data

### Export Endpoints
- `GET /api/export/features/json` - Download features as JSON
- `GET /api/export/features/csv` - Download features as CSV
- `GET /api/export/phin/json` - Download Phin dataset as JSON
- `GET /api/export/complete/json` - Download complete ML dataset

### AI Endpoints (requires OPENAI_API_KEY)
- `GET /api/ai/status` - Check AI availability
- `POST /api/ai/analyze-feature` - Analyze a musical feature
- `POST /api/ai/explain` - Explain a musical concept
- `POST /api/ai/compare-scales` - Compare Thai and Jazz scales
- `POST /api/ai/fusion-suggestion` - Generate fusion composition ideas

## Recent Changes
- **2025-11-28**: Enhanced web dashboard with AI analysis and visualizations
  - Added AI-powered analysis using OpenAI GPT-5 for musical insights
  - Integrated Chart.js for interactive data visualizations
  - Added advanced filtering by category and search terms
  - Built Thai-Jazz technique relationship mapping
  - Added JSON/CSV export functionality for researchers
  - Implemented dynamic AI availability checking

- **2025-11-28**: Initial extraction and dataset creation
  - Implemented PDF extraction with PyMuPDF
  - Created ML dataset schema for Thai-Jazz fusion
  - Built dataset explorer for interactive analysis
  - Extracted 680 pages with keyword analysis

## User Preferences
- Thai language support enabled
- Focus on cross-cultural music research
- ML dataset structure for audio feature extraction
