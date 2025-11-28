
#!/usr/bin/env python3
"""
Music Notation Extractor
========================
Extract and analyze musical notation from Thai-Jazz dissertation.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import re


class MusicNotationExtractor:
    """Extract musical notation and patterns from dissertation."""
    
    def __init__(self, data_dir: str = "output"):
        self.data_dir = Path(data_dir)
        self.extracted_data = self._load_extracted_data()
        
    def _load_extracted_data(self) -> Dict:
        """Load extracted dissertation data."""
        json_path = self.data_dir / "dissertation_extracted.json"
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _get_context(self, text: str, position: int, window: int = 100) -> str:
        """Get surrounding context for a match."""
        start = max(0, position - window)
        end = min(len(text), position + window)
        context = text[start:end].replace('\n', ' ').strip()
        return context
    
    def extract_all_music_notes(self) -> pd.DataFrame:
        """Extract all types of musical notation."""
        results = []
        
        for page_num, text in self.extracted_data.get('extracted_text', {}).items():
            if not str(page_num).isdigit():
                continue
            
            page_num = int(page_num)
            
            # 1. Note sequences (A, B, C, D, E)
            note_seq = r'[A-G][#♯b♭]?(?:,\s*[A-G][#♯b♭]?){2,}'
            for match in re.finditer(note_seq, text):
                results.append({
                    'page': page_num,
                    'type': 'western_notes',
                    'notation': match.group(0),
                    'context': self._get_context(text, match.start())
                })
            
            # 2. Thai scale degrees (1 2 3 5 6, etc.)
            scale_deg = r'\b([1-7][\s,]+){2,}[1-7]\b'
            for match in re.finditer(scale_deg, text):
                results.append({
                    'page': page_num,
                    'type': 'scale_degrees',
                    'notation': match.group(0),
                    'context': self._get_context(text, match.start())
                })
            
            # 3. Thai lai modes
            lai_pattern = r'(lai\s+\w+).*?([A-G][#♯b♭]?(?:,\s*[A-G][#♯b♭]?)+)'
            for match in re.finditer(lai_pattern, text, re.IGNORECASE):
                results.append({
                    'page': page_num,
                    'type': 'lai_mode',
                    'notation': match.group(2),
                    'context': match.group(0)
                })
            
            # 4. Chord progressions
            chord_prog = r'[A-G][#♯b♭]?(?:maj|min|m|M|dim|aug|sus|add)?[0-9]?(?:\s*-\s*[A-G][#♯b♭]?(?:maj|min|m|M|dim|aug|sus|add)?[0-9]?){2,}'
            for match in re.finditer(chord_prog, text):
                if 'Figure' not in match.group(0):  # Skip figure references
                    results.append({
                        'page': page_num,
                        'type': 'chord_progression',
                        'notation': match.group(0),
                        'context': self._get_context(text, match.start())
                    })
            
            # 5. Musical intervals
            interval_pattern = r'(?:P[145]|M[2367]|m[2367]|A[1-7]|d[1-7])'
            for match in re.finditer(interval_pattern, text):
                results.append({
                    'page': page_num,
                    'type': 'interval',
                    'notation': match.group(0),
                    'context': self._get_context(text, match.start(), 60)
                })
        
        return pd.DataFrame(results)
    
    def extract_musical_compositions(self) -> pd.DataFrame:
        """Extract composition titles and their musical details."""
        results = []
        
        for page_num, text in self.extracted_data.get('extracted_text', {}).items():
            if not str(page_num).isdigit():
                continue
            
            # Look for quoted composition titles
            comp_pattern = r'["""]([^"""]+)["""]'
            for match in re.finditer(comp_pattern, text):
                title = match.group(1)
                # Filter out non-musical titles
                if len(title) < 50 and any(keyword in text[max(0, match.start()-200):match.end()+200].lower() 
                                          for keyword in ['composition', 'piece', 'song', 'melody', 'lai', 'phleng']):
                    results.append({
                        'page': int(page_num),
                        'title': title,
                        'context': self._get_context(text, match.start(), 150)
                    })
        
        return pd.DataFrame(results)
    
    def export_notation_dataset(self, output_path: str = None):
        """Export complete notation dataset."""
        if output_path is None:
            output_path = self.data_dir / "music_notation_dataset"
        
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Extract all notation
        notation_df = self.extract_all_music_notes()
        compositions_df = self.extract_musical_compositions()
        
        # Save to CSV and JSON
        notation_df.to_csv(output_path / "musical_notation.csv", index=False)
        notation_df.to_json(output_path / "musical_notation.json", 
                           orient='records', force_ascii=False, indent=2)
        
        compositions_df.to_csv(output_path / "compositions.csv", index=False)
        compositions_df.to_json(output_path / "compositions.json",
                               orient='records', force_ascii=False, indent=2)
        
        # Create summary
        summary = {
            'total_notations': len(notation_df),
            'by_type': notation_df['type'].value_counts().to_dict() if 'type' in notation_df.columns else {},
            'total_compositions': len(compositions_df),
            'pages_with_notation': len(notation_df['page'].unique()) if 'page' in notation_df.columns else 0
        }
        
        with open(output_path / "notation_summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*70}")
        print("Musical Notation Dataset Exported")
        print(f"{'='*70}")
        print(f"\nOutput directory: {output_path}")
        print(f"\nNotations extracted: {len(notation_df)}")
        print(f"  - Western notes: {summary['by_type'].get('western_notes', 0)}")
        print(f"  - Scale degrees: {summary['by_type'].get('scale_degrees', 0)}")
        print(f"  - Lai modes: {summary['by_type'].get('lai_mode', 0)}")
        print(f"  - Chord progressions: {summary['by_type'].get('chord_progression', 0)}")
        print(f"  - Intervals: {summary['by_type'].get('interval', 0)}")
        print(f"\nCompositions found: {len(compositions_df)}")
        print(f"Pages with notation: {summary['pages_with_notation']}")
        print(f"\n{'='*70}")
        
        return notation_df, compositions_df


if __name__ == "__main__":
    extractor = MusicNotationExtractor()
    notation_df, compositions_df = extractor.export_notation_dataset()
    
    print("\nSample notations:")
    print(notation_df.head(10).to_string(index=False))
