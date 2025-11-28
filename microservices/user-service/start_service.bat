@echo off
REM ==========================================================
REM  USER SERVICE STARTUP SCRIPT
REM  Food Delivery System
REM ==========================================================

echo ========================================
echo   STARTING USER SERVICE
echo ========================================
echo.

REM Navigate to user-service directory
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and add to PATH
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask flask-sqlalchemy flask-jwt-extended
)

echo [2/3] Starting User Service on port 5001...
echo.
echo Health Check: http://localhost:5001/health
echo API Endpoints: http://localhost:5001/api/users
echo.
echo Press Ctrl+C to stop the service
echo ========================================
echo.

REM Run the service
python app.py

REM If service crashes, show error
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERROR: Service failed to start!
    echo ========================================
    echo.
    echo Possible causes:
    echo - Port 5001 already in use
    echo - Database file locked
    echo - Missing dependencies
    echo - Syntax error in app.py
    echo.
    pause
)
