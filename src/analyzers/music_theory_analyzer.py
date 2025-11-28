#!/usr/bin/env python3
"""
Music Theory Analyzer
====================
Focused analysis of notes, scales, and music theory elements
from the Thai-Jazz dissertation dataset.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import re


class MusicTheoryAnalyzer:
    """Analyze music theory elements: notes, scales, modes."""

    def __init__(self, data_dir: str = "output"):
        self.data_dir = Path(data_dir)
        self.extracted_data = self._load_extracted_data()
        self.analysis_df = self._load_analysis()

    def _load_extracted_data(self) -> Dict:
        """Load extracted dissertation data."""
        json_path = self.data_dir / "dissertation_extracted.json"
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_analysis(self) -> pd.DataFrame:
        """Load analysis CSV."""
        csv_path = self.data_dir / "dissertation_analysis.csv"
        if csv_path.exists():
            return pd.read_csv(csv_path)
        return pd.DataFrame()

    def extract_scale_references(self) -> pd.DataFrame:
        """Extract all scale references from the text."""
        scale_patterns = {
            'pentatonic': r'pentatonic',
            'heptatonic': r'heptatonic',
            'chromatic': r'chromatic',
            'diatonic': r'diatonic',
            'modal': r'modal|mode[s]?',
            'major': r'major\s+scale',
            'minor': r'minor\s+scale',
            'dorian': r'dorian',
            'phrygian': r'phrygian',
            'lydian': r'lydian',
            'mixolydian': r'mixolydian',
            'aeolian': r'aeolian',
            'locrian': r'locrian',
            'whole_tone': r'whole\s+tone',
            'diminished': r'diminished\s+scale',
            'blues': r'blues\s+scale',
            'bebop': r'bebop\s+scale',
            'thai_mode': r'thang|ทาง|thai\s+mode',
            'lai': r'lai\s+\w+',
        }

        results = []
        for page_num, text in self.extracted_data.get('extracted_text', {}).items():
            for scale_name, pattern in scale_patterns.items():
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    context = self._get_context(text, match.start(), 100)
                    results.append({
                        'page': int(page_num),
                        'scale_type': scale_name,
                        'match': match.group(0),
                        'context': context
                    })

        return pd.DataFrame(results)

    def extract_note_references(self) -> pd.DataFrame:
        """Extract musical note references."""
        note_patterns = {
            'pitch_class': r'\b[A-G][#♯b♭]?\b',
            'solfege': r'\bdo|re|mi|fa|sol|la|ti\b',
            'degree': r'\b[1-7][\^°]\b',
            'interval': r'(major|minor|perfect|augmented|diminished)\s+(second|third|fourth|fifth|sixth|seventh|octave)',
        }

        results = []
        for page_num, text in self.extracted_data.get('extracted_text', {}).items():
            # Look for note sequences (e.g., "A, C, D, E, G")
            note_seq_pattern = r'([A-G][#♯b♭]?,\s*){2,}[A-G][#♯b♭]?'
            matches = re.finditer(note_seq_pattern, text)
            for match in matches:
                results.append({
                    'page': int(page_num),
                    'type': 'note_sequence',
                    'content': match.group(0),
                    'context': self._get_context(text, match.start(), 80)
                })

        return pd.DataFrame(results)

    def extract_tuning_systems(self) -> pd.DataFrame:
        """Extract tuning system references."""
        results = []
        tuning_pattern = r'([A-G][#♯b♭]?-){1,}[A-G][#♯b♭]?'

        for page_num, text in self.extracted_data.get('extracted_text', {}).items():
            matches = re.finditer(tuning_pattern, text)
            for match in matches:
                results.append({
                    'page': int(page_num),
                    'tuning': match.group(0),
                    'context': self._get_context(text, match.start(), 100)
                })

        return pd.DataFrame(results)

    def get_thai_scales(self) -> pd.DataFrame:
        """Get Thai scale information from phin dataset."""
        phin_lai_path = self.data_dir / "phin_dataset" / "phin_lai_patterns.json"
        if phin_lai_path.exists():
            with open(phin_lai_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        return pd.DataFrame()

    def get_jazz_scales(self) -> List[str]:
        """Get Jazz scales from schema."""
        schema_path = self.data_dir / "dataset" / "schema.json"
        if schema_path.exists():
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            jazz_features = schema.get('categories', {}).get('jazz_modern', {}).get('features', [])
            return jazz_features
        return []

    def analyze_scale_distribution(self) -> Dict[str, int]:
        """Analyze distribution of scale types mentioned."""
        scale_df = self.extract_scale_references()
        if not scale_df.empty:
            return scale_df['scale_type'].value_counts().to_dict()
        return {}

    def find_pages_with_scales(self, scale_type: str) -> pd.DataFrame:
        """Find all pages mentioning a specific scale type."""
        scale_df = self.extract_scale_references()
        if not scale_df.empty:
            return scale_df[scale_df['scale_type'].str.contains(scale_type, case=False, na=False)]
        return pd.DataFrame()

    def _get_context(self, text: str, position: int, context_size: int = 100) -> str:
        """Extract context around a position."""
        start = max(0, position - context_size)
        end = min(len(text), position + context_size)
        context = text[start:end].replace('\n', ' ').strip()
        return context

    def generate_music_theory_report(self) -> Dict[str, Any]:
        """Generate comprehensive music theory report."""
        scales = self.extract_scale_references()
        notes = self.extract_note_references()
        tunings = self.extract_tuning_systems()
        thai_scales = self.get_thai_scales()

        report = {
            'total_scale_mentions': len(scales),
            'unique_scale_types': scales['scale_type'].nunique() if not scales.empty else 0,
            'scale_distribution': self.analyze_scale_distribution(),
            'total_note_sequences': len(notes),
            'total_tuning_systems': len(tunings),
            'thai_lai_patterns': len(thai_scales),
            'pages_with_scales': sorted(scales['page'].unique().tolist()) if not scales.empty else [],
            'most_common_scales': scales['scale_type'].value_counts().head(10).to_dict() if not scales.empty else {}
        }

        return report

    def extract_note_sequences(self) -> pd.DataFrame:
        """Extract note sequences and melodic patterns."""
        results = []

        for page_num, text in self.extracted_data.get('extracted_text', {}).items():
            # Skip if not a valid page number
            if not str(page_num).isdigit():
                continue

            # Pattern 1: Basic note sequences (A, B, C, D...)
            note_seq_pattern = r'[A-G][#♯b♭]?(?:,\s*[A-G][#♯b♭]?){2,}'
            matches = re.finditer(note_seq_pattern, text)
            for match in matches:
                results.append({
                    'page': int(page_num),
                    'type': 'note_sequence',
                    'content': match.group(0),
                    'context': self._get_context(text, match.start(), 80)
                })

            # Pattern 2: Thai lai patterns (ลาย)
            lai_pattern = r'lai\s+\w+.*?(?:consisting of|pitches).*?([A-G][#♯b♭]?(?:,\s*[A-G][#♯b♭]?)+)'
            matches = re.finditer(lai_pattern, text, re.IGNORECASE)
            for match in matches:
                results.append({
                    'page': int(page_num),
                    'type': 'lai_pattern',
                    'content': match.group(1) if match.groups() else match.group(0),
                    'context': self._get_context(text, match.start(), 120)
                })

            # Pattern 3: Scale degree patterns (1 2 3 5, etc.)
            scale_degree_pattern = r'(?:♭?[1-7][-­¯]?\s*){3,}'
            matches = re.finditer(scale_degree_pattern, text)
            for match in matches:
                if any(c.isdigit() for c in match.group(0)):
                    results.append({
                        'page': int(page_num),
                        'type': 'scale_degrees',
                        'content': match.group(0).strip(),
                        'context': self._get_context(text, match.start(), 80)
                    })

        return pd.DataFrame(results)


def main():
    """Run music theory analysis."""
    print("=" * 70)
    print("MUSIC THEORY ANALYZER")
    print("Focus: Notes, Scales, and Music Theory")
    print("=" * 70)

    analyzer = MusicTheoryAnalyzer()

    # Generate report
    print("\nGenerating music theory report...")
    report = analyzer.generate_music_theory_report()

    print("\n" + "=" * 70)
    print("MUSIC THEORY SUMMARY")
    print("=" * 70)
    print(f"Total Scale Mentions: {report['total_scale_mentions']}")
    print(f"Unique Scale Types: {report['unique_scale_types']}")
    print(f"Note Sequences Found: {report['total_note_sequences']}")
    print(f"Tuning Systems Found: {report['total_tuning_systems']}")
    print(f"Thai Lai Patterns: {report['thai_lai_patterns']}")

    print("\n" + "=" * 70)
    print("MOST COMMON SCALES")
    print("=" * 70)
    for scale, count in report['most_common_scales'].items():
        print(f"  {scale:20} {count:5} mentions")

    # Extract and save detailed data
    print("\nExtracting detailed scale data...")
    scales_df = analyzer.extract_scale_references()
    scales_df.to_csv('output/scale_analysis.csv', index=False)
    print(f"Saved to: output/scale_analysis.csv ({len(scales_df)} entries)")

    print("\nExtracting note sequences...")
    notes_df = analyzer.extract_note_sequences()
    notes_df.to_csv('output/note_sequences.csv', index=False)
    print(f"Saved to: output/note_sequences.csv ({len(notes_df)} entries)")

    print("\nExtracting tuning systems...")
    tunings_df = analyzer.extract_tuning_systems()
    tunings_df.to_csv('output/tuning_systems.csv', index=False)
    print(f"Saved to: output/tuning_systems.csv ({len(tunings_df)} entries)")

    # Show Thai scale examples
    print("\n" + "=" * 70)
    print("THAI LAI PATTERNS (SCALES)")
    print("=" * 70)
    thai_scales = analyzer.get_thai_scales()
    if not thai_scales.empty:
        for _, row in thai_scales.iterrows():
            print(f"\n{row['name_english']} ({row['name_thai']})")
            print(f"  Scale: {row['scale_type']}")
            print(f"  Meaning: {row['meaning']}")
            if row['drone_note']:
                print(f"  Drone: {row['drone_note']}")

    print("\n" + "=" * 70)
    print("Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()