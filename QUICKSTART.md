# Quick Start Guide

## 🚀 How to Use This Program

### Step 1: Install Tesseract OCR

**EASIEST METHOD - Direct Download:**

**Option 1:** Double-click `install_tesseract_helper.bat` 
(This will open the download page and guide you!)

**Option 2:** Manual steps:
1. Go to: https://github.com/UB-Mannheim/tesseract/wiki
2. Download: tesseract-ocr-w64-setup-5.3.3.20231005.exe
3. Run the installer (use default settings)
4. Restart your computer

**Option 3:** Direct download link:
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe

**Need detailed help?** See `INSTALL_TESSERACT.txt`

### Step 2: Run the Program

Double-click: **`run_ocr_extractor.bat`**

### Step 3: Extract Serial Numbers

1. Click **"📁 Upload Image"**
2. Select your screenshot
3. Click **"🔍 Extract Devices"** - Wait a few seconds
4. Review the extracted devices in the table
5. Click **"💾 Export to TXT"**
6. Type your desired filename (e.g., "MyBoat_Devices")
7. Click Save

### That's it! 🎉

## 📸 How to Get Device Screenshots

### From Raymarine Axiom:
1. Go to: **Settings → Network**
2. You'll see a list of all devices
3. Take a photo with your phone OR
4. Use the LightHouse app to screenshot

### Tips for Best Results:
- ✅ Use high resolution images
- ✅ Make sure text is clear and sharp
- ✅ PNG format is best
- ✅ Take photo straight-on (not at angle)
- ❌ Avoid blurry images
- ❌ Avoid glare or reflections

## ⚠️ Troubleshooting

### "Tesseract Not Found"
- Install Tesseract using instructions above
- Restart your computer
- Run program again

### "No devices found"
- Check if image is clear
- Try taking a new screenshot
- Increase image resolution
- Make sure device list is visible

### Need Help?
Check **README_OCR.md** for detailed instructions.

## 📁 Files in This Folder

- **device_ocr_extractor.py** - Main program
- **run_ocr_extractor.bat** - Double-click this to start
- **requirements.txt** - Python dependencies
- **README_OCR.md** - Full documentation
- **QUICKSTART.md** - This file
