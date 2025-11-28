
# Examples

## Basic Extraction

Extract all data from the dissertation:

```python
from src.pdf_extractor import DissertationExtractor

extractor = DissertationExtractor("attached_assets/Tanarat Chaichana - PhD Dissertation [complete] 14_04_2022_1764338380212.pdf")

# Extract all text
text = extractor.extract_all_text()
print(f"Extracted {len(text)} pages")

# Find chapters
chapters = extractor.identify_chapters()
for ch in chapters[:5]:
    print(f"Chapter {ch['chapter_number']}: {ch['title']}")

# Export results
extractor.export_to_json("output/extracted.json")
```

## Search for Specific Topics

Search for improvisation techniques:

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Search for improvisation
improv_results = explorer.search_content("improvisation")
print(f"Found {len(improv_results)} pages about improvisation")

for result in improv_results[:3]:
    print(f"\nPage {result['page']}:")
    print(result['context'])
```

## Analyze Thai Music Features

Find all references to Thai modes (thang):

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Get Thai mode references
thang_refs = explorer.get_thang_references()

print(f"Found {len(thang_refs)} thang references")
for ref in thang_refs[:5]:
    print(f"Page {ref['page']} ({ref['keyword']}): {ref['context'][:100]}...")
```

## Build Custom Feature Catalog

Create a catalog of specific music features:

```python
from src.dataset_builder import ThaiJazzDatasetBuilder
import json

builder = ThaiJazzDatasetBuilder()

# Get feature catalog
catalog = builder.generate_feature_catalog()

# Filter Thai traditional features
thai_features = catalog[catalog['category'] == 'thai_traditional']
print(thai_features)

# Export to CSV
thai_features.to_csv("output/thai_features.csv", index=False)
```

## Extract Phin Data

Work with the Phin instrument dataset:

```python
from src.phin_dataset_builder import PhinDatasetBuilder

builder = PhinDatasetBuilder()

# Get all tuning systems
tunings = builder.build_tuning_dataset()
print("Phin Tuning Systems:")
print(tunings[['string_count', 'tuning', 'description']])

# Get lai patterns
lai_patterns = builder.build_lai_dataset()
print("\nLai Patterns:")
for _, lai in lai_patterns.iterrows():
    print(f"{lai['name_thai']} - {lai['meaning']}")

# Export everything
builder.export_all()
```

## Filter by Content Type

Get pages by specific content categories:

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Get pages about Thai music
thai_pages = explorer.get_thai_music_pages()
print(f"Thai music: {len(thai_pages)} entries")

# Get pages about Jazz
jazz_pages = explorer.get_jazz_pages()
print(f"Jazz: {len(jazz_pages)} entries")

# Get pages about fusion
fusion_pages = explorer.get_fusion_pages()
print(f"Cross-cultural fusion: {len(fusion_pages)} entries")

# Get pages about ML
ml_pages = explorer.get_ml_pages()
print(f"Machine learning: {len(ml_pages)} entries")
```

## Export Subset of Data

Export specific pages for focused analysis:

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Get pages about improvisation
improv_pages = explorer.get_pages_with_feature('improvisation')
page_numbers = improv_pages['page'].unique().tolist()

# Export just those pages
explorer.export_subset(pages=page_numbers, output_path="output/improvisation_subset.json")
print(f"Exported {len(page_numbers)} pages to improvisation_subset.json")
```

## Analyze Feature Distribution

Get statistics on feature occurrence:

```python
from src.dataset_explorer import DatasetExplorer
import pandas as pd

explorer = DatasetExplorer()

# Get feature statistics
stats = explorer.get_feature_statistics()

print(f"Total feature instances: {stats['total_entries']}")
print(f"Unique pages analyzed: {stats['unique_pages']}")
print(f"\nContent distribution:")
print(f"  Thai music: {stats['thai_music_count']} pages")
print(f"  Jazz: {stats['jazz_count']} pages")
print(f"  Fusion: {stats['fusion_count']} pages")
print(f"  ML: {stats['ml_count']} pages")

print(f"\nTop features:")
for feature, count in list(stats['feature_counts'].items())[:10]:
    print(f"  {feature}: {count}")
```

## Working with Page Content

Read and analyze specific pages:

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Get content from a specific page
page_101_content = explorer.get_page_content(101)
print("Page 101 content:")
print(page_101_content[:500])  # First 500 characters

# Search within specific page content
if "phin" in page_101_content.lower():
    print("\nPage 101 contains information about the Phin instrument")
```

## Generate Summary Report

Create a comprehensive summary:

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Generate and print summary
summary = explorer.summary()
print(summary)

# Save summary to file
with open("output/dataset_summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)
```

## Batch Processing

Process multiple features at once:

```python
from src.dataset_explorer import DatasetExplorer

explorer = DatasetExplorer()

# Define features of interest
features = ['rhythm', 'improvisation', 'thai_mode', 'jazz_chord']

# Get pages for each feature
results = {}
for feature in features:
    df = explorer.get_pages_with_feature(feature)
    results[feature] = {
        'count': len(df),
        'unique_pages': df['page'].nunique() if not df.empty else 0,
        'sample_pages': df['page'].unique()[:5].tolist() if not df.empty else []
    }

# Display results
for feature, data in results.items():
    print(f"\n{feature.upper()}:")
    print(f"  Instances: {data['count']}")
    print(f"  Unique pages: {data['unique_pages']}")
    print(f"  Sample pages: {data['sample_pages']}")
```
