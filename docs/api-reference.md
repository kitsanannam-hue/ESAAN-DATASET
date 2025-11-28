
# API Reference

## Extractors

### DissertationExtractor

Main class for extracting text and metadata from PDF dissertations.

**Module:** `src.extractors.pdf_extractor`

#### Constructor

```python
DissertationExtractor(pdf_path: str)
```

**Parameters:**
- `pdf_path` (str): Path to the PDF file

#### Methods

##### extract_all_text()

```python
extract_all_text(progress_callback=None) -> Dict[int, str]
```

Extract text from all pages.

**Parameters:**
- `progress_callback` (callable, optional): Function called with (current, total) for progress tracking

**Returns:**
- Dict mapping page numbers to extracted text

##### extract_page_range()

```python
extract_page_range(start: int, end: int) -> Dict[int, str]
```

Extract text from specific page range.

##### identify_chapters()

```python
identify_chapters() -> List[Dict]
```

Identify chapter structure from extracted text.

##### find_music_keywords()

```python
find_music_keywords() -> Dict[str, List[Dict]]
```

Find pages containing music-related keywords.

### MusicNotationExtractor

Extract musical notation from dissertation pages.

**Module:** `src.extractors.music_notation_extractor`

#### Methods

##### extract_from_dissertation()

```python
extract_from_dissertation(pdf_path: str) -> pd.DataFrame
```

Extract all musical notation from dissertation.

##### get_western_notation()

```python
get_western_notation() -> List[Dict]
```

Get Western musical notation (C, D, E, etc.).

##### get_scale_degrees()

```python
get_scale_degrees() -> List[Dict]
```

Get scale degree notation (1, 2, 3, etc.).

##### get_lai_modes()

```python
get_lai_modes() -> List[Dict]
```

Get Thai lai mode references.

## Builders

### ThaiJazzDatasetBuilder

Build ML dataset for Thai-Jazz cross-cultural music fusion.

**Module:** `src.builders.dataset_builder`

#### Methods

##### build_from_extracted_data()

```python
build_from_extracted_data(extracted_data: Dict) -> pd.DataFrame
```

Build dataset from extracted dissertation data.

##### generate_feature_catalog()

```python
generate_feature_catalog() -> pd.DataFrame
```

Generate catalog of all music features for ML.

### PhinDatasetBuilder

Build specialized dataset for Thai Phin instrument.

**Module:** `src.builders.phin_dataset_builder`

#### Methods

##### build_tuning_dataset()

```python
build_tuning_dataset() -> pd.DataFrame
```

Build dataset of phin tuning systems.

##### build_lai_dataset()

```python
build_lai_dataset() -> pd.DataFrame
```

Build dataset of lai melodic patterns.

##### build_artist_dataset()

```python
build_artist_dataset() -> pd.DataFrame
```

Build dataset of phin master artists.

### ThaiJazzMLBuilder

Build Thai-Jazz ML features dataset.

**Module:** `src.builders.thai_jazz_ml_builder`

#### Methods

##### build_thai_jazz_features()

```python
build_thai_jazz_features() -> pd.DataFrame
```

Build Thai-Jazz feature dataset.

##### build_hybridization_techniques()

```python
build_hybridization_techniques() -> pd.DataFrame
```

Build hybridization techniques dataset.

##### build_scale_mapping()

```python
build_scale_mapping() -> pd.DataFrame
```

Build Thai-Jazz scale mapping dataset.

## Analyzers

### MusicTheoryAnalyzer

Analyze music theory concepts in the dissertation.

**Module:** `src.analyzers.music_theory_analyzer`

#### Methods

##### analyze_scales()

```python
analyze_scales(text: str) -> List[Dict]
```

Analyze scale references in text.

##### analyze_modes()

```python
analyze_modes(text: str) -> List[Dict]
```

Analyze mode references (Thai thang, Jazz modes).

### DataQualityChecker

Validate and clean dataset quality.

**Module:** `src.analyzers.data_quality_checker`

#### Methods

##### check_all_datasets()

```python
check_all_datasets() -> Dict
```

Check quality of all datasets.

##### clean_datasets()

```python
clean_datasets()
```

Clean all datasets.

##### validate_dataset()

```python
validate_dataset(dataset_name: str) -> bool
```

Validate a specific dataset.

## Explorers

### DatasetExplorer

Interactive explorer for the Thai-Jazz music dataset.

**Module:** `src.explorers.dataset_explorer`

#### Methods

##### get_page_content()

```python
get_page_content(page_num: int) -> str
```

Get text content of a specific page.

##### search_content()

```python
search_content(query: str, case_sensitive: bool = False) -> List[Dict]
```

Search for text across all pages.

##### get_thai_music_pages()

```python
get_thai_music_pages() -> pd.DataFrame
```

Get all pages containing Thai music content.

##### get_jazz_pages()

```python
get_jazz_pages() -> pd.DataFrame
```

Get all pages containing Jazz content.

##### get_feature_statistics()

```python
get_feature_statistics() -> Dict[str, Any]
```

Get statistics about features in the dataset.

## Web API Endpoints

The Flask application (`app.py`) provides these REST API endpoints:

### GET /api/summary

Get dataset summary statistics.

### GET /api/thai-music-pages

Get pages containing Thai music content.

### GET /api/jazz-pages

Get pages containing Jazz content.

### GET /api/phin-lai-patterns

Get Phin lai patterns dataset.

### GET /api/notations

Get musical notation dataset.

### GET /api/compositions

Get musical compositions found.

### GET /api/notation-summary

Get notation dataset summary.
