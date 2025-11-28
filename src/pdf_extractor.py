import fitz
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd


class DissertationExtractor:
    """Extract and analyze PhD dissertation on cross-cultural music ML dataset."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.doc = fitz.open(str(self.pdf_path))
        self.total_pages = len(self.doc)
        self.extracted_text: Dict[int, str] = {}
        self.chapters: List[Dict] = []
        self.music_features: List[Dict] = []
        
    def extract_all_text(self, progress_callback=None) -> Dict[int, str]:
        """Extract text from all pages."""
        for page_num in range(self.total_pages):
            page = self.doc[page_num]
            text = page.get_text("text")
            self.extracted_text[page_num + 1] = text
            
            if progress_callback:
                progress_callback(page_num + 1, self.total_pages)
                
        return self.extracted_text
    
    def extract_page_range(self, start: int, end: int) -> Dict[int, str]:
        """Extract text from a specific page range."""
        result = {}
        for page_num in range(start - 1, min(end, self.total_pages)):
            page = self.doc[page_num]
            text = page.get_text("text")
            result[page_num + 1] = text
            self.extracted_text[page_num + 1] = text
        return result
    
    def identify_chapters(self) -> List[Dict]:
        """Identify chapter structure from extracted text."""
        chapter_patterns = [
            r'(?:Chapter|CHAPTER|บทที่)\s*(\d+)[:\s]*(.+?)(?:\n|$)',
            r'^(\d+)\.\s+(.+?)(?:\n|$)',
        ]
        
        chapters = []
        for page_num, text in self.extracted_text.items():
            for pattern in chapter_patterns:
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    chapter_num = match.group(1)
                    chapter_title = match.group(2).strip()
                    chapters.append({
                        'chapter_number': chapter_num,
                        'title': chapter_title,
                        'start_page': page_num,
                        'raw_match': match.group(0)
                    })
        
        self.chapters = self._deduplicate_chapters(chapters)
        return self.chapters
    
    def _deduplicate_chapters(self, chapters: List[Dict]) -> List[Dict]:
        """Remove duplicate chapter entries."""
        seen = set()
        unique_chapters = []
        for ch in chapters:
            key = (ch['chapter_number'], ch['title'][:50])
            if key not in seen:
                seen.add(key)
                unique_chapters.append(ch)
        return sorted(unique_chapters, key=lambda x: int(x['chapter_number']) if x['chapter_number'].isdigit() else 0)
    
    def find_music_keywords(self) -> Dict[str, List[Dict]]:
        """Find pages containing music-related keywords."""
        keywords = {
            'thai_music': [
                'ดนตรีไทย', 'Thai music', 'traditional Thai',
                'piphat', 'ปี่พาทย์', 'mahori', 'มโหรี',
                'khong wong', 'ฆ้องวง', 'ranat', 'ระนาด',
                'thang', 'ทาง', 'เพลงไทย', 'Thai melody',
                'pentatonic', 'heptatonic', 'Thai scale'
            ],
            'jazz': [
                'jazz', 'แจ๊ส', 'improvisation', 'swing',
                'bebop', 'modal jazz', 'fusion', 'chord progression',
                'jazz harmony', 'blue notes', 'jazz scale',
                'syncopation', 'jazz rhythm'
            ],
            'cross_cultural': [
                'cross-cultural', 'ข้ามวัฒนธรรม', 'fusion',
                'hybrid', 'intercultural', 'blending',
                'integration', 'combination', 'synthesis',
                'transcultural', 'multicultural'
            ],
            'ml_dataset': [
                'machine learning', 'dataset', 'feature',
                'training', 'classification', 'neural network',
                'deep learning', 'audio feature', 'MFCC',
                'spectrogram', 'pitch', 'rhythm feature',
                'annotation', 'labeling', 'ground truth'
            ],
            'music_theory': [
                'melody', 'harmony', 'rhythm', 'tempo',
                'scale', 'mode', 'interval', 'chord',
                'timbre', 'dynamics', 'articulation',
                'phrase', 'motif', 'structure'
            ]
        }
        
        results = {category: [] for category in keywords}
        
        for page_num, text in self.extracted_text.items():
            text_lower = text.lower()
            for category, keyword_list in keywords.items():
                for keyword in keyword_list:
                    if keyword.lower() in text_lower:
                        results[category].append({
                            'page': page_num,
                            'keyword': keyword,
                            'context': self._get_keyword_context(text, keyword)
                        })
                        break
        
        return results
    
    def _get_keyword_context(self, text: str, keyword: str, context_chars: int = 200) -> str:
        """Get surrounding context for a keyword."""
        idx = text.lower().find(keyword.lower())
        if idx == -1:
            return ""
        
        start = max(0, idx - context_chars)
        end = min(len(text), idx + len(keyword) + context_chars)
        context = text[start:end].replace('\n', ' ').strip()
        
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."
            
        return context
    
    def extract_tables_and_figures(self) -> List[Dict]:
        """Identify tables and figures in the document."""
        patterns = [
            r'(?:Table|ตาราง)\s*(\d+[\.\d]*)[:\s]*(.+?)(?:\n|$)',
            r'(?:Figure|Fig\.|รูป|ภาพ)\s*(\d+[\.\d]*)[:\s]*(.+?)(?:\n|$)',
        ]
        
        items = []
        for page_num, text in self.extracted_text.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    item_type = 'table' if 'table' in match.group(0).lower() or 'ตาราง' in match.group(0) else 'figure'
                    items.append({
                        'type': item_type,
                        'number': match.group(1),
                        'caption': match.group(2).strip()[:200],
                        'page': page_num
                    })
        
        return items
    
    def extract_dataset_features(self) -> List[Dict]:
        """Extract ML dataset feature descriptions from the text."""
        feature_patterns = [
            r'feature[s]?\s*(?:include|are|:)\s*(.+?)(?:\.|$)',
            r'(?:audio|music)\s*feature[s]?\s*(?:such as|like|:)\s*(.+?)(?:\.|$)',
            r'(?:extract|compute|calculate)\s*(?:the\s+)?(?:following\s+)?feature[s]?\s*(.+?)(?:\.|$)',
        ]
        
        features = []
        for page_num, text in self.extracted_text.items():
            for pattern in feature_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    features.append({
                        'description': match.group(1).strip()[:300],
                        'page': page_num,
                        'raw_match': match.group(0)[:200]
                    })
        
        self.music_features = features
        return features
    
    def generate_summary_report(self) -> Dict:
        """Generate a comprehensive summary of the dissertation."""
        keyword_analysis = self.find_music_keywords()
        tables_figures = self.extract_tables_and_figures()
        features = self.extract_dataset_features()
        
        summary = {
            'total_pages': self.total_pages,
            'chapters': self.chapters,
            'keyword_analysis': {
                category: {
                    'count': len(items),
                    'pages': list(set(item['page'] for item in items))
                }
                for category, items in keyword_analysis.items()
            },
            'tables_count': len([t for t in tables_figures if t['type'] == 'table']),
            'figures_count': len([t for t in tables_figures if t['type'] == 'figure']),
            'ml_features_found': len(features),
            'tables_and_figures': tables_figures[:20],
            'sample_features': features[:10]
        }
        
        return summary
    
    def export_to_json(self, output_path: str):
        """Export all extracted data to JSON."""
        data = {
            'metadata': {
                'source_file': str(self.pdf_path),
                'total_pages': self.total_pages
            },
            'chapters': self.chapters,
            'extracted_text': self.extracted_text,
            'music_features': self.music_features
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """Convert extracted text to pandas DataFrame."""
        rows = []
        for page_num, text in self.extracted_text.items():
            rows.append({
                'page': page_num,
                'text': text,
                'word_count': len(text.split()),
                'char_count': len(text)
            })
        
        return pd.DataFrame(rows)
    
    def close(self):
        """Close the PDF document."""
        self.doc.close()


def print_progress(current: int, total: int):
    """Print extraction progress."""
    percent = (current / total) * 100
    bar_length = 40
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rExtracting: |{bar}| {percent:.1f}% ({current}/{total} pages)', end='', flush=True)
    if current == total:
        print()


if __name__ == "__main__":
    pdf_path = "attached_assets/Tanarat Chaichana - PhD Dissertation [complete] 14_04_2022_1764338380212.pdf"
    
    print("=" * 60)
    print("PhD Dissertation Extractor - Cross-Cultural Music ML Dataset")
    print("=" * 60)
    
    extractor = DissertationExtractor(pdf_path)
    print(f"\nPDF loaded: {extractor.total_pages} pages")
    
    print("\nExtracting text from all pages...")
    extractor.extract_all_text(progress_callback=print_progress)
    
    print("\nIdentifying chapters...")
    chapters = extractor.identify_chapters()
    print(f"Found {len(chapters)} chapters")
    
    print("\nGenerating summary report...")
    summary = extractor.generate_summary_report()
    
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total pages: {summary['total_pages']}")
    print(f"Tables found: {summary['tables_count']}")
    print(f"Figures found: {summary['figures_count']}")
    print(f"ML features mentioned: {summary['ml_features_found']}")
    
    print("\nKeyword Analysis:")
    for category, data in summary['keyword_analysis'].items():
        print(f"  - {category}: {data['count']} occurrences across {len(data['pages'])} pages")
    
    print("\nChapters found:")
    for ch in chapters[:10]:
        print(f"  Chapter {ch['chapter_number']}: {ch['title'][:60]}")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    extractor.export_to_json(str(output_dir / "dissertation_extracted.json"))
    print(f"\nExported to: {output_dir / 'dissertation_extracted.json'}")
    
    df = extractor.export_to_dataframe()
    df.to_csv(str(output_dir / "dissertation_pages.csv"), index=False)
    print(f"Exported to: {output_dir / 'dissertation_pages.csv'}")
    
    extractor.close()
    print("\nExtraction complete!")
