# Technohull Marine Device Serial Number Extractor

**Professional Marine Electronics Documentation Solution**

The Technohull Marine Device Serial Number Extractor is an enterprise-grade software application designed to streamline the documentation and inventory management of marine electronic equipment. This solution enables maritime professionals to efficiently extract, catalog, and manage device information from digital sources.

---

## Overview

This application provides automated optical character recognition (OCR) capabilities for extracting device information from screenshots and display images. The system is designed for use with Raymarine Axiom, CZone, and other marine electronics management systems.

### Key Capabilities

**Primary Function: OCR Image Processing**
- Automated text recognition from device list screenshots
- GUI-based interface for streamlined workflow
- Batch processing support for multiple devices
- Custom export formatting options
- Real-time preview and verification

**Core Components**
- `device_ocr_extractor.py` - Main application executable
- `run_ocr_extractor.bat` - Quick launch utility
- Supports PNG, JPG, BMP, TIFF image formats
- Dark mode professional interface

---

## Getting Started

### System Requirements

**Operating Environment**
- Windows 10/11 (64-bit)
- Python 3.8 or higher
- 4 GB RAM minimum (8 GB recommended)
- 2 GB available disk space
- Display resolution: 1920x1080 or higher

**Software Dependencies**
- EasyOCR (automatically installed)
- PyTorch framework
- PIL/Pillow image processing library
- Tkinter GUI framework (included with Python)

### Installation Procedure

**Step 1: Launch Application**
Execute `run_ocr_extractor.bat` to start the application.

**Step 2: First-Time Setup**
Initial launch will automatically install required dependencies. This process takes approximately 2-5 minutes and occurs only once.

**Step 3: Operational Use**
1. Select "Upload Image" to load source material
2. Choose device screenshot or photograph
3. Click "Extract Devices" to initiate OCR processing
4. Review extracted data in tabular format
5. Assign device types using dropdown selectors
6. Select devices for export via checkboxes
7. Click "Export to TXT" to generate output file
8. Specify filename (format: SN_[SAP].txt)

---

## Installation and Configuration

### Prerequisites

**Python Environment**
Verify Python installation:
```powershell
python --version
```
Required version: Python 3.8 or higher

### Dependency Installation

Execute the following command in the project directory:
```powershell
pip install -r requirements.txt
```

This will install:
- EasyOCR (OCR engine)
- PyTorch (machine learning framework)
- Pillow (image processing)
- Additional required libraries

### No External Software Required
This application uses EasyOCR, which does not require Tesseract or any external OCR software installation.

---

## Data Extraction Capabilities

### Extracted Information

The system automatically identifies and extracts the following data fields:

**Device Information**
- Product name and model designation
- Product codes (e.g., E70656, V70524, MS-RA770)
- Serial numbers (multiple format support)
- Device type classification

**Supported Serial Number Formats**
- Alphanumeric codes (TAR3WR7, TADG0G9)
- Numeric sequences (0330729, 0730166)
- Hyphenated formats (J497793-0051)
- Extended formats (E704760350080)
- GMDSS formats (12L3487)

**Supported Device Types**
- AXIOM 2 PRO 9
- AXIOM 2 PRO 12
- AXIOM 2 PRO 16
- GMDSS
- RAYMARINE AIS 700
- RADAR QUANTUM 2
- THERMAL CAMERA
- RAYMARINE RAY53 VHF
- RAYMARINE RS 150

**Example Output**
```
GT9 - Vessel Name
9100967
___________________________________________

AXIOM 2 PRO 16:
E70658	TAR3WR7
E70658	TADG0G9

RAYMARINE RAY53 VHF:
E70524	0330729

RADAR QUANTUM 2:
E70498	0940100
```

---

## Image Acquisition Guidelines

### Source Material Requirements

**Recommended Specifications**
- Image resolution: 1920x1080 pixels minimum
- File format: PNG (preferred) or JPG
- Color depth: 24-bit or higher
- Compression: Minimal to none

**Image Quality Standards**
- Clear, sharp focus on text elements
- Uniform lighting without glare or reflection
- Perpendicular viewing angle to display
- High contrast between text and background
- Minimal motion blur or distortion

### Raymarine Axiom Procedure
1. Navigate to: Settings → Network → Device List
2. Capture image using mobile device or camera
3. Transfer file to workstation via USB, email, or cloud storage
4. Import to application using Upload Image function

---

## Feature Set

### Core Functionality

**Image Processing**
- Advanced OCR text recognition
- Multiple image format support (PNG, JPG, BMP, TIFF)
- Real-time image preview
- Automatic text detection and extraction

**User Interface**
- Professional dark mode theme
- Intuitive tabular data presentation
- Device type selection via dropdown menus
- Checkbox-based export selection
- Real-time status feedback

**Data Management**
- Vessel information tracking (Model, Name, SAP)
- Device type classification system
- Manual device entry capability
- Edit functionality for extracted data
- Grouped export by device type

**Export Capabilities**
- Custom filename generation (SN_[SAP].txt format)
- Formatted text output
- Device grouping by type
- Tab-delimited data structure

---

## Compatible Systems

### Supported Marine Electronics

