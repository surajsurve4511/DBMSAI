@echo off
:: MediCare Hospital Management System - Quick Launcher
:: This script helps you start the application easily

title MediCare HMS - Launcher
color 0A

echo.
echo ========================================================
echo       MediCare Hospital Management System
echo              AI-Powered Healthcare
echo ========================================================
echo.

:: Check if we're in the correct directory
if not exist "app.py" (
    echo ERROR: app.py not found!
    echo Please run this script from the DBMSAI directory.
    echo.
    pause
    exit /b 1
)

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher.
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking Python installation...
python --version
echo.

:: Check if virtual environment should be used
if exist "venv\Scripts\activate.bat" (
    echo [2/4] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [2/4] No virtual environment found, using system Python...
)
echo.

:: Check dependencies
echo [3/4] Checking dependencies...
python -c "import flask, mysql.connector, pandas, numpy, sklearn" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Some dependencies are missing!
    echo Installing required packages...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please run manually: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
) else (
    echo All dependencies installed!
)
echo.

:: Check database connection
echo [4/4] Checking database connection...
python -c "from database import Database; conn = Database.get_connection().__enter__(); print('Database connection: OK'); conn.close()" 2>nul
if errorlevel 1 (
    echo.
    echo WARNING: Could not connect to database!
    echo Please ensure:
    echo   1. MySQL server is running (XAMPP/WAMP)
    echo   2. 'hospital' database exists
    echo   3. Credentials in config.py are correct
    echo.
    echo Press any key to continue anyway...
    pause >nul
) else (
    echo Database connection: OK
)
echo.

echo ========================================================
echo              Starting MediCare HMS...
echo ========================================================
echo.
echo Server will start at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================================
echo.

:: Start the Flask application
python app.py

:: If the app exits, wait for user
echo.
echo.
echo Application has stopped.
pause
