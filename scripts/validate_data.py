
#!/usr/bin/env python3
"""Validate all datasets."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzers.data_quality_checker import DataQualityChecker

def main():
    print("=" * 70)
    print("Validating All Datasets")
    print("=" * 70)
    
    checker = DataQualityChecker()
    checker.generate_report()
    
    print("\n" + "=" * 70)
    print("Validation complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
