FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Expose port (Render will set PORT env variable)
EXPOSE 5000

# Use environment variable for port
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} app:app
