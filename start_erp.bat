@echo off
title ERP Application Startup

echo ================================
echo    ERP APPLICATION STARTUP
echo ================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install flask oracledb python-dotenv

echo.
echo Starting ERP Application...
echo.
echo The application will start on: http://localhost:5000
echo.
echo Instructions:
echo 1. Wait for the application to start
echo 2. Open your web browser
echo 3. Go to http://localhost:5000
echo 4. Login with any username/password
echo.

python app.py

echo.
echo Application stopped.
pause
