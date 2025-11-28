
# Phin Dataset Documentation

## Overview

The Phin dataset is a specialized collection for Thai Phin (พิณ) instrument research, extracted from the dissertation. The Phin is a traditional Thai stringed instrument commonly used in Isan (Northeast Thailand) music.

## Dataset Components

### 1. Tuning Systems

**File:** `output/phin_dataset/phin_tuning.csv/json`

13 tuning configurations for 2, 3, and 4-string Phin instruments.

#### 3-String Phin
- **E-A-E**: Most widely used tuning
- **E-A-A**: Alternative tuning
- **E-B-E**: Alternative tuning

#### 2-String Phin
- **E-A**: Standard 2-string
- **E-B**: Alternative
- **E-D**: Alternative
- **E-E**: Unison tuning

#### 4-String Phin
- **E-A-E-A**: Standard 4-string
- **E-A-E-B**: Alternative
- **A-E-A-E**: Inverted
- **E-E-A-A**: Paired unison

#### Regional Variations
- **D-A-G**: Lai noi tuning (Nong Kai Province)
- **A-D-A**: Lai noi tuning (other regions)

### 2. Lai Patterns (ลาย)

**File:** `output/phin_dataset/phin_lai_patterns.csv/json`

5 traditional melodic patterns used in Phin performance.

#### Lai Ka Ten Kon (ลายกาเต้นก้อน)
- **Meaning**: "Crows dancing over the rocks"
- **Scale**: A minor pentatonic
- **Drone**: D
- **Performer**: Thongsai Thabthanon (Ubon Ratchathani)
- **Characteristics**: Pentatonic, upbeat accents, sixteenth notes

#### Lai Kaeo Na Ma (ลายแก้วหน้าม้า)
- **Meaning**: "A house's face"
- **Scale**: G pentatonic
- **Drone**: G
- **Performer**: Boomma Kaowong (Kalasin)
- **Characteristics**: Penta-centric, rhythmic intensity

#### Lai Noi (ลายน้อย)
- **Meaning**: "Small/minor pattern"
- **Scale**: Pentatonic
- **Region**: Nong Kai / Various
- **Characteristics**: Regional tuning variations

#### Lai Yai (ลายใหญ่)
- **Meaning**: "Large/major pattern"
- **Scale**: A minor pentatonic (A, C, D, E, G)
- **Characteristics**: Fundamental mode

#### Lai Mae Bot (ลายแม่บท)
- **Meaning**: "Fundamental modes"
- **Scale**: Pentatonic
- **Characteristics**: Base patterns from khaen tradition

### 3. Master Artists

**File:** `output/phin_dataset/phin_artists.csv/json`

2 renowned Phin performers documented in the dissertation.

#### Thongsai Thabthanon (ทองใส ทับธานนท์)
- **Province**: Ubon Ratchathani
- **Specialty**: Electric phin pioneer
- **Notable**: Forerunner of modern phin performance, recorded phleng luk thung
- **Works**: Lai Ka Ten Kon

#### Boomma Kaowong (บุญมา แก้ววงษ์)
- **Province**: Kalasin
- **Specialty**: Three-string phin master
- **Notable**: Visually impaired maestro, rhythmically skilled
- **Works**: Lai Kaeo Na Ma

### 4. Playing Techniques

**File:** `output/phin_dataset/phin_techniques.csv/json`

5 fundamental Phin playing techniques.

#### Sieng Sep (เสียงเซ็บ)
- **Category**: Drone
- **Description**: Sustained pitch underneath melody, similar to khaen

#### Upbeat Accents
- **Category**: Rhythm
- **Description**: Swing-like feel with emphasis on upbeats

#### Sixteenth Note Patterns
- **Category**: Rhythm
- **Description**: Creates rhythmic intensity

#### Pentatonic Construction
- **Category**: Melody
- **Description**: Primary melodic construction based on pentatonic scales

#### Penta-centric Concept
- **Category**: Melody
- **Description**: Melodic approach centered around five-note scale system

## ML Feature Schema

**File:** `output/phin_dataset/phin_ml_schema.json`

Machine learning feature schema for Phin audio analysis.

### Phin-Specific Features

```json
{
  "phin_specific": {
    "drone_detection": "Detect sieng sep (drone) presence",
    "string_count_estimation": "Estimate 2/3/4 string phin",
    "lai_pattern_recognition": "Classify lai melodic patterns",
    "upbeat_accent_detection": "Detect swing-like upbeat patterns",
    "pentatonic_scale_detection": "Identify pentatonic scale usage"
  }
}
```

### Recommended Audio Parameters

- **Sample Rate**: 22050 Hz
- **Hop Length**: 512
- **FFT Size**: 2048

## Usage Example

```python
from src.phin_dataset_builder import PhinDatasetBuilder

builder = PhinDatasetBuilder()

# Load phin-related pages (optional)
builder.load_phin_pages("/tmp/phin_pages_raw.json")

# Build individual datasets
tuning_df = builder.build_tuning_dataset()
lai_df = builder.build_lai_dataset()
artist_df = builder.build_artist_dataset()
technique_df = builder.build_technique_dataset()

# Get ML schema
schema = builder.build_ml_features_schema()

# Export everything
dataset = builder.export_all()
```

## Research Applications

The Phin dataset can be used for:

1. **Instrument Recognition**: Train models to identify Phin vs. other instruments
2. **Tuning Classification**: Detect which tuning system is being used
3. **Lai Pattern Recognition**: Classify traditional melodic patterns
4. **Technique Detection**: Identify playing techniques in audio
5. **Regional Style Analysis**: Compare performance styles across regions
6. **Cross-Cultural Studies**: Analyze fusion of Phin with other musical traditions
