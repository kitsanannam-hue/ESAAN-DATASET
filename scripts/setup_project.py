
#!/usr/bin/env python3
"""Setup the project structure and verify dependencies."""
from pathlib import Path

def create_directories():
    """Create all necessary directories."""
    directories = [
        'data/raw/dissertations',
        'data/processed',
        'output',
        'static/css',
        'static/js',
        'static/images',
        'tests',
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {directory}")

def verify_structure():
    """Verify the project structure."""
    required = [
        'src/extractors',
        'src/analyzers',
        'src/builders',
        'src/explorers',
        'config',
        'scripts',
        'tests',
        'templates',
        'docs',
    ]
    
    for directory in required:
        if Path(directory).exists():
            print(f"✓ {directory} exists")
        else:
            print(f"✗ {directory} missing")

def main():
    print("=" * 70)
    print("Setting up Thai-Jazz ML Dataset Project")
    print("=" * 70)
    
    print("\n[1/2] Creating directories...")
    create_directories()
    
    print("\n[2/2] Verifying structure...")
    verify_structure()
    
    print("\n" + "=" * 70)
    print("Setup complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
