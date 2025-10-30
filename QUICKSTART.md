# Quick Start Guide 🚀

## 5-Minute Setup

### 1. Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### 2. Run the Application (1 min)
```bash
python app/app.py
```

### 3. Test the API (2 min)

Open browser: http://localhost:5000

Or use curl:
```bash
# Submit feedback
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","feedback":"Hello World!"}'

# Get all feedback
curl http://localhost:5000/api/feedback

# Health check
curl http://localhost:5000/health
```

### 4. Run Tests (1 min)
```bash
pytest
```

## Docker Quick Start

```bash
# Build and run
docker build -t feedback-backend .
docker run -p 5000:5000 feedback-backend

# Access at http://localhost:5000
```

## Common Commands

```bash
# Development with auto-reload
FLASK_ENV=development python app/app.py

# Production with Gunicorn
gunicorn --bind 0.0.0.0:5000 app.app:app

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black app/

# Check code quality
flake8 app/
```

That's it! You're ready to go! 🎉
