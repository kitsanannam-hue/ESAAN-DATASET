import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd
from dataclasses import dataclass, asdict
from enum import Enum


class MusicCategory(Enum):
    THAI_TRADITIONAL = "thai_traditional"
    JAZZ_MODERN = "jazz_modern"
    CROSS_CULTURAL_FUSION = "cross_cultural_fusion"
    MUSIC_THEORY = "music_theory"
    ML_FEATURES = "ml_features"


@dataclass
class MusicFeature:
    """Represents a music feature extracted from the dissertation."""
    name: str
    category: str
    description: str
    data_type: str
    value_range: Optional[str] = None
    source_page: Optional[int] = None
    example_values: Optional[List[Any]] = None


@dataclass
class DatasetEntry:
    """Represents a single entry in the ML dataset."""
    entry_id: str
    category: str
    subcategory: str
    content: str
    features: Dict[str, Any]
    source_page: int
    keywords: List[str]
    metadata: Dict[str, Any]


class ThaiJazzDatasetBuilder:
    """Build ML dataset for Thai-Jazz cross-cultural music fusion."""
    
    THAI_MUSIC_FEATURES = {
        'thang': {
            'description': 'Thai melodic mode system (7 modes)',
            'modes': ['nai', 'klang', 'phiang-o-lang', 'phiang-o-bon', 
                     'kruad', 'chawa', 'samniang']
        },
        'luk_tok': {
            'description': 'Thai rhythmic patterns and accents',
            'patterns': ['sam_chan', 'song_chan', 'chan_dio']
        },
        'ornaments': {
            'description': 'Thai melodic ornamentations',
            'types': ['kro', 'won', 'soi']
        },
        'scale_structure': {
            'description': 'Thai pentatonic/heptatonic scale systems',
            'types': ['pentatonic_anhemitonic', 'heptatonic_equidistant']
        }
    }
    
    JAZZ_FEATURES = {
        'chord_types': {
            'description': 'Jazz chord vocabulary',
            'types': ['major7', 'minor7', 'dominant7', 'half_diminished', 
                     'diminished', 'augmented', 'altered', 'suspended']
        },
        'scales_modes': {
            'description': 'Jazz scales and modes',
            'types': ['major', 'dorian', 'phrygian', 'lydian', 'mixolydian',
                     'aeolian', 'locrian', 'melodic_minor', 'harmonic_minor',
                     'whole_tone', 'diminished', 'altered', 'bebop']
        },
        'rhythm_patterns': {
            'description': 'Jazz rhythmic characteristics',
            'patterns': ['swing', 'straight', 'shuffle', 'latin', 'funk']
        },
        'improvisation': {
            'description': 'Jazz improvisation techniques',
            'techniques': ['chord_tones', 'approach_notes', 'enclosures',
                          'sequences', 'motivic_development']
        }
    }
    
    FUSION_FEATURES = {
        'melody_integration': {
            'description': 'Techniques for blending Thai and Jazz melodies',
            'approaches': ['mode_mapping', 'ornament_adaptation', 'phrase_exchange']
        },
        'harmony_adaptation': {
            'description': 'Adapting Thai melodies to Jazz harmony',
            'techniques': ['reharmonization', 'modal_interchange', 'pedal_points']
        },
        'rhythm_fusion': {
            'description': 'Combining Thai and Jazz rhythmic elements',
            'approaches': ['polyrhythm', 'metric_modulation', 'accent_blending']
        }
    }
    
    def __init__(self):
        self.entries: List[DatasetEntry] = []
        self.features: List[MusicFeature] = []
        self.schema = self._define_schema()
        
    def _define_schema(self) -> Dict:
        """Define the ML dataset schema."""
        return {
            'version': '1.0',
            'name': 'Thai-Jazz Cross-Cultural Music Dataset',
            'description': 'Dataset for machine learning on Thai-Jazz music fusion',
            'categories': {
                'thai_traditional': {
                    'description': 'Traditional Thai music elements',
                    'features': list(self.THAI_MUSIC_FEATURES.keys())
                },
                'jazz_modern': {
                    'description': 'Modern Jazz music elements',
                    'features': list(self.JAZZ_FEATURES.keys())
                },
                'cross_cultural_fusion': {
                    'description': 'Cross-cultural fusion techniques',
                    'features': list(self.FUSION_FEATURES.keys())
                }
            },
            'audio_features': {
                'spectral': ['mfcc', 'spectral_centroid', 'spectral_bandwidth', 
                            'spectral_rolloff', 'chroma'],
                'temporal': ['tempo', 'beat_frames', 'onset_strength'],
                'harmonic': ['tonnetz', 'harmonic_percussive_ratio'],
                'rhythm': ['tempo', 'beat_histogram', 'rhythm_pattern']
            },
            'annotation_types': {
                'melodic': ['pitch_contour', 'ornament_type', 'phrase_boundary'],
                'harmonic': ['chord_label', 'key', 'mode'],
                'rhythmic': ['beat_position', 'accent_pattern', 'tempo_variation'],
                'structural': ['section_label', 'form', 'transition_type']
            }
        }
    
    def load_extracted_data(self, json_path: str) -> Dict:
        """Load previously extracted dissertation data."""
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def analyze_content_for_features(self, text: str, page_num: int) -> List[Dict]:
        """Analyze text content to extract music features."""
        found_features = []
        
        feature_patterns = {
            'pitch': r'pitch\s*(?:class|range|contour|detection)',
            'mfcc': r'MFCC|mel[-\s]?frequency\s+cepstral',
            'tempo': r'tempo\s*(?:detection|estimation|tracking)',
            'rhythm': r'rhythm(?:ic)?\s*(?:pattern|feature|analysis)|จังหวะ|luk\s*tok',
            'melody': r'melod(?:y|ic)\s*(?:contour|feature|extraction)|ทำนอง',
            'harmony': r'harmon(?:y|ic)\s*(?:analysis|feature|progression)|เสียงประสาน',
            'timbre': r'timbr(?:e|al)\s*(?:feature|analysis|characteristic)|เสียง',
            'onset': r'onset\s*(?:detection|strength)',
            'beat': r'beat\s*(?:tracking|detection|histogram)',
            'chroma': r'chroma(?:gram)?\s*(?:feature|vector)',
            'spectrogram': r'spectro(?:gram|scopy)',
            'thai_mode': r'thang|ทาง|thai\s+(?:mode|scale)|ทางเพลง|thang\s+(?:nai|klang|phiang)',
            'jazz_chord': r'(?:jazz\s+)?chord\s*(?:progression|type|voicing)|คอร์ด',
            'improvisation': r'improvis(?:ation|e|ing)|การด้น|ด้นสด',
            'ornamentation': r'ornament(?:ation|s)?|กรอ|วน|โน้ตประดับ',
            'thai_scale': r'pentatonic|heptatonic|บันไดเสียง|เสียง\s*(?:5|7)',
            'piphat': r'piphat|ปี่พาทย์|mahori|มโหรี|วงดนตรีไทย',
            'khaen': r'khaen|แคน|phin|พิณ|ranat|ระนาด',
            'cross_cultural': r'cross[-\s]?cultural|ข้ามวัฒนธรรม|intercultural|hybrid|fusion',
        }
        
        for feature_name, pattern in feature_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                context = self._extract_context(text, pattern)
                found_features.append({
                    'name': feature_name,
                    'page': page_num,
                    'context': context
                })
        
        return found_features
    
    def _extract_context(self, text: str, pattern: str, context_size: int = 150) -> str:
        """Extract context around a matched pattern."""
        match = re.search(pattern, text, re.IGNORECASE)
        if not match:
            return ""
        
        start = max(0, match.start() - context_size)
        end = min(len(text), match.end() + context_size)
        context = text[start:end].replace('\n', ' ').strip()
        return context
    
    def build_from_extracted_data(self, extracted_data: Dict) -> pd.DataFrame:
        """Build dataset from extracted dissertation data."""
        entries = []
        
        for page_num, text in extracted_data.get('extracted_text', {}).items():
            page_num = int(page_num)
            features = self.analyze_content_for_features(text, page_num)
            
            if features:
                for feature in features:
                    entry = {
                        'page': page_num,
                        'feature_name': feature['name'],
                        'context': feature['context'],
                        'word_count': len(text.split()),
                        'has_thai_music': bool(re.search(r'ดนตรีไทย|thai\s+music|piphat|mahori', text, re.IGNORECASE)),
                        'has_jazz': bool(re.search(r'jazz|แจ๊ส|improvisation|swing', text, re.IGNORECASE)),
                        'has_ml_terms': bool(re.search(r'machine\s+learning|neural|dataset|training', text, re.IGNORECASE)),
                        'has_fusion': bool(re.search(r'fusion|cross[-\s]?cultural|hybrid|blend', text, re.IGNORECASE))
                    }
                    entries.append(entry)
        
        return pd.DataFrame(entries)
    
    def generate_feature_catalog(self) -> pd.DataFrame:
        """Generate a catalog of all music features for ML."""
        catalog = []
        
        for feature_name, feature_info in self.THAI_MUSIC_FEATURES.items():
            catalog.append({
                'feature_name': feature_name,
                'category': 'thai_traditional',
                'description': feature_info['description'],
                'sub_types': json.dumps(feature_info.get('modes', 
                                       feature_info.get('patterns', 
                                       feature_info.get('types', []))))
            })
        
        for feature_name, feature_info in self.JAZZ_FEATURES.items():
            catalog.append({
                'feature_name': feature_name,
                'category': 'jazz_modern',
                'description': feature_info['description'],
                'sub_types': json.dumps(feature_info.get('types', 
                                       feature_info.get('patterns', 
                                       feature_info.get('techniques', []))))
            })
        
        for feature_name, feature_info in self.FUSION_FEATURES.items():
            catalog.append({
                'feature_name': feature_name,
                'category': 'cross_cultural_fusion',
                'description': feature_info['description'],
                'sub_types': json.dumps(feature_info.get('approaches', 
                                       feature_info.get('techniques', [])))
            })
        
        return pd.DataFrame(catalog)
    
    def export_dataset(self, output_dir: str):
        """Export all dataset components."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        with open(output_path / 'schema.json', 'w', encoding='utf-8') as f:
            json.dump(self.schema, f, ensure_ascii=False, indent=2)
        
        feature_catalog = self.generate_feature_catalog()
        feature_catalog.to_csv(output_path / 'feature_catalog.csv', index=False)
        feature_catalog.to_json(output_path / 'feature_catalog.json', 
                               orient='records', force_ascii=False, indent=2)
        
        print(f"Dataset schema exported to: {output_path / 'schema.json'}")
        print(f"Feature catalog exported to: {output_path / 'feature_catalog.csv'}")
        
        return output_path


class DatasetAnalyzer:
    """Analyze the built dataset for insights."""
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        
    def load_dataset(self) -> pd.DataFrame:
        """Load the dataset from CSV."""
        csv_path = self.dataset_path / 'dissertation_analysis.csv'
        if csv_path.exists():
            return pd.read_csv(csv_path)
        return pd.DataFrame()
    
    def generate_statistics(self, df: pd.DataFrame) -> Dict:
        """Generate dataset statistics."""
        if df.empty:
            return {'error': 'No data available'}
        
        stats = {
            'total_entries': len(df),
            'unique_pages': df['page'].nunique() if 'page' in df.columns else 0,
            'feature_distribution': df['feature_name'].value_counts().to_dict() if 'feature_name' in df.columns else {},
            'thai_music_pages': df['has_thai_music'].sum() if 'has_thai_music' in df.columns else 0,
            'jazz_pages': df['has_jazz'].sum() if 'has_jazz' in df.columns else 0,
            'ml_pages': df['has_ml_terms'].sum() if 'has_ml_terms' in df.columns else 0,
            'fusion_pages': df['has_fusion'].sum() if 'has_fusion' in df.columns else 0,
        }
        
        return stats


if __name__ == "__main__":
    print("=" * 60)
    print("Thai-Jazz Cross-Cultural Music Dataset Builder")
    print("=" * 60)
    
    builder = ThaiJazzDatasetBuilder()
    
    output_dir = "output/dataset"
    builder.export_dataset(output_dir)
    
    print("\nDataset Schema:")
    print(json.dumps(builder.schema, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("Feature Catalog Preview:")
    print("=" * 60)
    catalog = builder.generate_feature_catalog()
    print(catalog.to_string(index=False))
    
    print("\n\nTo build full dataset from extracted dissertation:")
    print("  1. Run pdf_extractor.py first to extract dissertation content")
    print("  2. Use builder.build_from_extracted_data() with extracted JSON")
