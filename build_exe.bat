@echo off
echo ============================================================
echo Technohull Serial Number Extractor - Build Executable
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Building standalone executable...
echo This will take several minutes. Please wait...
echo.

REM Run the build script
python build_exe.py

echo.
echo ============================================================
if exist "dist\TechnohullSerialExtractor.exe" (
    echo SUCCESS! Your executable is ready in the 'dist' folder
    echo You can now distribute TechnohullSerialExtractor.exe
) else (
    echo Build may have failed. Check the output above for errors.
)
echo ============================================================
echo.
pause
