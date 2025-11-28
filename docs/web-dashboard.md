
# Web Dashboard

## Overview

The Thai-Jazz ML Dataset project includes an interactive web dashboard built with Flask for exploring the extracted datasets.

## Starting the Dashboard

```bash
python app.py
```

Or click the **Run** button in Replit (configured to run the Web Dashboard workflow).

The dashboard will be available at `http://0.0.0.0:5000`

## Features

### Dataset Overview

The main page displays:
- Total pages analyzed
- Number of Thai music pages
- Number of Jazz pages
- Number of fusion pages
- Feature distribution statistics

### Thai Music Content

Browse pages containing Thai traditional music content:
- Thai modes (thang)
- Lai patterns
- Phin instrument references
- Traditional scales

### Jazz Content

Explore Jazz-related content:
- Jazz harmony and chords
- Improvisation techniques
- Jazz scales and modes
- Cross-cultural fusion examples

### Phin Dataset

View the specialized Phin instrument dataset:
- Tuning systems (13 configurations)
- Lai patterns (5 traditional patterns)
- Master artists
- Playing techniques

### Musical Notation

Browse extracted musical notation:
- Western notation (C, D, E, etc.)
- Scale degrees (1, 2, 3, etc.)
- Thai lai modes
- Chord progressions
- Interval patterns

## API Endpoints

All data is available via REST API:

| Endpoint | Description |
|----------|-------------|
| `/api/summary` | Dataset summary statistics |
| `/api/thai-music-pages` | Thai music pages |
| `/api/jazz-pages` | Jazz pages |
| `/api/phin-lai-patterns` | Phin lai patterns |
| `/api/notations` | Musical notations |
| `/api/compositions` | Musical compositions |
| `/api/notation-summary` | Notation summary |

## Usage Examples

### Fetch Summary Data

```javascript
fetch('/api/summary')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Get Thai Music Pages

```javascript
fetch('/api/thai-music-pages')
  .then(response => response.json())
  .then(pages => console.log(pages));
```

### Access Phin Dataset

```javascript
fetch('/api/phin-lai-patterns')
  .then(response => response.json())
  .then(patterns => console.log(patterns));
```

## Customization

The dashboard template is located at `templates/index.html`. You can customize:
- Layout and styling
- Data visualizations
- Navigation
- Content sections

Static assets (CSS, JavaScript, images) go in the `static/` directory.

## Troubleshooting

If the dashboard shows errors loading data:

1. Ensure datasets have been generated:
   ```bash
   python main.py
   ```

2. Check that output files exist:
   ```bash
   ls -la output/
   ```

3. Verify Flask is running on the correct port (5000):
   ```bash
   # Check console output for "Running on http://0.0.0.0:5000"
   ```

4. Review console logs in the browser developer tools for specific errors
