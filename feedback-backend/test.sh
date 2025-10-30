#!/bin/bash
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
pytest tests/ \
    --verbose \
    --cov=app \
    --cov-report=html \
    --cov-report=term-missing \
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
