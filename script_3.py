# Create comprehensive test files
test_app = '''"""
Unit Tests for Feedback Collection Backend API
Tests all API endpoints and functionality
"""

import pytest
import json
import os
from datetime import datetime

# Import the Flask app
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.app import app, FEEDBACK_FILE

@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test data before and after each test"""
    if os.path.exists(FEEDBACK_FILE):
        os.remove(FEEDBACK_FILE)
    yield
    if os.path.exists(FEEDBACK_FILE):
        os.remove(FEEDBACK_FILE)

# ============================================
# Health Check Tests
# ============================================

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'feedback_count' in data

def test_app_info(client):
    """Test application info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'app_name' in data
    assert 'version' in data
    assert 'endpoints' in data

# ============================================
# Feedback Submission Tests
# ============================================

def test_submit_valid_feedback(client):
    """Test submitting valid feedback"""
    feedback_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'feedback': 'This is a test feedback message'
    }
    
    response = client.post('/api/feedback',
                          data=json.dumps(feedback_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Feedback submitted successfully!'
    assert 'id' in data
    assert 'timestamp' in data

def test_submit_feedback_without_name(client):
    """Test submitting feedback without name (should use Anonymous)"""
    feedback_data = {
        'feedback': 'Anonymous feedback'
    }
    
    response = client.post('/api/feedback',
                          data=json.dumps(feedback_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    
    # Verify feedback was saved with Anonymous name
    response = client.get('/api/feedback')
    data = json.loads(response.data)
    assert data['feedback'][0]['name'] == 'Anonymous'

def test_submit_empty_feedback(client):
    """Test submitting empty feedback (should fail)"""
    response = client.post('/api/feedback',
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_submit_feedback_too_long(client):
    """Test submitting feedback that exceeds character limit"""
    feedback_data = {
        'feedback': 'x' * 1001  # Exceeds 1000 character limit
    }
    
    response = client.post('/api/feedback',
                          data=json.dumps(feedback_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'too long' in data['error'].lower()

def test_submit_feedback_invalid_email(client):
    """Test submitting feedback with invalid email"""
    feedback_data = {
        'email': 'invalid-email',
        'feedback': 'Test feedback'
    }
    
    response = client.post('/api/feedback',
                          data=json.dumps(feedback_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'email' in data['error'].lower()

# ============================================
# Feedback Retrieval Tests
# ============================================

def test_get_all_feedback_empty(client):
    """Test getting all feedback when none exists"""
    response = client.get('/api/feedback')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['count'] == 0
    assert data['total'] == 0
    assert len(data['feedback']) == 0

def test_get_all_feedback(client):
    """Test getting all feedback after submission"""
    # Submit multiple feedback entries
    for i in range(3):
        feedback_data = {
            'name': f'User {i}',
            'feedback': f'Feedback {i}'
        }
        client.post('/api/feedback',
                   data=json.dumps(feedback_data),
                   content_type='application/json')
    
    # Get all feedback
    response = client.get('/api/feedback')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['count'] == 3
    assert data['total'] == 3
    assert len(data['feedback']) == 3

def test_get_feedback_with_pagination(client):
    """Test getting feedback with limit and offset"""
    # Submit 5 feedback entries
    for i in range(5):
        feedback_data = {'feedback': f'Feedback {i}'}
        client.post('/api/feedback',
                   data=json.dumps(feedback_data),
                   content_type='application/json')
    
    # Get with limit
    response = client.get('/api/feedback?limit=2')
    data = json.loads(response.data)
    assert data['count'] == 2
    assert data['total'] == 5
    
    # Get with offset
    response = client.get('/api/feedback?offset=2')
    data = json.loads(response.data)
    assert data['count'] == 3

def test_get_feedback_by_id(client):
    """Test getting specific feedback by ID"""
    # Submit feedback
    feedback_data = {
        'name': 'Test User',
        'feedback': 'Specific feedback'
    }
    response = client.post('/api/feedback',
                          data=json.dumps(feedback_data),
                          content_type='application/json')
    
    feedback_id = json.loads(response.data)['id']
    
    # Get feedback by ID
    response = client.get(f'/api/feedback/{feedback_id}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['id'] == feedback_id
    assert data['feedback'] == 'Specific feedback'

def test_get_feedback_by_invalid_id(client):
    """Test getting feedback with non-existent ID"""
    response = client.get('/api/feedback/9999')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data

# ============================================
# Feedback Deletion Tests
# ============================================

def test_delete_feedback(client):
    """Test deleting feedback"""
    # Submit feedback
    feedback_data = {'feedback': 'To be deleted'}
    response = client.post('/api/feedback',
                          data=json.dumps(feedback_data),
                          content_type='application/json')
    
    feedback_id = json.loads(response.data)['id']
    
    # Delete feedback
    response = client.delete(f'/api/feedback/{feedback_id}')
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get(f'/api/feedback/{feedback_id}')
    assert response.status_code == 404

def test_delete_nonexistent_feedback(client):
    """Test deleting non-existent feedback"""
    response = client.delete('/api/feedback/9999')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data

# ============================================
# Statistics Tests
# ============================================

def test_get_statistics(client):
    """Test getting feedback statistics"""
    # Submit various feedback entries
    test_data = [
        {'name': 'User 1', 'email': 'user1@test.com', 'feedback': 'Feedback 1'},
        {'name': 'Anonymous', 'feedback': 'Feedback 2'},
        {'name': 'User 3', 'email': 'user3@test.com', 'feedback': 'Feedback 3'},
    ]
    
    for data in test_data:
        client.post('/api/feedback',
                   data=json.dumps(data),
                   content_type='application/json')
    
    # Get statistics
    response = client.get('/api/stats')
    assert response.status_code == 200
    
    stats = json.loads(response.data)
    assert stats['total_feedback'] == 3
    assert stats['total_with_email'] == 2
    assert 'latest_timestamp' in stats
    assert 'oldest_timestamp' in stats

# ============================================
# Error Handling Tests
# ============================================

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data

def test_405_error(client):
    """Test 405 method not allowed"""
    response = client.put('/api/feedback')
    assert response.status_code == 405

# ============================================
# Integration Tests
# ============================================

def test_full_feedback_workflow(client):
    """Test complete feedback submission and retrieval workflow"""
    # 1. Check initial state
    response = client.get('/api/feedback')
    initial_data = json.loads(response.data)
    assert initial_data['total'] == 0
    
    # 2. Submit feedback
    feedback_data = {
        'name': 'Integration Test User',
        'email': 'integration@test.com',
        'feedback': 'This is an integration test'
    }
    response = client.post('/api/feedback',
                          data=json.dumps(feedback_data),
                          content_type='application/json')
    assert response.status_code == 201
    
    # 3. Verify submission
    response = client.get('/api/feedback')
    data = json.loads(response.data)
    assert data['total'] == 1
    assert data['feedback'][0]['name'] == 'Integration Test User'
    
    # 4. Get statistics
    response = client.get('/api/stats')
    stats = json.loads(response.data)
    assert stats['total_feedback'] == 1
    assert stats['total_with_email'] == 1
    
    # 5. Check health
    response = client.get('/health')
    health = json.loads(response.data)
    assert health['status'] == 'healthy'
    assert health['feedback_count'] == 1

def test_home_page_rendering(client):
    """Test that home page renders correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Feedback Collection System' in response.data
'''

with open(f"{backend_dir}/tests/test_app.py", 'w', encoding='utf-8') as f:
    f.write(test_app)

# Create __init__.py for tests package
with open(f"{backend_dir}/tests/__init__.py", 'w') as f:
    f.write('')

# Create pytest configuration
pytest_ini = '''[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=app
    --cov-report=html
    --cov-report=term-missing

markers =
    unit: Unit tests
    integration: Integration tests
    slow: Tests that take a long time
'''

with open(f"{backend_dir}/pytest.ini", 'w') as f:
    f.write(pytest_ini)

print("✅ Test files created")
print("   - tests/test_app.py (comprehensive unit tests)")
print("   - tests/__init__.py")
print("   - pytest.ini (pytest configuration)")
