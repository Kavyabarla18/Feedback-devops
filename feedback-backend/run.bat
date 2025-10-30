@echo off
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
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\.installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\.installed
)

REM Run the application
echo.
echo Starting Flask application...
echo Access at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app\app.py
