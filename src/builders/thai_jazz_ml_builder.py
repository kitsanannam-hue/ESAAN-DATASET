
#!/usr/bin/env python3
"""
Thai-Jazz ML Dataset Builder
=============================
Comprehensive ML dataset builder for Thai-Jazz fusion music analysis.
Based on PhD dissertation research.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import re


@dataclass
class MusicFeature:
    """Represents a music feature for ML."""
    name: str
    category: str
    thai_term: str
    description: str
    application: str
    examples: List[str]
    source_pages: List[int]


class ThaiJazzMLBuilder:
    """Build comprehensive ML dataset for Thai-Jazz fusion."""
    
    # Thai Classical Music Features (ดนตรีไทยเดิม)
    THAI_CLASSICAL_FEATURES = {
        'thao': MusicFeature(
            name='Thao (เทา)',
            category='compositional_technique',
            thai_term='เทา',
            description='Melodic augmentation/diminution technique',
            application='Apply to jazz standards like Giant Steps',
            examples=['Khaek Toi Moh'],
            source_pages=[68, 75]
        ),
        'luk_mot': MusicFeature(
            name='Luk Mot (ลูกโมท)',
            category='melodic_pattern',
            thai_term='ลูกโมท',
            description='Closing melodic phrase (similar to blues riff)',
            application='Use as ending phrases in jazz composition',
            examples=['Khaek Toi Moh'],
            source_pages=[71]
        ),
        'luk_yon': MusicFeature(
            name='Luk Yon (ลูกย้อน)',
            category='harmonic_technique',
            thai_term='ลูกย้อน',
            description='Pedal point / sustained pitch',
            application='Create modal jazz harmonies',
            examples=['Thai classical compositions'],
            source_pages=[71]
        ),
        'ti_kep': MusicFeature(
            name='Ti Kep (ตีเก็บ)',
            category='ornamental_technique',
            thai_term='ตีเก็บ',
            description='8-note run imitating ranad ek xylophone',
            application='Vibraphone or marimba techniques in jazz orchestra',
            examples=['Samniang Jin'],
            source_pages=[73, 183]
        ),
        'thang_kro': MusicFeature(
            name='Thang Kro (ทางกรอ)',
            category='ornamental_technique',
            thai_term='ทางกรอ',
            description='Tremolo technique',
            application='String section or woodwind tremolo effects',
            examples=['Nanapa'],
            source_pages=[88, 92]
        ),
        'nathap_propkai': MusicFeature(
            name='Nathap Propkai (หน้าทับพรบ ไกล)',
            category='rhythmic_pattern',
            thai_term='หน้าทับพรบไกล',
            description='Thai rhythmic cycle (3 levels: sam chan, song chan, chan dio)',
            application='Adapt to drum set and bass patterns',
            examples=['Thai classical compositions'],
            source_pages=[62, 64]
        ),
    }
    
    # Isan Music Features (ดนตรีอีสาน)
    ISAN_FEATURES = {
        'lai_yai': MusicFeature(
            name='Lai Yai (ลายใหญ่)',
            category='mode',
            thai_term='ลายใหญ่',
            description='A minor pentatonic mode (A, C, D, E, G)',
            application='Bass improvisation, modal jazz composition',
            examples=['Lai Teay Khong', 'Mekong'],
            source_pages=[27, 107, 200]
        ),
        'lai_noi': MusicFeature(
            name='Lai Noi (ลายน้อย)',
            category='mode',
            thai_term='ลายน้อย',
            description='D minor pentatonic mode (D, F, G, A, C)',
            application='Reharmonization with jazz chords',
            examples=['Lai Lom Phat Phrao'],
            source_pages=[100, 107]
        ),
        'khaen_drone': MusicFeature(
            name='Sieng Sep (เสียงเซ็บ)',
            category='harmonic_technique',
            thai_term='เสียงเซ็บ',
            description='Drone technique (root, P4, P5, octave)',
            application='Creates suspended chord texture in jazz',
            examples=['Khaen performances'],
            source_pages=[99, 102]
        ),
        'upbeat_accent': MusicFeature(
            name='Upbeat Accents',
            category='rhythmic_pattern',
            thai_term='จังหวะเน้นขึ้น',
            description='Swing-like upbeat emphasis',
            application='Swing feel in jazz orchestra arrangements',
            examples=['Phin performances', 'Pong lang'],
            source_pages=[102, 104]
        ),
    }
    
    # Southern Music Features (ดนตรีใต้)
    SOUTHERN_FEATURES = {
        'khuen_hua_pi': MusicFeature(
            name='Khuen Hua Pi (ขึ้นหัวปี่)',
            category='performance_technique',
            thai_term='ขึ้นหัวปี่',
            description='Pi nora ascending technique with tremolo',
            application='Soprano saxophone techniques',
            examples=['Singora'],
            source_pages=[112, 114]
        ),
        'lagu_dua': MusicFeature(
            name='Lagu Dua',
            category='rhythmic_pattern',
            thai_term='ลากูดัว',
            description='Rong ngeng rhythmic pattern',
            application='Conga or drum set patterns',
            examples=['Singora'],
            source_pages=[131, 223]
        ),
        'nora_gongs': MusicFeature(
            name='Mong (ฆ้อง)',
            category='harmonic_marker',
            thai_term='ฆ้อง',
            description='Two gongs in perfect 5th (D-G or Eb-Ab)',
            application='Bass markers in jazz arrangement',
            examples=['Singora'],
            source_pages=[115, 230]
        ),
    }
    
    # Northern Music Features (ดนตรีเหนือ)
    NORTHERN_FEATURES = {
        'khap_saw': MusicFeature(
            name='Khap Saw (ขับซอ)',
            category='performance_technique',
            thai_term='ขับซอ',
            description='Vocal with pi jum (perpetual eighth-notes)',
            application='Flute/clarinet heterophony',
            examples=['Wiang Haeng'],
            source_pages=[146, 247]
        ),
        'sueng_tremolo': MusicFeature(
            name='Sueng Tremolo (ซึง)',
            category='instrumental_technique',
            thai_term='การสั่นเสียงซึง',
            description='Tremolo on sueng (fretted lute)',
            application='Guitar tremolo effects',
            examples=['Wiang Haeng'],
            source_pages=[145, 247]
        ),
    }
    
    def __init__(self, output_dir: str = "output/ml_dataset"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.all_features = {
            **self.THAI_CLASSICAL_FEATURES,
            **self.ISAN_FEATURES,
            **self.SOUTHERN_FEATURES,
            **self.NORTHERN_FEATURES
        }
    
    def build_feature_catalog(self) -> pd.DataFrame:
        """Build comprehensive feature catalog."""
        rows = []
        for feature_id, feature in self.all_features.items():
            rows.append({
                'feature_id': feature_id,
                'name': feature.name,
                'category': feature.category,
                'thai_term': feature.thai_term,
                'description': feature.description,
                'application': feature.application,
                'examples': ', '.join(feature.examples),
                'source_pages': ', '.join(map(str, feature.source_pages))
            })
        return pd.DataFrame(rows)
    
    def build_hybridization_techniques(self) -> pd.DataFrame:
        """Build hybridization techniques dataset."""
        techniques = [
            {
                'technique': 'Melodic Transformation',
                'thai_element': 'Thai melodies (Lao Somdej, Lai Teay Khong)',
                'jazz_element': 'Harmonic design, Contemporary rhythm',
                'example': 'Mekong composition',
                'source_pages': '200-213'
            },
            {
                'technique': 'Layering (Polyphonic Stratification)',
                'thai_element': 'Thang khong wong yai melodies',
                'jazz_element': 'Jazz solo interplay',
                'example': 'Samniang Jin',
                'source_pages': '182-185'
            },
            {
                'technique': 'Instrumental Imitation',
                'thai_element': 'Ranad ek (vibraphone), Pi nora (soprano sax)',
                'jazz_element': 'Jazz orchestra instrumentation',
                'example': 'Singora, Phuen Ban',
                'source_pages': '175, 227'
            },
            {
                'technique': 'Rhythmic Adaptation',
                'thai_element': 'Nathap, Rebana patterns',
                'jazz_element': 'Drum set, bass grooves',
                'example': 'Buang-Suang, Singora',
                'source_pages': '64, 223'
            },
            {
                'technique': 'Odd Meter Integration',
                'thai_element': 'Thai melodic phrases',
                'jazz_element': '5/4, 7/4, 11/8 meters',
                'example': 'Various compositions',
                'source_pages': '118'
            },
            {
                'technique': 'Literary Integration',
                'thai_element': 'Thai poetry (Pra Artit Ching Duang)',
                'jazz_element': 'Spoken-word monologues',
                'example': 'Patchim',
                'source_pages': '191-192'
            }
        ]
        return pd.DataFrame(techniques)
    
    def build_scale_mapping(self) -> pd.DataFrame:
        """Build Thai-Jazz scale mapping."""
        mappings = [
            {
                'thai_scale': 'Lai Yai (ลายใหญ่)',
                'pitches': 'A, C, D, E, G',
                'jazz_equivalent': 'A minor pentatonic',
                'compatible_chords': 'Am7, Dm7, Em7(b5), Fmaj7, G7sus4',
                'application': 'Modal jazz, bass improvisation'
            },
            {
                'thai_scale': 'Lai Noi (ลายน้อย)',
                'pitches': 'D, F, G, A, C',
                'jazz_equivalent': 'D minor pentatonic',
                'compatible_chords': 'Dm7, Gm7, Am7(b5), Bbmaj7, C7sus4',
                'application': 'Reharmonization, Dorian mode'
            },
            {
                'thai_scale': 'Lai Se (ลายเส)',
                'pitches': 'E, G, A, B, D',
                'jazz_equivalent': 'E minor pentatonic',
                'compatible_chords': 'Em7, Am7, Bm7(b5), Cmaj7, D7sus4',
                'application': 'Khaen improvisation style'
            },
            {
                'thai_scale': 'Lai Sutsanaen (ลายสุดสะแนน)',
                'pitches': 'C, D, E, G, A',
                'jazz_equivalent': 'C major pentatonic',
                'compatible_chords': 'Cmaj7, Dm7, Em7, Am7, G7sus4',
                'application': 'Major tonality, bright sound'
            },
            {
                'thai_scale': 'Nora Scale',
                'pitches': 'C, D, E, G (with G as marker)',
                'jazz_equivalent': 'C major pentatonic subset',
                'compatible_chords': 'Cmaj7, G7sus4, Am7',
                'application': 'Southern Thai melodic style'
            }
        ]
        return pd.DataFrame(mappings)
    
    def build_ml_audio_features_schema(self) -> Dict:
        """Build ML audio features schema."""
        return {
            'version': '2.0',
            'name': 'Thai-Jazz Cross-Cultural ML Dataset',
            'description': 'Comprehensive ML dataset for Thai-Jazz fusion analysis',
            'audio_features': {
                'spectral': {
                    'mfcc': {
                        'description': 'Mel-frequency cepstral coefficients',
                        'dimensions': 13,
                        'use_case': 'Timbre analysis, instrument identification'
                    },
                    'spectral_centroid': {
                        'description': 'Center of mass of spectrum',
                        'use_case': 'Brightness, ranad ek vs vibraphone distinction'
                    },
                    'spectral_bandwidth': {
                        'description': 'Spread of spectrum',
                        'use_case': 'Harmonic richness, drone detection'
                    },
                    'chroma': {
                        'description': 'Pitch class energy distribution',
                        'dimensions': 12,
                        'use_case': 'Pentatonic scale detection, lai identification'
                    },
                },
                'temporal': {
                    'tempo': {
                        'description': 'Beats per minute',
                        'use_case': 'Chan (sam/song/dio) classification'
                    },
                    'beat_frames': {
                        'description': 'Beat positions',
                        'use_case': 'Nathap pattern analysis'
                    },
                    'onset_strength': {
                        'description': 'Note onset detection',
                        'use_case': 'Upbeat accent detection, swing feel'
                    },
                },
                'harmonic': {
                    'fundamental_frequency': {
                        'description': 'F0 estimation',
                        'use_case': 'Melody extraction, lai pattern recognition'
                    },
                    'harmonic_ratio': {
                        'description': 'Harmonic to noise ratio',
                        'use_case': 'Khaen drone vs melody separation'
                    },
                },
                'thai_specific': {
                    'pentatonic_detection': {
                        'description': 'Detect pentatonic scale usage',
                        'techniques': ['pitch histogram', 'key profile matching']
                    },
                    'drone_detection': {
                        'description': 'Detect sustained pitches (sieng sep)',
                        'techniques': ['spectral flux', 'pitch constancy']
                    },
                    'ornament_classification': {
                        'description': 'Classify Thai ornaments (kro, won, ti kep)',
                        'techniques': ['pitch contour analysis', 'temporal patterns']
                    },
                    'nathap_recognition': {
                        'description': 'Recognize Thai rhythmic cycles',
                        'techniques': ['beat histogram', 'accent pattern matching']
                    }
                }
            },
            'annotation_types': {
                'feature_label': {
                    'type': 'multi_label',
                    'values': list(self.all_features.keys()),
                    'description': 'Thai music features present in audio'
                },
                'lai_mode': {
                    'type': 'categorical',
                    'values': ['lai_yai', 'lai_noi', 'lai_se', 'lai_sutsanaen', 
                              'lai_pong_sai', 'lai_soi', 'none'],
                    'description': 'Isan lai mode classification'
                },
                'hybridization_level': {
                    'type': 'ordinal',
                    'values': ['pure_thai', 'thai_dominant', 'balanced', 
                              'jazz_dominant', 'pure_jazz'],
                    'description': 'Degree of Thai-Jazz fusion'
                },
                'regional_style': {
                    'type': 'categorical',
                    'values': ['central', 'isan', 'southern', 'northern', 'mixed'],
                    'description': 'Thai regional music style'
                },
                'jazz_style': {
                    'type': 'categorical',
                    'values': ['swing', 'bebop', 'modal', 'fusion', 'contemporary'],
                    'description': 'Jazz style classification'
                }
            },
            'composition_metadata': {
                'composition_name': 'string',
                'composer': 'string',
                'duration_seconds': 'float',
                'tempo_bpm': 'float',
                'key_signature': 'string',
                'time_signature': 'string',
                'instrumentation': 'list[string]',
                'source_pages': 'list[int]'
            },
            'recommended_parameters': {
                'sample_rate': 22050,
                'hop_length': 512,
                'n_fft': 2048,
                'n_mels': 128,
                'frame_length': 2048
            }
        }
    
    def export_all(self):
        """Export all ML datasets."""
        # Feature catalog
        features_df = self.build_feature_catalog()
        features_df.to_csv(self.output_dir / 'thai_jazz_features.csv', index=False)
        features_df.to_json(self.output_dir / 'thai_jazz_features.json', 
                           orient='records', force_ascii=False, indent=2)
        
        # Hybridization techniques
        hybrid_df = self.build_hybridization_techniques()
        hybrid_df.to_csv(self.output_dir / 'hybridization_techniques.csv', index=False)
        hybrid_df.to_json(self.output_dir / 'hybridization_techniques.json',
                         orient='records', force_ascii=False, indent=2)
        
        # Scale mappings
        scales_df = self.build_scale_mapping()
        scales_df.to_csv(self.output_dir / 'thai_jazz_scale_mapping.csv', index=False)
        scales_df.to_json(self.output_dir / 'thai_jazz_scale_mapping.json',
                         orient='records', force_ascii=False, indent=2)
        
        # ML schema
        schema = self.build_ml_audio_features_schema()
        with open(self.output_dir / 'ml_audio_features_schema.json', 'w', encoding='utf-8') as f:
            json.dump(schema, f, ensure_ascii=False, indent=2)
        
        # Complete dataset
        complete_dataset = {
            'metadata': {
                'name': 'Thai-Jazz Cross-Cultural ML Dataset',
                'version': '2.0',
                'description': 'Comprehensive dataset for Thai-Jazz fusion music analysis',
                'source': 'PhD Dissertation: Jazz Orchestra Portraits of Thailand',
                'total_features': len(self.all_features),
                'regional_coverage': ['Central', 'Isan', 'Southern', 'Northern']
            },
            'features': features_df.to_dict('records'),
            'hybridization_techniques': hybrid_df.to_dict('records'),
            'scale_mappings': scales_df.to_dict('records'),
            'ml_schema': schema
        }
        
        with open(self.output_dir / 'complete_ml_dataset.json', 'w', encoding='utf-8') as f:
            json.dump(complete_dataset, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*70}")
        print("Thai-Jazz ML Dataset Export Complete")
        print(f"{'='*70}")
        print(f"\nOutput directory: {self.output_dir}")
        print(f"\nFiles created:")
        print(f"  - thai_jazz_features.csv/json ({len(features_df)} features)")
        print(f"  - hybridization_techniques.csv/json ({len(hybrid_df)} techniques)")
        print(f"  - thai_jazz_scale_mapping.csv/json ({len(scales_df)} mappings)")
        print(f"  - ml_audio_features_schema.json")
        print(f"  - complete_ml_dataset.json")
        print(f"\n{'='*70}")
        
        return complete_dataset


if __name__ == "__main__":
    builder = ThaiJazzMLBuilder()
    builder.export_all()
