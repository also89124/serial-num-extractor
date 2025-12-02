@echo off
REM Marine Device Serial Number Extractor - OCR Version
REM Launch script for Windows - NO TESSERACT NEEDED!

title Marine Device Serial Number Extractor
color 0B

echo.
echo ============================================================
echo        Marine Device Serial Number Extractor
echo              NO INSTALLATION REQUIRED!
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%~dp0"

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import easyocr" >nul 2>&1
if errorlevel 1 (
    echo.
    echo First time setup - Installing required packages...
    echo This will take 2-5 minutes. Please wait...
    echo.
    pip install -r requirements.txt
    echo.
    echo Installation complete!
    echo.
)

echo Starting application...
echo.
echo NOTE: First run will download OCR model (~100MB)
echo This only happens once and takes 1-2 minutes.
echo.

python device_ocr_extractor.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo Program encountered an error
    echo ============================================================
    pause
)
