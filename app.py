
from flask import Flask, render_template, jsonify, request
from src.dataset_explorer import DatasetExplorer
from src.phin_dataset_builder import PhinDatasetBuilder
import json
from pathlib import Path

app = Flask(__name__)
explorer = DatasetExplorer()

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/api/summary')
def get_summary():
    """Get dataset summary statistics."""
    stats = explorer.get_feature_statistics()
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
def thai_music_pages():
    """Get Thai music pages."""
    df = explorer.get_thai_music_pages()
    return jsonify(df.to_dict('records')[:100])

@app.route('/api/jazz-pages')
def jazz_pages():
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
    return jsonify(df.to_dict('records'))

@app.route('/api/phin/lai-patterns')
def phin_lai():
    """Get Phin lai patterns."""
    builder = PhinDatasetBuilder()
    df = builder.build_lai_dataset()
    return jsonify(df.to_dict('records'))

@app.route('/api/phin/artists')
def phin_artists():
    """Get Phin artists."""
    builder = PhinDatasetBuilder()
    df = builder.build_artist_dataset()
    return jsonify(df.to_dict('records'))

@app.route('/api/chapters')
def get_chapters():
    """Get chapter information."""
    chapters = explorer.get_chapter_info()
    return jsonify(chapters)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
