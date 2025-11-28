from flask import Flask, render_template, jsonify, request
from src.dataset_explorer import DatasetExplorer
from src.phin_dataset_builder import PhinDatasetBuilder
import json
from pathlib import Path
import numpy as np
import pandas as pd

app = Flask(__name__)
explorer = DatasetExplorer()

def convert_to_serializable(obj):
    """Convert numpy/pandas types to Python native types for JSON serialization."""
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/api/summary')
def get_summary():
    """Get dataset summary statistics."""
    stats = explorer.get_feature_statistics()
    stats = convert_to_serializable(stats)
    return jsonify(stats)

@app.route('/api/search')
def search():
    """Search content across all pages."""
    query = request.args.get('q', '')
    case_sensitive = request.args.get('case_sensitive', 'false') == 'true'

    if not query:
        return jsonify([])

    results = explorer.search_content(query, case_sensitive)
    return jsonify(results[:50])  # Limit to 50 results

@app.route('/api/page/<int:page_num>')
def get_page(page_num):
    """Get content for a specific page."""
    content = explorer.get_page_content(page_num)
    return jsonify({'page': page_num, 'content': content})

@app.route('/api/thai-music-pages')
def get_thai_pages():
    """Get Thai music pages."""
    df = explorer.get_thai_music_pages()
    return jsonify(df.to_dict('records')[:100])

@app.route('/api/jazz-pages')
def get_jazz_pages():
    """Get Jazz pages."""
    df = explorer.get_jazz_pages()
    return jsonify(df.to_dict('records')[:100])

@app.route('/api/fusion-pages')
def fusion_pages():
    """Get fusion pages."""
    df = explorer.get_fusion_pages()
    return jsonify(df.to_dict('records')[:100])

@app.route('/api/ml-pages')
def ml_pages():
    """Get ML pages."""
    df = explorer.get_ml_pages()
    return jsonify(df.to_dict('records')[:100])

@app.route('/api/feature-catalog')
def feature_catalog():
    """Get feature catalog."""
    df = explorer.get_feature_catalog()
    return jsonify(df.to_dict('records'))

@app.route('/api/schema')
def get_schema():
    """Get ML dataset schema."""
    return jsonify(explorer.get_schema())

@app.route('/api/phin/tuning')
def phin_tuning():
    """Get Phin tuning systems."""
    builder = PhinDatasetBuilder()
    df = builder.build_tuning_dataset()
    # Convert DataFrame to a list of dictionaries, handling potential int64 issues
    records = df.to_dict('records')
    return jsonify([convert_to_serializable(record) for record in records])

@app.route('/api/phin/lai-patterns')
def phin_lai():
    """Get Phin lai patterns."""
    builder = PhinDatasetBuilder()
    df = builder.build_lai_dataset()
    # Convert DataFrame to a list of dictionaries, handling potential int64 issues
    records = df.to_dict('records')
    return jsonify([convert_to_serializable(record) for record in records])

@app.route('/api/phin/artists')
def phin_artists():
    """Get Phin artists."""
    builder = PhinDatasetBuilder()
    df = builder.build_artist_dataset()
    # Convert DataFrame to a list of dictionaries, handling potential int64 issues
    records = df.to_dict('records')
    return jsonify([convert_to_serializable(record) for record in records])

@app.route('/api/chapters')
def get_chapters():
    """Get chapter information."""
    chapters = explorer.get_chapter_info()
    # Ensure chapters are serializable, as they might contain numpy types
    serializable_chapters = convert_to_serializable(chapters)
    return jsonify(serializable_chapters)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)