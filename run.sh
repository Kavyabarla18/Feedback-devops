#!/bin/bash
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
