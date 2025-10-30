# Create requirements.txt with all dependencies
requirements = '''# Flask Framework
Flask==2.3.3
Werkzeug==2.3.7

# CORS Support
Flask-CORS==4.0.0

# Environment Variables
python-dotenv==1.0.0

# Production Server
gunicorn==21.2.0

# Testing
pytest==7.4.2
pytest-flask==1.2.0
pytest-cov==4.1.0

# Code Quality
flake8==6.1.0
black==23.9.1

# Additional Utilities
python-dateutil==2.8.2
'''

with open(f"{backend_dir}/requirements.txt", 'w') as f:
    f.write(requirements)

# Create development requirements
dev_requirements = '''# Include base requirements
-r requirements.txt

# Development Tools
ipython==8.16.1
ipdb==0.13.13

# Testing & Coverage
pytest-watch==4.2.0
coverage==7.3.2

# Code Formatting
autopep8==2.0.4

# Documentation
sphinx==7.2.6
'''

with open(f"{backend_dir}/requirements-dev.txt", 'w') as f:
    f.write(dev_requirements)

print("✅ Requirements files created")
print("   - requirements.txt (production dependencies)")
print("   - requirements-dev.txt (development dependencies)")
