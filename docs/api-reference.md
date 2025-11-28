
# API Reference

## DissertationExtractor

Main class for extracting text and metadata from PDF dissertations.

### Constructor

```python
DissertationExtractor(pdf_path: str)
```

**Parameters:**
- `pdf_path` (str): Path to the PDF file

### Methods

#### extract_all_text()

```python
extract_all_text(progress_callback=None) -> Dict[int, str]
```

Extract text from all pages.

**Parameters:**
- `progress_callback` (callable, optional): Function called with (current, total) for progress tracking

**Returns:**
- Dict mapping page numbers to extracted text

#### extract_page_range()

```python
extract_page_range(start: int, end: int) -> Dict[int, str]
```

Extract text from specific page range.

**Parameters:**
- `start` (int): Starting page number (1-indexed)
- `end` (int): Ending page number (inclusive)

**Returns:**
- Dict mapping page numbers to extracted text

#### identify_chapters()

```python
identify_chapters() -> List[Dict]
```

Identify chapter structure from extracted text.

**Returns:**
- List of chapter dictionaries with keys: `chapter_number`, `title`, `start_page`, `raw_match`

#### find_music_keywords()

```python
find_music_keywords() -> Dict[str, List[Dict]]
```

Find pages containing music-related keywords.

**Returns:**
- Dict mapping categories to lists of matches:
  - `thai_music`
  - `jazz`
  - `cross_cultural`
  - `ml_dataset`
  - `music_theory`

#### export_to_json()

```python
export_to_json(output_path: str)
```

Export all extracted data to JSON.

#### export_to_dataframe()

```python
export_to_dataframe() -> pd.DataFrame
```

Convert extracted text to pandas DataFrame.

## ThaiJazzDatasetBuilder

Build ML dataset for Thai-Jazz cross-cultural music fusion.

### Constructor

```python
ThaiJazzDatasetBuilder()
```

### Methods

#### build_from_extracted_data()

```python
build_from_extracted_data(extracted_data: Dict) -> pd.DataFrame
```

Build dataset from extracted dissertation data.

**Parameters:**
- `extracted_data` (dict): Dictionary from DissertationExtractor.export_to_json()

**Returns:**
- DataFrame with analyzed features

#### generate_feature_catalog()

```python
generate_feature_catalog() -> pd.DataFrame
```

Generate catalog of all music features for ML.

**Returns:**
- DataFrame with columns: `feature_name`, `category`, `description`, `sub_types`

#### export_dataset()

```python
export_dataset(output_dir: str) -> Path
```

Export all dataset components.

**Parameters:**
- `output_dir` (str): Directory to save dataset files

**Returns:**
- Path object to output directory

## DatasetExplorer

Interactive explorer for the Thai-Jazz music dataset.

### Constructor

```python
DatasetExplorer(output_dir: str = "output")
```

**Parameters:**
- `output_dir` (str): Directory containing extracted data

### Methods

#### get_page_content()

```python
get_page_content(page_num: int) -> str
```

Get text content of a specific page.

#### search_content()

```python
search_content(query: str, case_sensitive: bool = False) -> List[Dict]
```

Search for text across all pages.

**Parameters:**
- `query` (str): Search term
- `case_sensitive` (bool): Whether search is case-sensitive

**Returns:**
- List of dicts with keys: `page`, `context`

#### get_thai_music_pages()

```python
get_thai_music_pages() -> pd.DataFrame
```

Get all pages containing Thai music content.

#### get_jazz_pages()

```python
get_jazz_pages() -> pd.DataFrame
```

Get all pages containing Jazz content.

#### get_fusion_pages()

```python
get_fusion_pages() -> pd.DataFrame
```

Get all pages containing cross-cultural fusion content.

#### get_ml_pages()

```python
get_ml_pages() -> pd.DataFrame
```

Get all pages containing ML-related content.

#### get_feature_statistics()

```python
get_feature_statistics() -> Dict[str, Any]
```

Get statistics about features in the dataset.

#### summary()

```python
summary() -> str
```

Generate text summary of the dataset.

## PhinDatasetBuilder

Build specialized dataset for Thai Phin instrument.

### Constructor

```python
PhinDatasetBuilder(output_dir: str = "output/phin_dataset")
```

### Methods

#### build_tuning_dataset()

```python
build_tuning_dataset() -> pd.DataFrame
```

Build dataset of phin tuning systems.

#### build_lai_dataset()

```python
build_lai_dataset() -> pd.DataFrame
```

Build dataset of lai melodic patterns.

#### build_artist_dataset()

```python
build_artist_dataset() -> pd.DataFrame
```

Build dataset of phin master artists.

#### build_technique_dataset()

```python
build_technique_dataset() -> pd.DataFrame
```

Build dataset of phin playing techniques.

#### export_all()

```python
export_all() -> Dict
```

Export all phin datasets and return combined dataset dictionary.
