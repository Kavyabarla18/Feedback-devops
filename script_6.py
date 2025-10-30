# Create additional utility files and scripts

# Create a run script
run_script = '''#!/bin/bash
# Flask Backend Run Script

echo "================================="
echo "Feedback Collection Backend API"
echo "================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Run the application
echo ""
echo "Starting Flask application..."
echo "Access at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python app/app.py
'''

with open(f"{backend_dir}/run.sh", 'w') as f:
    f.write(run_script)

# Create Windows batch script
run_bat = '''@echo off
REM Flask Backend Run Script for Windows

echo =================================
echo Feedback Collection Backend API
echo =================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\\Scripts\\activate.bat

REM Install dependencies if needed
if not exist "venv\\.installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\\.installed
)

REM Run the application
echo.
echo Starting Flask application...
echo Access at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app\\app.py
'''

with open(f"{backend_dir}/run.bat", 'w') as f:
    f.write(run_bat)

# Create test runner script
test_script = '''#!/bin/bash
# Run all tests with coverage

echo "================================="
echo "Running Backend Tests"
echo "================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install test dependencies
pip install -r requirements-dev.txt > /dev/null 2>&1

# Run tests with coverage
pytest tests/ \\
    --verbose \\
    --cov=app \\
    --cov-report=html \\
    --cov-report=term-missing \\
    --color=yes

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
    echo "Coverage report generated in: htmlcov/index.html"
else
    echo ""
    echo "❌ Some tests failed!"
    exit 1
fi
'''

with open(f"{backend_dir}/test.sh", 'w') as f:
    f.write(test_script)

# Create .gitignore
gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.hypothesis/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Application
feedback_data.json
test_feedback_data.json
*.log

# Environment
.env
.env.local

# Docker
.dockerignore
'''

with open(f"{backend_dir}/.gitignore", 'w') as f:
    f.write(gitignore)

# Create Makefile for common tasks
makefile = '''# Makefile for Feedback Backend

.PHONY: help install run test clean docker-build docker-run

help:
\t@echo "Available commands:"
\t@echo "  make install      - Install dependencies"
\t@echo "  make run          - Run the application"
\t@echo "  make test         - Run tests with coverage"
\t@echo "  make clean        - Clean generated files"
\t@echo "  make docker-build - Build Docker image"
\t@echo "  make docker-run   - Run Docker container"

install:
\t@echo "Installing dependencies..."
\tpip install -r requirements.txt
\tpip install -r requirements-dev.txt

run:
\t@echo "Starting Flask application..."
\tpython app/app.py

test:
\t@echo "Running tests..."
\tpytest tests/ --verbose --cov=app --cov-report=html --cov-report=term-missing

clean:
\t@echo "Cleaning generated files..."
\trm -rf __pycache__ .pytest_cache htmlcov .coverage
\trm -rf app/__pycache__ tests/__pycache__ config/__pycache__
\trm -f feedback_data.json test_feedback_data.json
\tfind . -type d -name "*.egg-info" -exec rm -rf {} +
\tfind . -type f -name "*.pyc" -delete

docker-build:
\t@echo "Building Docker image..."
\tdocker build -t feedback-backend .

docker-run:
\t@echo "Running Docker container..."
\tdocker run -d -p 5000:5000 --name feedback-api feedback-backend

format:
\t@echo "Formatting code..."
\tblack app/ tests/
\tflake8 app/ tests/

lint:
\t@echo "Linting code..."
\tflake8 app/ tests/
'''

with open(f"{backend_dir}/Makefile", 'w') as f:
    f.write(makefile)

# Make shell scripts executable
import stat
for script in ['run.sh', 'test.sh']:
    script_path = f"{backend_dir}/{script}"
    st = os.stat(script_path)
    os.chmod(script_path, st.st_mode | stat.S_IEXEC)

print("✅ Utility files created")
print("   - run.sh (Linux/Mac run script)")
print("   - run.bat (Windows run script)")
print("   - test.sh (Test runner script)")
print("   - .gitignore (Git ignore rules)")
print("   - Makefile (Common tasks)")
