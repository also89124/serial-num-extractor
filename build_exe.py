"""
Build script to create a standalone executable
Run this to create a single .exe file
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("Checking for PyInstaller...")
    try:
        import PyInstaller
        print("✓ PyInstaller already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")

def build_exe():
    """Build the executable"""
    print("\nBuilding executable...")
    print("This may take several minutes...\n")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single file
        "--windowed",  # No console window
        "--name=TechnohullSerialExtractor",  # Name of the exe
        "--icon=assets/app_icon.ico",  # App icon
        "--add-data=assets;assets",  # Include assets folder
        "device_ocr_extractor.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("✓ BUILD SUCCESSFUL!")
        print("="*60)
        print("\nYour executable is ready:")
        print("  Location: dist\\TechnohullSerialExtractor.exe")
        print("\nYou can now:")
        print("  1. Run the .exe directly from the dist folder")
        print("  2. Copy it to any Windows computer")
        print("  3. No Python installation needed!")
        print("\nNote: First run may take 10-30 seconds to start")
        print("      (OCR model loading)")
        print("="*60)
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Build failed: {e}")
        print("\nTry running: pip install pyinstaller")
        sys.exit(1)

if __name__ == '__main__':
    print("="*60)
    print("Technohull Serial Number Extractor - EXE Builder")
    print("="*60)
    
    install_pyinstaller()
    build_exe()
