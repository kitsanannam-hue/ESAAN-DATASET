#!/usr/bin/env python3
"""
Cross-Cultural Music ML Dataset Extractor
==========================================
Analyzes PhD dissertation on Thai-Jazz fusion music
and creates structured ML dataset.

Author: Generated for Music Research Analysis
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from pdf_extractor import DissertationExtractor, print_progress
from dataset_builder import ThaiJazzDatasetBuilder


def main():
    """Main entry point for the dissertation analysis."""
    
    pdf_path = "attached_assets/Tanarat Chaichana - PhD Dissertation [complete] 14_04_2022_1764338380212.pdf"
    output_dir = Path("output")
    
    print("=" * 70)
    print("  CROSS-CULTURAL MUSIC ML DATASET EXTRACTOR")
    print("  Thai-Jazz Fusion Music Research Analysis")
    print("=" * 70)
    
    if not Path(pdf_path).exists():
        print(f"\nError: PDF file not found at {pdf_path}")
        print("Please ensure the dissertation PDF is in the attached_assets folder.")
        return
    
    print(f"\n[1/5] Loading PDF...")
    extractor = DissertationExtractor(pdf_path)
    print(f"      Loaded: {extractor.total_pages} pages")
    
    print(f"\n[2/5] Extracting text from all pages...")
    extractor.extract_all_text(progress_callback=print_progress)
    
    print(f"\n[3/5] Analyzing document structure...")
    chapters = extractor.identify_chapters()
    print(f"      Found {len(chapters)} chapters")
    
    print(f"\n[4/5] Generating analysis report...")
    summary = extractor.generate_summary_report()
    
    output_dir.mkdir(exist_ok=True)
    
    extractor.export_to_json(str(output_dir / "dissertation_extracted.json"))
    
    df = extractor.export_to_dataframe()
    df.to_csv(str(output_dir / "dissertation_pages.csv"), index=False)
    
    print(f"\n[5/5] Building ML dataset structure...")
    builder = ThaiJazzDatasetBuilder()
    
    with open(output_dir / "dissertation_extracted.json", 'r', encoding='utf-8') as f:
        extracted_data = json.load(f)
    
    analysis_df = builder.build_from_extracted_data(extracted_data)
    analysis_df.to_csv(str(output_dir / "dissertation_analysis.csv"), index=False)
    
    builder.export_dataset(str(output_dir / "dataset"))
    
    print("\n" + "=" * 70)
    print("  ANALYSIS COMPLETE")
    print("=" * 70)
    
    print(f"\n{'DISSERTATION SUMMARY':^70}")
    print("-" * 70)
    print(f"  Total Pages:              {summary['total_pages']}")
    print(f"  Tables Found:             {summary['tables_count']}")
    print(f"  Figures Found:            {summary['figures_count']}")
    print(f"  ML Features Mentioned:    {summary['ml_features_found']}")
    
    print(f"\n{'KEYWORD ANALYSIS':^70}")
    print("-" * 70)
    for category, data in summary['keyword_analysis'].items():
        category_display = category.replace('_', ' ').title()
        print(f"  {category_display:25} {data['count']:5} occurrences ({len(data['pages']):3} pages)")
    
    print(f"\n{'CHAPTERS FOUND':^70}")
    print("-" * 70)
    for ch in chapters[:15]:
        title = ch['title'][:50] + "..." if len(ch['title']) > 50 else ch['title']
        print(f"  Chapter {ch['chapter_number']:3}: {title}")
    
    if not analysis_df.empty:
        print(f"\n{'ML FEATURE EXTRACTION':^70}")
        print("-" * 70)
        print(f"  Total Feature Instances:  {len(analysis_df)}")
        print(f"  Unique Features Found:    {analysis_df['feature_name'].nunique()}")
        print(f"\n  Feature Distribution:")
        feature_counts = analysis_df['feature_name'].value_counts().head(10)
        for feature, count in feature_counts.items():
            print(f"    - {feature:20} {count:5} instances")
    
    print(f"\n{'OUTPUT FILES':^70}")
    print("-" * 70)
    print(f"  Extracted Text:     {output_dir / 'dissertation_extracted.json'}")
    print(f"  Pages CSV:          {output_dir / 'dissertation_pages.csv'}")
    print(f"  Analysis CSV:       {output_dir / 'dissertation_analysis.csv'}")
    print(f"  Dataset Schema:     {output_dir / 'dataset' / 'schema.json'}")
    print(f"  Feature Catalog:    {output_dir / 'dataset' / 'feature_catalog.csv'}")
    
    print(f"\n{'SAMPLE CONTENT':^70}")
    print("-" * 70)
    if summary.get('tables_and_figures'):
        print("\n  Sample Tables/Figures:")
        for item in summary['tables_and_figures'][:5]:
            print(f"    {item['type'].title()} {item['number']}: {item['caption'][:60]}")
    
    extractor.close()
    
    print("\n" + "=" * 70)
    print("  Analysis complete! Check the 'output' folder for results.")
    print("=" * 70)


if __name__ == "__main__":
    main()
