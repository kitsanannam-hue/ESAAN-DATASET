#!/usr/bin/env python3
"""
Interactive Dataset Explorer for Thai-Jazz Cross-Cultural Music Dataset
========================================================================
Provides tools to explore, query, and analyze the extracted dissertation data.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any


class DatasetExplorer:
    """Interactive explorer for the Thai-Jazz music dataset."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.extracted_data: Optional[Dict] = None
        self.pages_df: Optional[pd.DataFrame] = None
        self.analysis_df: Optional[pd.DataFrame] = None
        self.feature_catalog: Optional[pd.DataFrame] = None
        self.schema: Optional[Dict] = None
        
        self._load_data()
    
    def _load_data(self):
        """Load all dataset components."""
        extracted_path = self.output_dir / "dissertation_extracted.json"
        if extracted_path.exists():
            with open(extracted_path, 'r', encoding='utf-8') as f:
                self.extracted_data = json.load(f)
        
        pages_path = self.output_dir / "dissertation_pages.csv"
        if pages_path.exists():
            self.pages_df = pd.read_csv(pages_path)
        
        analysis_path = self.output_dir / "dissertation_analysis.csv"
        if analysis_path.exists():
            self.analysis_df = pd.read_csv(analysis_path)
        
        catalog_path = self.output_dir / "dataset" / "feature_catalog.csv"
        if catalog_path.exists():
            self.feature_catalog = pd.read_csv(catalog_path)
        
        schema_path = self.output_dir / "dataset" / "schema.json"
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
    
    def get_page_content(self, page_num: int) -> str:
        """Get the text content of a specific page."""
        if self.extracted_data and 'extracted_text' in self.extracted_data:
            return self.extracted_data['extracted_text'].get(str(page_num), "Page not found")
        return "No extracted data available"
    
    def search_content(self, query: str, case_sensitive: bool = False) -> List[Dict]:
        """Search for text across all pages."""
        results = []
        if not self.extracted_data or 'extracted_text' not in self.extracted_data:
            return results
        
        for page_num, text in self.extracted_data['extracted_text'].items():
            search_text = text if case_sensitive else text.lower()
            search_query = query if case_sensitive else query.lower()
            
            if search_query in search_text:
                idx = search_text.find(search_query)
                start = max(0, idx - 100)
                end = min(len(text), idx + len(query) + 100)
                context = text[start:end].replace('\n', ' ').strip()
                
                results.append({
                    'page': int(page_num),
                    'context': f"...{context}..."
                })
        
        return sorted(results, key=lambda x: x['page'])
    
    def get_pages_with_feature(self, feature_name: str) -> pd.DataFrame:
        """Get all pages containing a specific music feature."""
        if self.analysis_df is None:
            return pd.DataFrame()
        
        return self.analysis_df[self.analysis_df['feature_name'] == feature_name]
    
    def get_thai_music_pages(self) -> pd.DataFrame:
        """Get all pages containing Thai music content."""
        if self.analysis_df is None:
            return pd.DataFrame()
        
        return self.analysis_df[self.analysis_df['has_thai_music'] == True]
    
    def get_jazz_pages(self) -> pd.DataFrame:
        """Get all pages containing Jazz content."""
        if self.analysis_df is None:
            return pd.DataFrame()
        
        return self.analysis_df[self.analysis_df['has_jazz'] == True]
    
    def get_fusion_pages(self) -> pd.DataFrame:
        """Get all pages containing cross-cultural fusion content."""
        if self.analysis_df is None:
            return pd.DataFrame()
        
        return self.analysis_df[self.analysis_df['has_fusion'] == True]
    
    def get_ml_pages(self) -> pd.DataFrame:
        """Get all pages containing ML-related content."""
        if self.analysis_df is None:
            return pd.DataFrame()
        
        return self.analysis_df[self.analysis_df['has_ml_terms'] == True]
    
    def get_feature_statistics(self) -> Dict[str, Any]:
        """Get statistics about features in the dataset."""
        if self.analysis_df is None:
            return {}
        
        stats = {
            'total_entries': len(self.analysis_df),
            'unique_pages': self.analysis_df['page'].nunique(),
            'feature_counts': self.analysis_df['feature_name'].value_counts().to_dict(),
            'thai_music_count': self.analysis_df['has_thai_music'].sum(),
            'jazz_count': self.analysis_df['has_jazz'].sum(),
            'fusion_count': self.analysis_df['has_fusion'].sum(),
            'ml_count': self.analysis_df['has_ml_terms'].sum()
        }
        
        return stats
    
    def get_chapter_info(self) -> List[Dict]:
        """Get information about chapters in the dissertation."""
        if self.extracted_data and 'chapters' in self.extracted_data:
            return self.extracted_data['chapters']
        return []
    
    def get_feature_catalog(self) -> pd.DataFrame:
        """Get the feature catalog for ML dataset."""
        if self.feature_catalog is not None:
            return self.feature_catalog
        return pd.DataFrame()
    
    def get_schema(self) -> Dict:
        """Get the ML dataset schema."""
        return self.schema or {}
    
    def export_subset(self, pages: List[int], output_path: str):
        """Export a subset of pages to a new JSON file."""
        if not self.extracted_data:
            return
        
        subset = {
            'metadata': self.extracted_data.get('metadata', {}),
            'pages': {str(p): self.extracted_data['extracted_text'].get(str(p), '') 
                     for p in pages if str(p) in self.extracted_data.get('extracted_text', {})}
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(subset, f, ensure_ascii=False, indent=2)
    
    def get_thang_references(self) -> List[Dict]:
        """Find all references to Thai 'thang' (modes) in the text."""
        thang_keywords = [
            'thang nai', 'thang klang', 'thang phiang o',
            'thang kruad', 'thang chawa', 'ทางใน', 'ทางกลาง',
            'thang', 'ทาง'
        ]
        
        results = []
        for keyword in thang_keywords:
            matches = self.search_content(keyword)
            for match in matches:
                match['keyword'] = keyword
                results.append(match)
        
        return results
    
    def get_improvisation_examples(self) -> pd.DataFrame:
        """Get pages discussing improvisation techniques."""
        return self.get_pages_with_feature('improvisation')
    
    def summary(self) -> str:
        """Generate a text summary of the dataset."""
        stats = self.get_feature_statistics()
        
        summary_lines = [
            "=" * 60,
            "THAI-JAZZ CROSS-CULTURAL MUSIC DATASET SUMMARY",
            "=" * 60,
            "",
            f"Total Feature Entries: {stats.get('total_entries', 0)}",
            f"Unique Pages Analyzed: {stats.get('unique_pages', 0)}",
            "",
            "Content Distribution:",
            f"  - Thai Music: {stats.get('thai_music_count', 0)} pages",
            f"  - Jazz: {stats.get('jazz_count', 0)} pages",
            f"  - Cross-Cultural Fusion: {stats.get('fusion_count', 0)} pages",
            f"  - ML Related: {stats.get('ml_count', 0)} pages",
            "",
            "Feature Distribution:"
        ]
        
        for feature, count in stats.get('feature_counts', {}).items():
            summary_lines.append(f"  - {feature}: {count} instances")
        
        summary_lines.extend([
            "",
            "=" * 60
        ])
        
        return "\n".join(summary_lines)


def interactive_menu():
    """Run an interactive menu for exploring the dataset."""
    explorer = DatasetExplorer()
    
    while True:
        print("\n" + "=" * 60)
        print("THAI-JAZZ MUSIC DATASET EXPLORER")
        print("=" * 60)
        print("\n1. View Dataset Summary")
        print("2. Search Content")
        print("3. View Page Content")
        print("4. List Thai Music Pages")
        print("5. List Jazz Pages")
        print("6. List Fusion Pages")
        print("7. View Feature Catalog")
        print("8. View ML Dataset Schema")
        print("9. Find Thang (Thai Mode) References")
        print("10. View Improvisation Examples")
        print("0. Exit")
        
        choice = input("\nEnter choice (0-10): ").strip()
        
        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            print(explorer.summary())
        elif choice == "2":
            query = input("Enter search query: ").strip()
            if query:
                results = explorer.search_content(query)
                print(f"\nFound {len(results)} results:")
                for r in results[:10]:
                    print(f"\n  Page {r['page']}: {r['context'][:150]}...")
        elif choice == "3":
            try:
                page_num = int(input("Enter page number: ").strip())
                content = explorer.get_page_content(page_num)
                print(f"\n--- Page {page_num} ---")
                print(content[:2000] + "..." if len(content) > 2000 else content)
            except ValueError:
                print("Invalid page number")
        elif choice == "4":
            df = explorer.get_thai_music_pages()
            print(f"\nPages with Thai music content: {len(df)}")
            if not df.empty:
                print(df[['page', 'feature_name', 'context']].head(10).to_string())
        elif choice == "5":
            df = explorer.get_jazz_pages()
            print(f"\nPages with Jazz content: {len(df)}")
            if not df.empty:
                print(df[['page', 'feature_name', 'context']].head(10).to_string())
        elif choice == "6":
            df = explorer.get_fusion_pages()
            print(f"\nPages with fusion content: {len(df)}")
            if not df.empty:
                print(df[['page', 'feature_name', 'context']].head(10).to_string())
        elif choice == "7":
            catalog = explorer.get_feature_catalog()
            if not catalog.empty:
                print("\nFeature Catalog:")
                print(catalog.to_string())
        elif choice == "8":
            schema = explorer.get_schema()
            print("\nML Dataset Schema:")
            print(json.dumps(schema, indent=2, ensure_ascii=False))
        elif choice == "9":
            results = explorer.get_thang_references()
            print(f"\nFound {len(results)} thang references:")
            for r in results[:10]:
                print(f"  Page {r['page']} ({r['keyword']}): {r['context'][:100]}...")
        elif choice == "10":
            df = explorer.get_improvisation_examples()
            print(f"\nImprovisation examples: {len(df)}")
            if not df.empty:
                print(df[['page', 'context']].head(10).to_string())
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("Loading Thai-Jazz Music Dataset Explorer...")
    explorer = DatasetExplorer()
    print(explorer.summary())
    
    print("\n\nTo run interactive mode, use: python src/dataset_explorer.py --interactive")
    print("\nOr import and use programmatically:")
    print("  from dataset_explorer import DatasetExplorer")
    print("  explorer = DatasetExplorer()")
    print("  results = explorer.search_content('improvisation')")