**Raymarine Systems**
- Axiom 2 Pro Series (9", 12", 16")
- Axiom+ Series
- Axiom XL Series

**Network Management Systems**
- CZone Digital Switching
- Empirbus NMEA 2000 Networks
- Garmin Marine Network
- Simrad/B&G/Lowrance Networks

**General Compatibility**
- Any marine display system with text-based device lists
- Network configuration screens
- Device management interfaces

---

## Professional Applications

### Use Cases

**Marine Survey Operations**
- Complete equipment inventory documentation
- Serial number verification and recording
- Asset tracking for insurance and valuation purposes

**Service and Maintenance**
- Equipment warranty tracking
- Maintenance record keeping
- Service history documentation
- Parts ordering and replacement verification

**Commercial Operations**
- Fleet management and asset tracking
- Vessel sale documentation
- Insurance claim preparation
- Regulatory compliance documentation

**Corporate Applications**
- Multi-vessel fleet inventory
- Standardized documentation procedures
- Quality assurance and verification
- Asset lifecycle management

---

## System Architecture

### Performance Characteristics

**Initial Deployment**
- First execution: 2-5 minutes (dependency installation)
- OCR model download: 100-200 MB (one-time process)
- Subsequent launches: Immediate

**Operational Performance**
- OCR processing time: 10-30 seconds per image
- Batch processing: Supported for multiple devices
- Offline operation: Fully functional after initial setup
- Data privacy: All processing performed locally

---

## Security and Privacy

### Data Protection

**Local Processing**
All data processing occurs entirely on the local workstation. No information is transmitted to external servers or cloud services.

**Network Independence**
After initial setup, the application operates completely offline. Internet connectivity is not required for normal operations.

**Data Confidentiality**
- Source images remain on local storage
- No telemetry or usage data collection
- No external data transmission
- Complete data privacy assurance

**Compliance**
Suitable for use in environments requiring:
- Data sovereignty
- Air-gapped operations
- Confidential information handling
- GDPR compliance

---

## Troubleshooting

### Common Issues and Resolutions

**Issue: No Devices Detected**
- Verify image quality and resolution
- Ensure adequate contrast and lighting
- Confirm text is clearly visible and in focus
- Try higher resolution source image
- Check that device list is fully visible in frame

**Issue: Application Won't Launch**
- Verify Python installation (python --version)
- Check all dependencies installed (pip list)
- Run as Administrator if permission issues occur
- Review console output for error messages

**Issue: Slow Initial Performance**
- First execution loads OCR models (10-30 seconds normal)
- Subsequent executions will be significantly faster
- Ensure adequate system resources available

**Issue: Export File Not Generated**
- Verify write permissions in target directory
- Ensure vessel information fields are completed
- Confirm at least one device is selected for export
- Check available disk space

### Technical Support

For additional assistance, consult:
- QUICKSTART.md for rapid solutions
- BUILD_INSTRUCTIONS.txt for deployment issues
- System console output for error diagnostics

---

## Project Structure

```
serial numbers extractor/
├── Core Application
│   ├── device_ocr_extractor.py    # Main application
│   ├── run_ocr_extractor.bat      # Launch utility
│   └── requirements.txt           # Dependencies
│
├── Build System
│   ├── build_exe.bat              # Executable builder
│   ├── build_exe.py               # Build script
│   └── BUILD_INSTRUCTIONS.txt     # Build documentation
│
├── Assets
│   ├── assets/                    # Application icons
│   ├── create_icon.py             # Icon generator
│   └── barcode-illustration*.avif # Icon source
│
└── Documentation
    ├── README.md                  # Primary documentation
    └── QUICKSTART.md              # Quick reference
```

---

## Technical Documentation

### Documentation Suite

| Document | Description |
|----------|-------------|
| README.md | Primary documentation and system overview |
| QUICKSTART.md | Rapid deployment guide |
| BUILD_INSTRUCTIONS.txt | Executable compilation procedures |
| requirements.txt | Python dependency specifications |

---

## Deployment Options

### Standalone Executable
For distribution to systems without Python:

1. Execute `build_exe.bat`
2. Executable generated in `dist/` directory
3. File: TechnohullSerialExtractor.exe (~500MB)
4. No installation required on target systems
5. Self-contained with all dependencies

### Python Deployment
For development or customization:

1. Install Python 3.8+
2. Install dependencies: `pip install -r requirements.txt`
3. Execute: `run_ocr_extractor.bat` or `python device_ocr_extractor.py`

---

## Best Practices

### Image Acquisition
- Use PNG format for optimal quality
- Maintain resolution of 1920x1080 or higher
- Ensure perpendicular viewing angle
- Avoid glare and reflections
- Verify text clarity before processing

### Data Management
- Complete vessel information fields before export
- Verify device type assignments
- Review extracted data before export
- Maintain consistent naming conventions
- Archive source images with exported data

### Operational Guidelines
- Allow adequate time for first-run setup
- Verify extracted data accuracy
- Maintain backup copies of export files
- Document image source and date
- Follow organizational data management protocols

---

## Version Information

### Current Release: Version 1.0
**Release Date:** December 2, 2025

**Features:**
- OCR-based device information extraction
- Professional dark mode GUI interface
- Vessel information management
- Device type classification system
- Custom export formatting
- Manual device entry and editing
- Batch device processing
- Comprehensive documentation suite

---

## License and Usage

**License:** Proprietary - Technohull Marine
**Permitted Use:** Commercial and internal business operations
**Restrictions:** Distribution subject to licensing terms

---

## Technical Support and Contact

For technical assistance, deployment guidance, or licensing inquiries, consult your system administrator or IT department.

**Documentation Resources:**
- README.md (this document)
- QUICKSTART.md (rapid deployment guide)
- BUILD_INSTRUCTIONS.txt (executable compilation)

---

**Technohull Marine Device Serial Number Extractor**  
*Professional Marine Electronics Documentation Solution*  
*Version 1.0 - December 2025*
