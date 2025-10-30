# Create Dockerfile and configuration files
dockerfile = '''# Multi-stage Dockerfile for Flask Backend
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app/ ./app/

# Create data directory
RUN mkdir -p /app/data

# Set environment variables
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.app:app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app.app:app"]
'''

with open(f"{backend_dir}/Dockerfile", 'w') as f:
    f.write(dockerfile)

# Create .dockerignore
dockerignore = '''__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
*.egg-info
dist/
build/
tests/
*.md
.gitignore
'''

with open(f"{backend_dir}/.dockerignore", 'w') as f:
    f.write(dockerignore)

# Create environment configuration
env_example = '''# Flask Configuration
FLASK_APP=app.app:app
FLASK_ENV=production

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Application Settings
MAX_CONTENT_LENGTH=16777216
FEEDBACK_FILE=feedback_data.json

# CORS Settings
CORS_ORIGINS=*

# Logging
LOG_LEVEL=INFO
'''

with open(f"{backend_dir}/.env.example", 'w') as f:
    f.write(env_example)

# Create configuration file
config_py = '''"""
Configuration settings for the Flask application
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # File storage
    FEEDBACK_FILE = os.environ.get('FEEDBACK_FILE', 'feedback_data.json')
    
    # Request limits
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # JSON settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    FEEDBACK_FILE = 'test_feedback_data.json'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
'''

with open(f"{backend_dir}/config/config.py", 'w') as f:
    f.write(config_py)

with open(f"{backend_dir}/config/__init__.py", 'w') as f:
    f.write('')

print("✅ Docker and configuration files created")
print("   - Dockerfile (multi-stage build)")
print("   - .dockerignore")
print("   - .env.example (environment variables template)")
print("   - config/config.py (application configuration)")
