
# Dataset Schema

## Overview

The ML dataset schema for Thai-Jazz cross-cultural music fusion research defines the structure for machine learning applications on audio analysis and music feature extraction.

## Categories

### Thai Traditional Music

Features specific to Thai traditional music:

```json
{
  "thang": {
    "description": "Thai melodic mode system (7 modes)",
    "modes": ["nai", "klang", "phiang-o-lang", "phiang-o-bon", 
              "kruad", "chawa", "samniang"]
  },
  "luk_tok": {
    "description": "Thai rhythmic patterns and accents",
    "patterns": ["sam_chan", "song_chan", "chan_dio"]
  },
  "ornaments": {
    "description": "Thai melodic ornamentations",
    "types": ["kro", "won", "soi"]
  },
  "scale_structure": {
    "description": "Thai pentatonic/heptatonic scale systems",
    "types": ["pentatonic_anhemitonic", "heptatonic_equidistant"]
  }
}
```

### Jazz Modern

Features specific to modern Jazz music:

```json
{
  "chord_types": {
    "description": "Jazz chord vocabulary",
    "types": ["major7", "minor7", "dominant7", "half_diminished", 
              "diminished", "augmented", "altered", "suspended"]
  },
  "scales_modes": {
    "description": "Jazz scales and modes",
    "types": ["major", "dorian", "phrygian", "lydian", "mixolydian",
              "aeolian", "locrian", "melodic_minor", "harmonic_minor",
              "whole_tone", "diminished", "altered", "bebop"]
  },
  "rhythm_patterns": {
    "description": "Jazz rhythmic characteristics",
    "patterns": ["swing", "straight", "shuffle", "latin", "funk"]
  },
  "improvisation": {
    "description": "Jazz improvisation techniques",
    "techniques": ["chord_tones", "approach_notes", "enclosures",
                   "sequences", "motivic_development"]
  }
}
```

### Cross-Cultural Fusion

Features for blending Thai and Jazz elements:

```json
{
  "melody_integration": {
    "description": "Techniques for blending Thai and Jazz melodies",
    "approaches": ["mode_mapping", "ornament_adaptation", "phrase_exchange"]
  },
  "harmony_adaptation": {
    "description": "Adapting Thai melodies to Jazz harmony",
    "techniques": ["reharmonization", "modal_interchange", "pedal_points"]
  },
  "rhythm_fusion": {
    "description": "Combining Thai and Jazz rhythmic elements",
    "approaches": ["polyrhythm", "metric_modulation", "accent_blending"]
  }
}
```

## Audio Features

### Spectral Features

- **MFCC** (Mel-frequency cepstral coefficients)
- **Spectral Centroid** (Center of mass of spectrum)
- **Spectral Bandwidth** (Spread of spectrum)
- **Spectral Rolloff** (Frequency below which 85% of energy is contained)
- **Chroma** (Pitch class energy distribution)

### Temporal Features

- **Tempo** (Beats per minute)
- **Beat Frames** (Beat positions in frames)
- **Onset Strength** (Note onset detection strength)

### Harmonic Features

- **Tonnetz** (Tonal centroid features)
- **Harmonic-Percussive Ratio** (Separation of harmonic and percussive components)

### Rhythm Features

- **Tempo** (Beat tracking)
- **Beat Histogram** (Distribution of beat strengths)
- **Rhythm Pattern** (Detected rhythmic patterns)

## Annotation Types

### Melodic Annotations

- **Pitch Contour**: Melodic line tracking
- **Ornament Type**: Thai ornament classification
- **Phrase Boundary**: Phrase segmentation

### Harmonic Annotations

- **Chord Label**: Jazz chord identification
- **Key**: Musical key detection
- **Mode**: Modal analysis (Thai thang or Jazz modes)

### Rhythmic Annotations

- **Beat Position**: Metrical position
- **Accent Pattern**: Rhythmic accent detection
- **Tempo Variation**: Tempo changes over time

### Structural Annotations

- **Section Label**: Form analysis (intro, verse, solo, etc.)
- **Form**: Overall musical structure
- **Transition Type**: Analysis of transitions between sections

## Schema File

The complete schema is available in: `output/dataset/schema.json`

```python
from src.dataset_builder import ThaiJazzDatasetBuilder

builder = ThaiJazzDatasetBuilder()
schema = builder.schema
```
