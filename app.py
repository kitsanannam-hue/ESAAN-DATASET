from flask import Flask, render_template, jsonify, request, Response
from src.explorers.dataset_explorer import DatasetExplorer
from src.builders.phin_dataset_builder import PhinDatasetBuilder
from src.ai_analyzer import (
    analyze_feature_connection, 
    generate_fusion_suggestion, 
    explain_musical_concept,
    compare_scale_systems,
    is_available as ai_available
)
import json
import csv
import io
from pathlib import Path
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
explorer = DatasetExplorer()

def convert_to_serializable(obj):
    """Convert numpy/pandas types to Python native types for JSON serialization."""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
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

@app.route('/api/phin-lai-patterns')
def phin_lai_patterns():
    """Get Phin lai patterns."""
    try:
        phin_path = Path('output/phin_dataset/phin_lai_patterns.json')
        if phin_path.exists():
            with open(phin_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(convert_to_serializable(data))
        else:
            return jsonify({'error': 'Phin lai patterns not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/music-notation')
def music_notation():
    """Get all musical notation."""
    try:
        notation_path = Path('output/music_notation_dataset/musical_notation.json')
        if notation_path.exists():
            with open(notation_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data[:100])  # Limit to 100 for performance
        else:
            return jsonify({'error': 'Notation dataset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compositions')
def compositions():
    """Get musical compositions."""
    try:
        comp_path = Path('output/music_notation_dataset/compositions.json')
        if comp_path.exists():
            with open(comp_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'error': 'Compositions not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notation-summary')
def notation_summary():
    """Get notation dataset summary."""
    try:
        summary_path = Path('output/music_notation_dataset/notation_summary.json')
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'error': 'Summary not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai/status')
def ai_status():
    """Check if AI analysis is available."""
    return jsonify({
        'available': ai_available(),
        'message': 'AI analysis ready' if ai_available() else 'Add OPENAI_API_KEY to enable AI analysis'
    })


@app.route('/api/ai/analyze-feature', methods=['POST'])
def ai_analyze_feature():
    """Analyze a musical feature using AI."""
    feature_data = request.json
    if not feature_data:
        return jsonify({'error': 'No feature data provided'}), 400
    
    result = analyze_feature_connection(feature_data)
    return jsonify(result)


@app.route('/api/ai/fusion-suggestion', methods=['POST'])
def ai_fusion_suggestion():
    """Generate fusion composition suggestions."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    thai_features = data.get('thai_features', [])
    jazz_style = data.get('jazz_style', 'Modal Jazz')
    
    result = generate_fusion_suggestion(thai_features, jazz_style)
    return jsonify(result)


@app.route('/api/ai/explain', methods=['POST'])
def ai_explain():
    """Explain a musical concept."""
    data = request.json
    if not data or 'concept' not in data:
        return jsonify({'error': 'No concept provided'}), 400
    
    concept = data['concept']
    context = data.get('context', 'Thai-Jazz fusion')
    
    result = explain_musical_concept(concept, context)
    return jsonify(result)


@app.route('/api/ai/compare-scales', methods=['POST'])
def ai_compare_scales():
    """Compare Thai and Jazz scales."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    thai_scale = data.get('thai_scale', 'Lai Yai')
    jazz_scale = data.get('jazz_scale', 'Dorian')
    
    result = compare_scale_systems(thai_scale, jazz_scale)
    return jsonify(result)


@app.route('/api/visualization/category-distribution')
def viz_category_distribution():
    """Get category distribution for visualization."""
    try:
        features_path = Path('output/ml_dataset/thai_jazz_features.json')
        if features_path.exists():
            with open(features_path, 'r', encoding='utf-8') as f:
                features = json.load(f)
            
            categories = {}
            for feature in features:
                cat = feature.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            return jsonify({
                'labels': list(categories.keys()),
                'values': list(categories.values()),
                'colors': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
            })
        return jsonify({'error': 'Features not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualization/regional-coverage')
def viz_regional_coverage():
    """Get regional coverage for visualization."""
    try:
        complete_path = Path('output/ml_dataset/complete_ml_dataset.json')
        if complete_path.exists():
            with open(complete_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            regions = data.get('metadata', {}).get('regional_coverage', [])
            region_counts = {r: 0 for r in regions}
            
            for feature in data.get('features', []):
                for region in regions:
                    if region.lower() in str(feature).lower():
                        region_counts[region] += 1
            
            return jsonify({
                'labels': list(region_counts.keys()),
                'values': list(region_counts.values()),
                'colors': ['#22c55e', '#3b82f6', '#f59e0b', '#ef4444']
            })
        return jsonify({'error': 'Dataset not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualization/notation-types')
def viz_notation_types():
    """Get notation type distribution for visualization."""
    try:
        summary_path = Path('output/music_notation_dataset/notation_summary.json')
        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            by_type = data.get('by_type', {})
            return jsonify({
                'labels': [k.replace('_', ' ').title() for k in by_type.keys()],
                'values': list(by_type.values()),
                'colors': ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']
            })
        return jsonify({'error': 'Summary not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/visualization/page-analysis')
def viz_page_analysis():
    """Get page analysis statistics."""
    stats = explorer.get_feature_statistics()
    stats = convert_to_serializable(stats)
    
    return jsonify({
        'labels': ['Thai Music', 'Jazz', 'Fusion', 'ML Content'],
        'values': [
            stats.get('thai_music_count', 0),
            stats.get('jazz_count', 0),
            stats.get('fusion_count', 0),
            stats.get('ml_count', 0)
        ],
        'colors': ['#667eea', '#f59e0b', '#10b981', '#ef4444']
    })


@app.route('/api/features/filter')
def filter_features():
    """Filter features by category and search term."""
    category = request.args.get('category', '')
    search = request.args.get('search', '').lower()
    
    try:
        features_path = Path('output/ml_dataset/thai_jazz_features.json')
        if features_path.exists():
            with open(features_path, 'r', encoding='utf-8') as f:
                features = json.load(f)
            
            filtered = features
            
            if category:
                filtered = [f for f in filtered if f.get('category', '') == category]
            
            if search:
                filtered = [f for f in filtered if 
                    search in f.get('name', '').lower() or
                    search in f.get('description', '').lower() or
                    search in f.get('thai_term', '').lower()]
            
            return jsonify(filtered)
        return jsonify({'error': 'Features not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/features/categories')
def get_categories():
    """Get all unique feature categories."""
    try:
        features_path = Path('output/ml_dataset/thai_jazz_features.json')
        if features_path.exists():
            with open(features_path, 'r', encoding='utf-8') as f:
                features = json.load(f)
            
            categories = list(set(f.get('category', 'unknown') for f in features))
            return jsonify(sorted(categories))
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/features/<format>')
def export_features(format):
    """Export features dataset in specified format."""
    try:
        features_path = Path('output/ml_dataset/thai_jazz_features.json')
        if not features_path.exists():
            return jsonify({'error': 'Features not found'}), 404
        
        with open(features_path, 'r', encoding='utf-8') as f:
            features = json.load(f)
        
        if format == 'json':
            return Response(
                json.dumps(features, indent=2, ensure_ascii=False),
                mimetype='application/json',
                headers={'Content-Disposition': 'attachment;filename=thai_jazz_features.json'}
            )
        elif format == 'csv':
            output = io.StringIO()
            if features:
                writer = csv.DictWriter(output, fieldnames=features[0].keys())
                writer.writeheader()
                writer.writerows(features)
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment;filename=thai_jazz_features.csv'}
            )
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/phin/<format>')
def export_phin(format):
    """Export Phin dataset in specified format."""
    try:
        phin_path = Path('output/phin_dataset/phin_dataset_complete.json')
        if not phin_path.exists():
            return jsonify({'error': 'Phin dataset not found'}), 404
        
        with open(phin_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if format == 'json':
            return Response(
                json.dumps(data, indent=2, ensure_ascii=False),
                mimetype='application/json',
                headers={'Content-Disposition': 'attachment;filename=phin_dataset.json'}
            )
        elif format == 'csv':
            output = io.StringIO()
            lai_patterns = data.get('lai_patterns', [])
            if lai_patterns:
                writer = csv.DictWriter(output, fieldnames=lai_patterns[0].keys())
                writer.writeheader()
                writer.writerows(lai_patterns)
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': 'attachment;filename=phin_lai_patterns.csv'}
            )
        else:
            return jsonify({'error': 'Unsupported format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/complete/<format>')
def export_complete(format):
    """Export complete ML dataset."""
    try:
        complete_path = Path('output/ml_dataset/complete_ml_dataset.json')
        if not complete_path.exists():
            return jsonify({'error': 'Dataset not found'}), 404
        
        with open(complete_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if format == 'json':
            return Response(
                json.dumps(data, indent=2, ensure_ascii=False),
                mimetype='application/json',
                headers={'Content-Disposition': 'attachment;filename=complete_ml_dataset.json'}
            )
        else:
            return jsonify({'error': 'Only JSON format supported for complete dataset'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/relationships')
def feature_relationships():
    """Get relationships between Thai and Jazz features."""
    relationships = [
        {
            'thai_feature': 'Thao (เทา)',
            'jazz_equivalent': 'Augmentation/Diminution',
            'connection': 'Both use rhythmic transformation of melodic material',
            'fusion_tip': 'Apply thao principles to Giant Steps changes'
        },
        {
            'thai_feature': 'Luk Mot (ลูกโมท)',
            'jazz_equivalent': 'Blues Riff / Turnaround',
            'connection': 'Closing phrases that signal section endings',
            'fusion_tip': 'Use luk mot patterns as jazz turnarounds'
        },
        {
            'thai_feature': 'Lai Yai (ลายใหญ่)',
            'jazz_equivalent': 'A Minor Pentatonic / Blues Scale',
            'connection': 'Similar intervallic structure and melodic function',
            'fusion_tip': 'Substitute blues licks with lai yai patterns'
        },
        {
            'thai_feature': 'Sieng Sep (เสียงเซ็บ)',
            'jazz_equivalent': 'Suspended Chords / Drones',
            'connection': 'Creates harmonic suspension and modal feel',
            'fusion_tip': 'Use khaen drone technique over jazz sus chords'
        },
        {
            'thai_feature': 'Nathap Propkai',
            'jazz_equivalent': 'Polyrhythmic Patterns',
            'connection': 'Layered rhythmic cycles',
            'fusion_tip': 'Adapt Thai rhythmic cycles for drum set grooves'
        },
        {
            'thai_feature': 'Ti Kep (ตีเก็บ)',
            'jazz_equivalent': 'Vibraphone Runs',
            'connection': '8-note melodic runs on mallet instruments',
            'fusion_tip': 'Apply ranad ek technique to jazz vibraphone'
        },
        {
            'thai_feature': 'Thang Kro (ทางกรอ)',
            'jazz_equivalent': 'Tremolo',
            'connection': 'Sustained pitch with rapid oscillation',
            'fusion_tip': 'Use in string and wind sections for Thai color'
        },
        {
            'thai_feature': 'Luk Yon (ลูกย้อน)',
            'jazz_equivalent': 'Pedal Point',
            'connection': 'Sustained bass note under changing harmony',
            'fusion_tip': 'Create modal jazz sections with Thai pedal tones'
        }
    ]
    return jsonify(relationships)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)