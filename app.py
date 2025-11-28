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

@app.route('/api/phin/techniques')
def phin_techniques():
    """Get Phin techniques."""
    builder = PhinDatasetBuilder()
    df = builder.build_technique_dataset()
    records = df.to_dict('records')
    return jsonify([convert_to_serializable(record) for record in records])

@app.route('/api/phin-dataset')
def phin_dataset():
    """Get complete Phin dataset."""
    try:
        phin_path = Path('output/phin_dataset/phin_dataset_complete.json')
        if phin_path.exists():
            with open(phin_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(convert_to_serializable(data))
        else:
            return jsonify({'error': 'Phin dataset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chapters')
def get_chapters():
    """Get chapter information."""
    chapters = explorer.get_chapter_info()
    # Ensure chapters are serializable, as they might contain numpy types
    serializable_chapters = convert_to_serializable(chapters)
    return jsonify(serializable_chapters)

@app.route('/api/ml-dataset/features')
def ml_features():
    """Get Thai-Jazz ML features."""
    try:
        features_path = Path('output/ml_dataset/thai_jazz_features.json')
        if features_path.exists():
            with open(features_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'error': 'ML features not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ml-dataset/hybridization')
def ml_hybridization():
    """Get hybridization techniques."""
    try:
        hybrid_path = Path('output/ml_dataset/hybridization_techniques.json')
        if hybrid_path.exists():
            with open(hybrid_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'error': 'Hybridization data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ml-dataset/scale-mapping')
def ml_scale_mapping():
    """Get Thai-Jazz scale mappings."""
    try:
        scale_path = Path('output/ml_dataset/thai_jazz_scale_mapping.json')
        if scale_path.exists():
            with open(scale_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'error': 'Scale mapping not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ml-dataset/complete')
def ml_complete():
    """Get complete ML dataset."""
    try:
        complete_path = Path('output/ml_dataset/complete_ml_dataset.json')
        if complete_path.exists():
            with open(complete_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'error': 'Complete dataset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)