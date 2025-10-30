"""
Feedback Collection Backend API
Flask REST API for collecting and managing user feedback
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)

CORS(app)

# Configuration
FEEDBACK_FILE = "feedback_data.json"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# ============================================
# Helper Functions
# ============================================

def load_feedback():
    """
    Load feedback from JSON file
    Returns: List of feedback entries
    """
    if not os.path.exists(FEEDBACK_FILE):
        return []
    try:
        with open(FEEDBACK_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading feedback: {e}")
        return []

def save_feedback(feedback_list):
    """
    Save feedback to JSON file
    Args:
        feedback_list: List of feedback entries to save
    """
    try:
        with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
            json.dump(feedback_list, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return False

def validate_feedback(data):
    """
    Validate feedback data
    Args:
        data: Dictionary containing feedback data
    Returns: Tuple (is_valid, error_message)
    """
    if not data:
        return False, "No data provided"

    if 'feedback' not in data or not data['feedback']:
        return False, "Feedback content is required"

    if len(data['feedback']) > 1000:
        return False, "Feedback text too long (max 1000 characters)"

    if 'name' in data and len(data.get('name', '')) > 100:
        return False, "Name too long (max 100 characters)"

    if 'email' in data and data.get('email'):
        email = data['email']
        if '@' not in email or '.' not in email.split('@')[-1]:
            return False, "Invalid email format"

    return True, None

def error_handler(func):
    """Decorator for consistent error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    return wrapper

# ============================================
# Routes - Web Interface & Static Files
# ============================================

@app.route('/')
def home():
    """
    Home page showing recent feedback
    Returns: Rendered HTML template
    """
    feedback_list = load_feedback()
    # Get last 20 feedback entries, most recent first
    recent_feedback = feedback_list[-20:] if len(feedback_list) > 20 else feedback_list
    recent_feedback.reverse()

    return render_template('index.html', 
                         feedback_list=recent_feedback,
                         total_count=len(feedback_list))

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files from static/css directory"""
    return send_from_directory('static/css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files from static/js directory"""
    return send_from_directory('static/js', filename)

# ============================================
# Routes - API Endpoints
# ============================================

@app.route('/api/feedback', methods=['POST'])
@error_handler
def submit_feedback():
    """
    Submit new feedback
    Request Body:
        {
            "name": "User Name (optional)",
            "email": "user@email.com (optional)",
            "feedback": "Feedback text (required)",
            "rating": 1-5 (optional)
        }
    Returns: JSON response with success/error message
    """
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate feedback
        is_valid, error_msg = validate_feedback(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Load existing feedback
        feedback_list = load_feedback()

        # Create feedback entry
        feedback_entry = {
            'id': len(feedback_list) + 1,
            'feedback': data['feedback'].strip(),
            'name': data.get('name', 'Anonymous').strip() or 'Anonymous',
            'email': data.get('email', '').strip(),
            'rating': data.get('rating', 0),
            'timestamp': datetime.now().isoformat(),
            'ip_address': request.remote_addr
        }

        # Add to list and save
        feedback_list.append(feedback_entry)
        if not save_feedback(feedback_list):
            return jsonify({'error': 'Failed to save feedback'}), 500

        return jsonify({
            'message': 'Feedback submitted successfully!',
            'id': feedback_entry['id'],
            'timestamp': feedback_entry['timestamp']
        }), 201

    except Exception as e:
        return jsonify({'error': f'Error processing feedback: {str(e)}'}), 500

@app.route('/api/feedback', methods=['GET'])
@error_handler
def get_all_feedback():
    """
    Get all feedback entries
    Query Parameters:
        limit: Maximum number of entries to return (default: all)
        offset: Number of entries to skip (default: 0)
    Returns: JSON array of feedback entries
    """
    feedback_list = load_feedback()

    # Handle pagination
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int, default=0)

    if offset > 0:
        feedback_list = feedback_list[offset:]

    if limit and limit > 0:
        feedback_list = feedback_list[:limit]

    return jsonify({
        'feedback': feedback_list,
        'count': len(feedback_list),
        'total': len(load_feedback())
    }), 200

@app.route('/api/feedback/<int:feedback_id>', methods=['GET'])
@error_handler
def get_feedback_by_id(feedback_id):
    """
    Get specific feedback by ID
    Args:
        feedback_id: Feedback ID
    Returns: JSON feedback entry or error
    """
    feedback_list = load_feedback()
    feedback = next((f for f in feedback_list if f.get('id') == feedback_id), None)

    if feedback:
        return jsonify(feedback), 200
    return jsonify({'error': 'Feedback not found'}), 404

@app.route('/api/feedback/<int:feedback_id>', methods=['DELETE'])
@error_handler
def delete_feedback(feedback_id):
    """
    Delete feedback by ID
    Args:
        feedback_id: Feedback ID to delete
    Returns: Success/error message
    """
    feedback_list = load_feedback()
    original_count = len(feedback_list)

    feedback_list = [f for f in feedback_list if f.get('id') != feedback_id]

    if len(feedback_list) == original_count:
        return jsonify({'error': 'Feedback not found'}), 404

    if save_feedback(feedback_list):
        return jsonify({'message': 'Feedback deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete feedback'}), 500

@app.route('/api/stats', methods=['GET'])
@error_handler
def get_statistics():
    """
    Get feedback statistics
    Returns: JSON with various statistics
    """
    feedback_list = load_feedback()

    # Calculate rating statistics
    ratings = [f.get('rating', 0) for f in feedback_list if f.get('rating', 0) > 0]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0

    stats = {
        'total_feedback': len(feedback_list),
        'total_with_email': sum(1 for f in feedback_list if f.get('email')),
        'total_anonymous': sum(1 for f in feedback_list if f.get('name') == 'Anonymous'),
        'average_rating': round(avg_rating, 2),
        'total_rated': len(ratings),
        'latest_timestamp': feedback_list[-1]['timestamp'] if feedback_list else None,
        'oldest_timestamp': feedback_list[0]['timestamp'] if feedback_list else None
    }

    return jsonify(stats), 200

# ============================================
# Health & Monitoring
# ============================================

@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring
    Returns: JSON with health status
    """
    try:
        # Check if we can read/write to storage
        feedback_list = load_feedback()

        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'feedback_count': len(feedback_list),
            'storage_accessible': True
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 503

@app.route('/api/info')
def app_info():
    """
    Application information endpoint
    Returns: JSON with app metadata
    """
    return jsonify({
        'app_name': 'Feedback Collection API',
        'version': '1.0.0',
        'description': 'REST API for collecting and managing user feedback',
        'endpoints': {
            'GET /': 'Web interface',
            'POST /api/feedback': 'Submit new feedback',
            'GET /api/feedback': 'Get all feedback (supports pagination)',
            'GET /api/feedback/<id>': 'Get feedback by ID',
            'DELETE /api/feedback/<id>': 'Delete feedback by ID',
            'GET /api/stats': 'Get feedback statistics',
            'GET /health': 'Health check',
            'GET /api/info': 'API information'
        }
    }), 200

# ============================================
# Error Handlers
# ============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ============================================
# Main Application Entry Point
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print("Feedback Collection Backend API")
    print("=" * 60)
    print(f"Starting server on http://0.0.0.0:5000")
    print(f"Storage file: {FEEDBACK_FILE}")
    print("=" * 60)

    app.run(host='0.0.0.0', port=5000, debug=True) 

