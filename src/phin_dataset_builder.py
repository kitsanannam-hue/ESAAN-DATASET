#!/usr/bin/env python3
"""
Phin Dataset Builder
====================
Specialized dataset for Thai Phin (พิณ) instrument research.
Extracts tuning systems, lai patterns, techniques, and artist information.
"""

import json
import re
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class PhinTuning:
    """Phin tuning configuration."""
    string_count: int
    tuning: str
    notes: List[str]
    description: str = ""
    region: str = ""


@dataclass
class LaiPattern:
    """Lai (melodic pattern) for Phin."""
    name_thai: str
    name_english: str
    meaning: str
    scale_type: str
    drone_note: str = ""
    source_page: int = 0
    performer: str = ""
    province: str = ""
    characteristics: List[str] = None


@dataclass
class PhinArtist:
    """Phin master/performer information."""
    name: str
    province: str
    specialty: str
    description: str
    notable_works: List[str] = None
    source_page: int = 0


@dataclass
class PhinTechnique:
    """Phin playing technique."""
    name: str
    description: str
    category: str
    source_page: int = 0


class PhinDatasetBuilder:
    """Build comprehensive dataset for Phin instrument."""
    
    PHIN_TUNING_SYSTEMS = {
        '3_string': [
            {'tuning': 'E-A-E', 'notes': ['E', 'A', 'E'], 'description': 'Most widely used'},
            {'tuning': 'E-A-A', 'notes': ['E', 'A', 'A'], 'description': 'Alternative tuning'},
            {'tuning': 'E-B-E', 'notes': ['E', 'B', 'E'], 'description': 'Alternative tuning'},
        ],
        '2_string': [
            {'tuning': 'E-A', 'notes': ['E', 'A'], 'description': 'Standard 2-string'},
            {'tuning': 'E-B', 'notes': ['E', 'B'], 'description': 'Alternative'},
            {'tuning': 'E-D', 'notes': ['E', 'D'], 'description': 'Alternative'},
            {'tuning': 'E-E', 'notes': ['E', 'E'], 'description': 'Unison tuning'},
        ],
        '4_string': [
            {'tuning': 'E-A-E-A', 'notes': ['E', 'A', 'E', 'A'], 'description': 'Standard 4-string'},
            {'tuning': 'E-A-E-B', 'notes': ['E', 'A', 'E', 'B'], 'description': 'Alternative'},
            {'tuning': 'A-E-A-E', 'notes': ['A', 'E', 'A', 'E'], 'description': 'Inverted'},
            {'tuning': 'E-E-A-A', 'notes': ['E', 'E', 'A', 'A'], 'description': 'Paired unison'},
        ],
        'regional': [
            {'tuning': 'D-A-G', 'notes': ['D', 'A', 'G'], 'description': 'Lai noi tuning from Nong Kai Province', 'region': 'Nong Kai'},
            {'tuning': 'A-D-A', 'notes': ['A', 'D', 'A'], 'description': 'Lai noi tuning (Terry Miller study)', 'region': 'Other region'},
        ]
    }
    
    LAI_PATTERNS = [
        LaiPattern(
            name_thai='ลายกาเต้นก้อน',
            name_english='Lai Ka Ten Kon',
            meaning='Crows dancing over the rocks',
            scale_type='A minor pentatonic',
            drone_note='D',
            performer='Thongsai Thabthanon',
            province='Ubon Ratchathani',
            source_page=101,
            characteristics=['pentatonic', 'upbeat accents', 'sixteenth notes', 'drone on D']
        ),
        LaiPattern(
            name_thai='ลายแก้วหน้าม้า',
            name_english='Lai Kaeo Na Ma',
            meaning="A house's face",
            scale_type='G pentatonic',
            drone_note='G',
            performer='Boomma Kaowong',
            province='Kalasin',
            source_page=101,
            characteristics=['pentatonic', 'penta-centric', 'rhythmic intensity', 'drone on G']
        ),
        LaiPattern(
            name_thai='ลายน้อย',
            name_english='Lai Noi',
            meaning='Small/minor pattern',
            scale_type='pentatonic',
            drone_note='',
            performer='',
            province='Nong Kai / Various',
            source_page=100,
            characteristics=['regional variations in tuning']
        ),
        LaiPattern(
            name_thai='ลายใหญ่',
            name_english='Lai Yai',
            meaning='Large/major pattern',
            scale_type='A minor pentatonic (A, C, D, E, G)',
            drone_note='',
            performer='',
            province='',
            source_page=27,
            characteristics=['fundamental mode']
        ),
        LaiPattern(
            name_thai='ลายแม่บท',
            name_english='Lai Mae Bot',
            meaning='Fundamental modes',
            scale_type='pentatonic',
            drone_note='',
            performer='',
            province='',
            source_page=100,
            characteristics=['base patterns from khaen tradition']
        ),
    ]
    
    PHIN_ARTISTS = [
        PhinArtist(
            name='Thongsai Thabthanon (ทองใส ทับธานนท์)',
            province='Ubon Ratchathani',
            specialty='Electric phin pioneer',
            description='Forerunner of modern phin performance using electric phin. Known for recording phleng luk thung with phin. Performances featured in isan nuea films.',
            notable_works=['Lai Ka Ten Kon'],
            source_page=101
        ),
        PhinArtist(
            name='Boomma Kaowong (บุญมา แก้ววงษ์)',
            province='Kalasin',
            specialty='Three-string phin master',
            description='Visually impaired phin master. Acclaimed as the maestro of three-string phin and one of the most rhythmically skilled performers.',
            notable_works=['Lai Kaeo Na Ma'],
            source_page=101
        ),
    ]
    
    PHIN_TECHNIQUES = [
        PhinTechnique(
            name='Sieng Sep (เสียงเซ็บ)',
            description='Drone technique similar to khaen, sustained pitch underneath melody',
            category='drone',
            source_page=102
        ),
        PhinTechnique(
            name='Upbeat Accents',
            description='Swing-like feel with emphasis on upbeats in eighth-note settings',
            category='rhythm',
            source_page=102
        ),
        PhinTechnique(
            name='Sixteenth Note Patterns',
            description='Used to create rhythmic intensity in performances',
            category='rhythm',
            source_page=102
        ),
        PhinTechnique(
            name='Pentatonic Construction',
            description='Primary melodic construction based on pentatonic scales',
            category='melody',
            source_page=102
        ),
        PhinTechnique(
            name='Penta-centric Concept',
            description='Melodic approach centered around five-note scale system',
            category='melody',
            source_page=102
        ),
    ]
    
    def __init__(self, output_dir: str = "output/phin_dataset"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_content: Dict[int, str] = {}
    
    def load_phin_pages(self, pages_json_path: str = None):
        """Load phin-related page content."""
        if pages_json_path and Path(pages_json_path).exists():
            with open(pages_json_path, 'r', encoding='utf-8') as f:
                self.extracted_content = json.load(f)
    
    def build_tuning_dataset(self) -> pd.DataFrame:
        """Build dataset of phin tuning systems."""
        rows = []
        for string_type, tunings in self.PHIN_TUNING_SYSTEMS.items():
            for tuning in tunings:
                rows.append({
                    'string_count': int(string_type.split('_')[0]) if string_type != 'regional' else 3,
                    'tuning_type': string_type,
                    'tuning': tuning['tuning'],
                    'notes': ','.join(tuning['notes']),
                    'description': tuning['description'],
                    'region': tuning.get('region', 'Standard'),
                })
        return pd.DataFrame(rows)
    
    def build_lai_dataset(self) -> pd.DataFrame:
        """Build dataset of lai patterns."""
        rows = []
        for lai in self.LAI_PATTERNS:
            row = {
                'name_thai': lai.name_thai,
                'name_english': lai.name_english,
                'meaning': lai.meaning,
                'scale_type': lai.scale_type,
                'drone_note': lai.drone_note,
                'performer': lai.performer,
                'province': lai.province,
                'source_page': lai.source_page,
                'characteristics': ','.join(lai.characteristics) if lai.characteristics else ''
            }
            rows.append(row)
        return pd.DataFrame(rows)
    
    def build_artist_dataset(self) -> pd.DataFrame:
        """Build dataset of phin artists."""
        rows = []
        for artist in self.PHIN_ARTISTS:
            rows.append({
                'name': artist.name,
                'province': artist.province,
                'specialty': artist.specialty,
                'description': artist.description,
                'notable_works': ','.join(artist.notable_works) if artist.notable_works else '',
                'source_page': artist.source_page
            })
        return pd.DataFrame(rows)
    
    def build_technique_dataset(self) -> pd.DataFrame:
        """Build dataset of phin techniques."""
        rows = []
        for tech in self.PHIN_TECHNIQUES:
            rows.append({
                'name': tech.name,
                'description': tech.description,
                'category': tech.category,
                'source_page': tech.source_page
            })
        return pd.DataFrame(rows)
    
    def build_ml_features_schema(self) -> Dict:
        """Build ML feature schema for phin audio analysis."""
        return {
            'name': 'Phin ML Dataset Schema',
            'version': '1.0',
            'instrument': 'phin',
            'instrument_thai': 'พิณ',
            'description': 'Machine learning dataset schema for Thai Phin instrument analysis',
            'audio_features': {
                'spectral': {
                    'mfcc': {'description': 'Mel-frequency cepstral coefficients', 'dimensions': 13},
                    'spectral_centroid': {'description': 'Center of mass of spectrum'},
                    'spectral_bandwidth': {'description': 'Spread of spectrum'},
                    'chroma': {'description': 'Pitch class energy distribution', 'dimensions': 12},
                },
                'temporal': {
                    'tempo': {'description': 'Beats per minute'},
                    'beat_frames': {'description': 'Beat positions in frames'},
                    'onset_strength': {'description': 'Note onset detection strength'},
                },
                'harmonic': {
                    'fundamental_frequency': {'description': 'F0 estimation for melody'},
                    'harmonic_ratio': {'description': 'Harmonic to noise ratio'},
                },
                'phin_specific': {
                    'drone_detection': {'description': 'Detect sieng sep (drone) presence'},
                    'string_count_estimation': {'description': 'Estimate 2/3/4 string phin'},
                    'lai_pattern_recognition': {'description': 'Classify lai melodic patterns'},
                    'upbeat_accent_detection': {'description': 'Detect swing-like upbeat patterns'},
                    'pentatonic_scale_detection': {'description': 'Identify pentatonic scale usage'},
                }
            },
            'annotation_types': {
                'lai_label': {'type': 'categorical', 'values': ['lai_ka_ten_kon', 'lai_kaeo_na_ma', 'lai_noi', 'lai_yai', 'lai_mae_bot', 'other']},
                'tuning': {'type': 'categorical', 'values': [
                    'E-A-E', 'E-A-A', 'E-B-E',
                    'E-A', 'E-B', 'E-D', 'E-E',
                    'E-A-E-A', 'E-A-E-B', 'A-E-A-E', 'E-E-A-A',
                    'D-A-G', 'A-D-A',
                    'other'
                ]},
                'drone_note': {'type': 'categorical', 'values': ['D', 'G', 'A', 'E', 'none', 'other']},
                'technique': {'type': 'multi_label', 'values': ['sieng_sep', 'upbeat_accent', 'sixteenth_notes', 'pentatonic', 'penta_centric']},
                'performer': {'type': 'string', 'description': 'Name of phin performer'},
                'province': {'type': 'categorical', 'values': ['Ubon Ratchathani', 'Kalasin', 'Nong Kai', 'Various', 'other']},
            },
            'recommended_sample_rate': 22050,
            'recommended_hop_length': 512,
            'recommended_n_fft': 2048,
        }
    
    def extract_phin_content_analysis(self) -> List[Dict]:
        """Analyze extracted content for phin-specific information."""
        analysis = []
        
        patterns = {
            'tuning': r'(?:tuning|tuned|string)[^.]*(?:E|A|D|G|B)[-\s](?:E|A|D|G|B)',
            'lai_pattern': r'lai\s+\w+|ลาย\w+',
            'pentatonic': r'pentatonic|penta[-\s]?centric',
            'drone': r'drone|sieng\s+sep|เสียงเซ็บ',
            'technique': r'accent|upbeat|sixteenth|rhythm',
            'performer': r'(?:Thongsai|Boomma|ทองใส|บุญมา)',
            'province': r'(?:Ubon|Kalasin|Nong\s+Kai|อุบล|กาฬสินธุ์|หนองคาย)',
        }
        
        for page_num, content in self.extracted_content.items():
            page_analysis = {
                'page': int(page_num),
                'has_tuning_info': bool(re.search(patterns['tuning'], content, re.IGNORECASE)),
                'has_lai_pattern': bool(re.search(patterns['lai_pattern'], content, re.IGNORECASE)),
                'has_pentatonic': bool(re.search(patterns['pentatonic'], content, re.IGNORECASE)),
                'has_drone_info': bool(re.search(patterns['drone'], content, re.IGNORECASE)),
                'has_technique': bool(re.search(patterns['technique'], content, re.IGNORECASE)),
                'has_performer': bool(re.search(patterns['performer'], content, re.IGNORECASE)),
                'has_province': bool(re.search(patterns['province'], content, re.IGNORECASE)),
                'word_count': len(content.split()),
            }
            analysis.append(page_analysis)
        
        return analysis
    
    def export_all(self):
        """Export all phin datasets."""
        tuning_df = self.build_tuning_dataset()
        tuning_df.to_csv(self.output_dir / 'phin_tuning.csv', index=False)
        tuning_df.to_json(self.output_dir / 'phin_tuning.json', orient='records', force_ascii=False, indent=2)
        
        lai_df = self.build_lai_dataset()
        lai_df.to_csv(self.output_dir / 'phin_lai_patterns.csv', index=False)
        lai_df.to_json(self.output_dir / 'phin_lai_patterns.json', orient='records', force_ascii=False, indent=2)
        
        artist_df = self.build_artist_dataset()
        artist_df.to_csv(self.output_dir / 'phin_artists.csv', index=False)
        artist_df.to_json(self.output_dir / 'phin_artists.json', orient='records', force_ascii=False, indent=2)
        
        technique_df = self.build_technique_dataset()
        technique_df.to_csv(self.output_dir / 'phin_techniques.csv', index=False)
        technique_df.to_json(self.output_dir / 'phin_techniques.json', orient='records', force_ascii=False, indent=2)
        
        schema = self.build_ml_features_schema()
        with open(self.output_dir / 'phin_ml_schema.json', 'w', encoding='utf-8') as f:
            json.dump(schema, f, ensure_ascii=False, indent=2)
        
        if self.extracted_content:
            content_analysis = self.extract_phin_content_analysis()
            analysis_df = pd.DataFrame(content_analysis)
            analysis_df.to_csv(self.output_dir / 'phin_page_analysis.csv', index=False)
        
        combined_dataset = {
            'metadata': {
                'name': 'Phin Dataset',
                'description': 'Comprehensive dataset for Thai Phin instrument research',
                'source': 'PhD Dissertation - Machine Learning Dataset for Cross-Cultural Music',
                'pages_analyzed': list(self.extracted_content.keys()) if self.extracted_content else [],
            },
            'tuning_systems': tuning_df.to_dict(orient='records'),
            'lai_patterns': lai_df.to_dict(orient='records'),
            'artists': artist_df.to_dict(orient='records'),
            'techniques': technique_df.to_dict(orient='records'),
            'ml_schema': schema,
        }
        
        with open(self.output_dir / 'phin_dataset_complete.json', 'w', encoding='utf-8') as f:
            json.dump(combined_dataset, f, ensure_ascii=False, indent=2)
        
        print(f"\nPhin Dataset exported to: {self.output_dir}")
        print(f"  - phin_tuning.csv/json ({len(tuning_df)} tuning systems)")
        print(f"  - phin_lai_patterns.csv/json ({len(lai_df)} lai patterns)")
        print(f"  - phin_artists.csv/json ({len(artist_df)} artists)")
        print(f"  - phin_techniques.csv/json ({len(technique_df)} techniques)")
        print(f"  - phin_ml_schema.json (ML feature schema)")
        print(f"  - phin_dataset_complete.json (combined dataset)")
        
        return combined_dataset


def main():
    """Build and export phin dataset."""
    print("=" * 60)
    print("PHIN DATASET BUILDER")
    print("Thai Phin (พิณ) Instrument Research Dataset")
    print("=" * 60)
    
    builder = PhinDatasetBuilder()
    
    phin_pages_path = "/tmp/phin_pages_raw.json"
    if Path(phin_pages_path).exists():
        builder.load_phin_pages(phin_pages_path)
        print(f"\nLoaded {len(builder.extracted_content)} pages of phin content")
    
    dataset = builder.export_all()
    
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    
    print("\nTuning Systems:")
    tuning_df = builder.build_tuning_dataset()
    for _, row in tuning_df.iterrows():
        print(f"  [{row['string_count']} strings] {row['tuning']}: {row['description']}")
    
    print("\nLai Patterns:")
    lai_df = builder.build_lai_dataset()
    for _, row in lai_df.iterrows():
        print(f"  {row['name_thai']} ({row['name_english']}): {row['meaning']}")
    
    print("\nArtists:")
    artist_df = builder.build_artist_dataset()
    for _, row in artist_df.iterrows():
        print(f"  {row['name']} - {row['specialty']}")
    
    print("\nTechniques:")
    technique_df = builder.build_technique_dataset()
    for _, row in technique_df.iterrows():
        print(f"  {row['name']} [{row['category']}]")
    
    print("\n" + "=" * 60)
    print("Phin Dataset creation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
