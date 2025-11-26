# Structured OCR Pipeline
Template-based OCR for digitizing semi-structured PDFs (voter rolls, Form-20).

![Python](https://img.shields.io/badge/Python-3.9%2B-teal)
![OCR](https://img.shields.io/badge/Tesseract-OCR-teal)
![PDF](https://img.shields.io/badge/PDF-Processing-teal)
![License](https://img.shields.io/badge/License-MIT-teal)

This repository implements a **high-accuracy OCR pipeline** optimized for documents with repeatable layouts.  
Instead of applying full-page OCR (slow + inaccurate), we **crop each page into logical sections** and apply OCR separately.

This improves accuracy and significantly reduces processing time.

---

## Features

- Converts PDF pages into images  
- Crops predictable sections using a coordinate template  
- Performs OCR on each section independently  
- Computes a confidence score per section  
- Outputs:
  - Cropped section images
  - Extracted text
  - Manifest JSON for reproducibility

---

## Repository Structure

```
structured-ocr-pipeline/
│
├── run_ocr.py
├── README.md
├── requirements.txt
├── LICENSE
└── ocr_output/
```

---

## Installation

Install Python dependencies:

```
pip install -r requirements.txt
```

Install Tesseract:

### Ubuntu
```
sudo apt install tesseract-ocr
```

### Mac (Homebrew)
```
brew install tesseract
```

### Windows
Download from:
https://github.com/UB-Mannheim/tesseract/wiki

Then update in `run_ocr.py`:

```
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## Usage

Run OCR on a PDF:

```
python run_ocr.py input.pdf
```

Output will be created in:

```
ocr_output/<pdf_name>/
```

---

## License

MIT License.  
See `LICENSE`.
