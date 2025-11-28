
#!/usr/bin/env python3
"""Export all datasets at once."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.builders.thai_jazz_ml_builder import ThaiJazzMLBuilder
from src.builders.phin_dataset_builder import PhinDatasetBuilder
from src.extractors.music_notation_extractor import MusicNotationExtractor

def main():
    print("=" * 70)
    print("Exporting All Datasets")
    print("=" * 70)
    
    print("\n[1/3] Exporting Thai-Jazz ML Dataset...")
    ml_builder = ThaiJazzMLBuilder()
    ml_builder.export_all()
    
    print("\n[2/3] Exporting Phin Dataset...")
    phin_builder = PhinDatasetBuilder()
    phin_builder.export_all()
    
    print("\n[3/3] Exporting Music Notation Dataset...")
    notation_extractor = MusicNotationExtractor()
    notation_extractor.export_notation_dataset()
    
    print("\n" + "=" * 70)
    print("All datasets exported successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()
