
#!/usr/bin/env python3
"""Tests for PDF extractor."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extractors.pdf_extractor import DissertationExtractor

def test_pdf_loading():
    """Test that PDF can be loaded."""
    pdf_path = Path("attached_assets/Tanarat Chaichana - PhD Dissertation [complete] 14_04_2022_1764338380212.pdf")
    
    if not pdf_path.exists():
        print(f"PDF not found at {pdf_path}")
        return False
    
    extractor = DissertationExtractor(str(pdf_path))
    assert extractor.total_pages == 680, f"Expected 680 pages, got {extractor.total_pages}"
    extractor.close()
    
    print("✓ PDF loading test passed")
    return True

if __name__ == "__main__":
    test_pdf_loading()
