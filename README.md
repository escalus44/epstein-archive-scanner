# Epstein Archive Scanner & Search Interface

This project scans large document archives and creates a searchable
web interface. It supports OCR text extraction, face detection, keyword
matching, and a live browser UI.

All input/output paths use **generic placeholders** so anyone can configure
their own directories (Linux, Mac, or Windows).

Epstein Files -> https://drive.google.com/drive/folders/1hTNH5woIRio578onLGElkTWofUSWRoH_  
---

## Features

### 🔎 Advanced Scanner (Python)
- OCR text extraction (Tesseract)
- OpenCV face detection
- Keyword matching
- Legal term matching
- Date extraction
- Name extraction
- Multi-threaded scanning (configurable)
- Writes all results to `results.db` (SQLite3)
- Saves extracted OCR text into `output/fulltext/`
- Saves cropped face images into `output/faces/`
- Skips files with no matches (optional)
- Handles 20k–50k+ files safely

### 🌐 Web Search UI (Flask)
- Fast search by keyword, snippet, file name, and metadata
- “Faces Only” filtering
- “Trump Only” filtering
- “Flight Logs Only” filtering
- Live feed (`/live`)
- Full-text viewer (`/view/<id>`)
- Built-in Finder Box:
  - Highlight all matches
  - Next/Prev jump
  - Counter: `3 / 21`

---

## Folder Structure

### Application
```
EpsteinApp/
    app.py
    templates/
        index.html
        live.html
        trump.html
        flightlogs.html
        faces.html
        fulltext.html
```

### Scanner
```
EpsteinScanner/
    scanner_advanced.py
```

### Output (user defined)
```
<OUTPUT_ROOT>/
    results.db
    fulltext/
    faces/
```

Where:
- `<INPUT_ROOT>` is where your extracted files are stored  
- `<OUTPUT_ROOT>` is where the scanner writes the results  
- You define both paths in the scanner script  

---

## Installation

### 1. Install dependencies
```
sudo apt install -y \
  python3-pip \
  tesseract-ocr \
  libtesseract-dev \
  poppler-utils \
  libjpeg-dev \
  libpng-dev \
  libxml2 \
  libxslt1.1 \
  libxslt1-dev \
  ffmpeg \
  sqlite3 \
  ntfs-3g


pip3 install \
  pdfplumber \
  pytesseract \
  pillow \
  python-docx \
  openpyxl \
  python-dateutil \
  tqdm \
  opencv-python \
  numpy \
  pandas \
  xlsxwriter \
  flask
```

### 2. Configure paths in the scanner
Inside the scanner script:
```
INPUT_ROOT  = "<INPUT_ROOT>"
OUTPUT_ROOT = "<OUTPUT_ROOT>"
```

### 3. Choose thread count
```
MAX_WORKERS = 3
```

### 4. Run the scanner
```
python3 scanner_advanced.py
```

---

## Running the Web App

From the EpsteinApp folder:
```
python3 app.py
```

Visit:
```
http://<your-ip>:5000
```

---

## Finder Box

Acts like a built-in document search:
- Highlights all matches
- Navigation arrows
- Hit counter
- Searches the entire rendered table
- Does not break page layout

---

## License
For research and educational use only.
