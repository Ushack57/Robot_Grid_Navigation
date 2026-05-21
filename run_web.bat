@echo off
REM Robot Grid Navigation - Web Visualizer Launcher
REM This script starts the Flask web server

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Robot Grid Navigation - Web Visualizer Launcher         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Error: Python not found. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠ Flask not installed. Installing now...
    pip install Flask==2.3.0 Werkzeug==2.3.0 -q
    if %errorlevel% neq 0 (
        echo ✗ Failed to install Flask
        pause
        exit /b 1
    )
    echo ✓ Flask installed successfully
    echo.
)

echo ✓ Flask is installed
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   Starting Web Server...                                   ║
echo ║   Open your browser and go to: http://localhost:5000      ║
echo ║   Press Ctrl+C to stop the server                         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

python app.py
