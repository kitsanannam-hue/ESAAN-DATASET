"""
AI-powered music analysis using OpenAI.
Provides insights about Thai-Jazz cross-cultural musical connections.
"""

import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user


def get_api_key():
    """Get OpenAI API key from environment (checked dynamically)."""
    return os.environ.get("OPENAI_API_KEY")


def get_client():
    """Get OpenAI client if API key is available."""
    api_key = get_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def analyze_feature_connection(feature_data):
    """Analyze the connection between Thai and Jazz elements for a feature."""
    client = get_client()
    if not client:
        return {
            "error": "OpenAI API key not configured",
            "suggestion": "Add your OPENAI_API_KEY to enable AI analysis"
        }
    
    try:
        prompt = f"""You are an expert in cross-cultural musicology, specializing in Thai traditional music and Jazz fusion.

Analyze this Thai musical feature and explain its connection to Jazz:

Feature: {feature_data.get('name', 'Unknown')}
Thai Term: {feature_data.get('thai_term', 'N/A')}
Category: {feature_data.get('category', 'N/A')}
Description: {feature_data.get('description', 'N/A')}
Jazz Application: {feature_data.get('application', 'N/A')}

Provide a detailed analysis in JSON format with these fields:
- thai_context: Cultural and musical context in Thai tradition
- jazz_parallel: Similar concepts or techniques in Jazz
- fusion_potential: How these can be combined creatively
- recommended_instruments: Best instruments for this fusion
- listening_examples: Suggested listening for understanding this technique"""

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a cross-cultural music expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=1024
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def generate_fusion_suggestion(thai_features, jazz_style):
    """Generate creative fusion suggestions based on Thai features and Jazz style."""
    client = get_client()
    if not client:
        return {
            "error": "OpenAI API key not configured",
            "suggestion": "Add your OPENAI_API_KEY to enable AI analysis"
        }
    
    try:
        prompt = f"""You are a composer specializing in Thai-Jazz fusion music.

Given these Thai musical elements:
{json.dumps(thai_features, indent=2)}

And this Jazz style: {jazz_style}

Create a creative fusion composition concept in JSON format:
- title: A creative title for the piece
- concept: Overall artistic concept
- thai_elements: Which Thai elements to feature and how
- jazz_elements: Jazz techniques to incorporate
- structure: Suggested musical structure
- arrangement_tips: Tips for arranging
- mood: The emotional quality of the piece"""

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are an innovative composer. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=1024
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def explain_musical_concept(concept_name, context="Thai-Jazz fusion"):
    """Explain a musical concept in the context of Thai-Jazz fusion."""
    client = get_client()
    if not client:
        return {
            "error": "OpenAI API key not configured",
            "suggestion": "Add your OPENAI_API_KEY to enable AI analysis"
        }
    
    try:
        prompt = f"""Explain the musical concept "{concept_name}" in the context of {context}.

Provide a clear, educational explanation in JSON format:
- definition: Clear definition of the concept
- thai_usage: How it's used in Thai traditional music
- jazz_usage: How it's used in Jazz
- fusion_application: How to apply it in Thai-Jazz fusion
- examples: Specific musical examples
- practice_tips: Tips for musicians learning this concept"""

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a music education expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=1024
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def compare_scale_systems(thai_scale, jazz_scale):
    """Compare Thai and Jazz scale systems."""
    client = get_client()
    if not client:
        return {
            "error": "OpenAI API key not configured",
            "suggestion": "Add your OPENAI_API_KEY to enable AI analysis"
        }
    
    try:
        prompt = f"""Compare these two scale systems:

Thai Scale: {thai_scale}
Jazz Scale: {jazz_scale}

Provide a detailed comparison in JSON format:
- similarities: Common elements between the scales
- differences: Key differences in structure and use
- harmonic_implications: Chord progressions that work with each
- melodic_characteristics: Melodic tendencies of each scale
- fusion_possibilities: Creative ways to combine them
- example_progression: A sample chord progression using both"""

        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a music theory expert. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_completion_tokens=1024
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}


def is_available():
    """Check if AI analysis is available (checked dynamically)."""
    return get_api_key() is not None
