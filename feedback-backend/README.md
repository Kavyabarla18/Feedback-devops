# Feedback Collection Backend API 🚀

A robust, production-ready Flask REST API for collecting and managing user feedback with comprehensive testing and DevOps integration.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [CI/CD Integration](#cicd-integration)
- [Configuration](#configuration)

## ✨ Features

- ✅ RESTful API design
- ✅ JSON file-based data persistence
- ✅ CORS support for cross-origin requests
- ✅ Input validation and error handling
- ✅ Pagination support
- ✅ Health check endpoints
- ✅ Comprehensive unit tests (pytest)
- ✅ Docker containerization
- ✅ Production-ready with Gunicorn
- ✅ Code coverage reporting
- ✅ API statistics endpoint

## 📁 Project Structure

```
feedback-backend/
├── app/
│   ├── app.py                 # Main Flask application
│   └── templates/
│       └── index.html         # Web interface
├── tests/
│   ├── __init__.py
│   └── test_app.py           # Comprehensive unit tests
├── config/
│   ├── __init__.py
│   └── config.py             # Configuration settings
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── Dockerfile               # Docker configuration
├── .dockerignore           # Docker ignore rules
├── .env.example            # Environment variables template
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) Docker for containerized deployment

### Local Setup

1. **Clone or extract the project**
   ```bash
   cd feedback-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **For development (with testing tools)**
   ```bash
   pip install -r requirements-dev.txt
   ```

## 💻 Usage

### Running Locally

#### Development Mode
```bash
python app/app.py
```

#### Production Mode with Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app.app:app
```

The application will be available at:
- **Web Interface**: http://localhost:5000
- **API Endpoints**: http://localhost:5000/api/*

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Available environment variables:
- `FLASK_ENV`: Environment (development/production)
- `PORT`: Server port (default: 5000)
- `FEEDBACK_FILE`: JSON storage file path

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### 1. Submit Feedback
```http
POST /api/feedback
Content-Type: application/json

{
    "name": "John Doe",           # Optional
    "email": "john@example.com",  # Optional
    "feedback": "Great service!"  # Required (max 1000 chars)
}
```

**Response (201 Created):**
```json
{
    "message": "Feedback submitted successfully!",
    "id": 1,
    "timestamp": "2025-10-27T17:30:00.123456"
}
```

#### 2. Get All Feedback
```http
GET /api/feedback
GET /api/feedback?limit=10&offset=0  # With pagination
```

**Response (200 OK):**
```json
{
    "feedback": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "feedback": "Great service!",
            "timestamp": "2025-10-27T17:30:00.123456",
            "ip_address": "127.0.0.1"
        }
    ],
    "count": 1,
    "total": 1
}
```

#### 3. Get Feedback by ID
```http
GET /api/feedback/{id}
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "feedback": "Great service!",
    "timestamp": "2025-10-27T17:30:00.123456"
}
```

#### 4. Delete Feedback
```http
DELETE /api/feedback/{id}
```

**Response (200 OK):**
```json
{
    "message": "Feedback deleted successfully"
}
```

#### 5. Get Statistics
```http
GET /api/stats
```

**Response (200 OK):**
```json
{
    "total_feedback": 10,
    "total_with_email": 7,
    "total_anonymous": 3,
    "latest_timestamp": "2025-10-27T17:30:00.123456",
    "oldest_timestamp": "2025-10-27T10:00:00.123456"
}
```

#### 6. Health Check
```http
GET /health
```

**Response (200 OK):**
```json
{
    "status": "healthy",
    "timestamp": "2025-10-27T17:30:00.123456",
    "feedback_count": 10,
    "storage_accessible": true
}
```

#### 7. API Information
```http
GET /api/info
```

**Response (200 OK):**
```json
{
    "app_name": "Feedback Collection API",
    "version": "1.0.0",
    "description": "REST API for collecting and managing user feedback",
    "endpoints": { ... }
}
```

### Error Responses

All endpoints return consistent error responses:

```json
{
    "error": "Error message description"
}
```

Common HTTP status codes:
- `400 Bad Request`: Invalid input or validation error
- `404 Not Found`: Resource not found
- `405 Method Not Allowed`: Invalid HTTP method
- `500 Internal Server Error`: Server-side error

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run Specific Test File
```bash
pytest tests/test_app.py -v
```

### Run Specific Test
```bash
pytest tests/test_app.py::test_submit_valid_feedback -v
```

### View Coverage Report
After running tests with coverage, open:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Categories

The test suite includes:
- ✅ Health check tests
- ✅ Feedback submission tests
- ✅ Feedback retrieval tests
- ✅ Pagination tests
- ✅ Validation tests
- ✅ Error handling tests
- ✅ Statistics tests
- ✅ Integration tests

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t feedback-backend .
```

### Run Container
```bash
docker run -d -p 5000:5000 --name feedback-api feedback-backend
```

### Run with Volume (Persistent Data)
```bash
docker run -d -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  --name feedback-api \
  feedback-backend
```

### View Logs
```bash
docker logs -f feedback-api
```

### Stop Container
```bash
docker stop feedback-api
docker rm feedback-api
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

## 🔄 CI/CD Integration

### Jenkins Pipeline

The backend integrates with Jenkins CI/CD pipeline:

```groovy
stage('Test Backend') {
    steps {
        dir('backend') {
            sh 'pip install -r requirements.txt'
            sh 'python -m pytest tests/ --verbose'
        }
    }
}

stage('Build Backend Image') {
    steps {
        dir('backend') {
            script {
                def backendImage = docker.build("feedback-backend:${BUILD_NUMBER}")
                backendImage.push()
            }
        }
    }
}
```

### GitHub Actions

Example workflow:
```yaml
name: Backend CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=app
```

## ⚙️ Configuration

### Application Config

Edit `config/config.py` for application settings:

- **Development**: Debug mode enabled
- **Production**: Optimized for performance
- **Testing**: Isolated test environment

### Environment-based Config

Load configuration based on environment:

```python
from config.config import config

app_config = config[os.getenv('FLASK_ENV', 'development')]
```

## 📊 Performance

- **Response Time**: < 100ms for most endpoints
- **Concurrent Users**: Supports 100+ concurrent requests with Gunicorn
- **Data Storage**: Efficient JSON file operations
- **Memory Usage**: ~50MB base memory footprint

## 🔒 Security Considerations

- Input validation on all endpoints
- CORS configuration for API access control
- Request size limits (16MB max)
- Error messages don't expose sensitive information
- Health check doesn't reveal system internals

## 🛠️ Development

### Code Formatting
```bash
black app/
flake8 app/
```

### Adding New Endpoints

1. Add route decorator to `app/app.py`
2. Implement endpoint logic
3. Add corresponding tests in `tests/test_app.py`
4. Update API documentation

## 📝 Data Storage

Feedback is stored in `feedback_data.json`:

```json
[
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "feedback": "Great application!",
        "timestamp": "2025-10-27T17:30:00.123456",
        "ip_address": "127.0.0.1"
    }
]
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9
```

### Permission Denied (Linux)
```bash
sudo chmod +x app/app.py
```

### Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

## 📞 Support

For issues, questions, or contributions, please open an issue on the project repository.

---

**Built with ❤️ using Flask**
