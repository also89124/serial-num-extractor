# Quick Start Guide

## How to Use This Program

### Step 1: Run the Program

Double-click: **`run_ocr_extractor.bat`**

On first launch, required OCR models and dependencies will be installed automatically. This is a one-time process and may take 2–5 minutes.

### Step 2: Extract Serial Numbers

1. Click **"Upload Images"**
2. Select one or more screenshots/photos
3. Click **"Extract Devices & Engines"**
4. Review extracted results in the table
5. Double-click the "Device Type" column to assign types if needed (e.g., AXIOM, AIS 700, ENGINE)
6. Check the items you want to export
7. Click **"Export to TXT"**
8. Enter a filename (format recommended: `SN_[SAP].txt`) and Save

### That's it

## How to Capture Screenshots

### From Raymarine Axiom:
1. Go to: **Settings → Network → Device List**
2. Capture a clear image of the device list
3. Transfer the image to your computer
4. Upload via the application

### For Engine Serial Numbers:
1. Navigate to your engine diagnostics/status screen
2. Capture the screen showing **Engine Serial Number** or **S/N**
3. Ensure the serial is legible and well-lit

### Tips for Best Results:
- Use high-resolution images (1920x1080+)
- Prefer PNG format for clarity
- Keep the camera perpendicular to the screen
- Avoid glare, reflections, and motion blur
- Ensure text is sharp and readable

## Troubleshooting

### First-run delay
- The first run downloads OCR models; subsequent runs are faster.

### "No items found"
- Check image clarity and resolution
- Ensure text is visible and not cropped
- Try another screenshot or a straighter angle
- Increase lighting and contrast

### Application issues
- Verify Python is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Review terminal output for error messages

### Need Help?
See **README.md** for full documentation.

## Files in This Folder

- **device_ocr_extractor.py** — Main application
- **run_ocr_extractor.bat** — Launch script
- **requirements.txt** — Python dependencies
- **README.md** — Full documentation
- **QUICKSTART.md** — This quick reference
