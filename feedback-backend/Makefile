# Makefile for Feedback Backend

.PHONY: help install run test clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run the application"
	@echo "  make test         - Run tests with coverage"
	@echo "  make clean        - Clean generated files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	@echo "Starting Flask application..."
	python app/app.py

test:
	@echo "Running tests..."
	pytest tests/ --verbose --cov=app --cov-report=html --cov-report=term-missing

clean:
	@echo "Cleaning generated files..."
	rm -rf __pycache__ .pytest_cache htmlcov .coverage
	rm -rf app/__pycache__ tests/__pycache__ config/__pycache__
	rm -f feedback_data.json test_feedback_data.json
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	@echo "Building Docker image..."
	docker build -t feedback-backend .

docker-run:
	@echo "Running Docker container..."
	docker run -d -p 5000:5000 --name feedback-api feedback-backend

format:
	@echo "Formatting code..."
	black app/ tests/
	flake8 app/ tests/

lint:
	@echo "Linting code..."
	flake8 app/ tests/
