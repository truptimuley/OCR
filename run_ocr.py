import sys
import json
import time
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Update this path on Windows if needed:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Coordinates for cropping sections (x, y, width, height)
TEMPLATE_COORDS = {
    "header": (50, 20, 1200, 200),
    "voter_info": (50, 220, 1200, 700),
    "address": (50, 930, 1200, 250),
    "id_block": (50, 1180, 1200, 180),
}

OCR_CONFIG = "--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.,/"

def crop_sections(img):
    w, h = img.size
    crops = {}
    for name, (x, y, wbox, hbox) in TEMPLATE_COORDS.items():
        crops[name] = img.crop((x, y, x + wbox, y + hbox))
    return crops

def run_ocr(pdf_path):
    pdf_path = Path(pdf_path)
    out_dir = Path("ocr_output") / pdf_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    pages = convert_from_path(pdf_path, dpi=200)
    manifest = {"source": str(pdf_path), "timestamp": time.time(), "pages": []}

    for i, page in enumerate(pages, start=1):
        page_dir = out_dir / f"page_{i:03d}"
        page_dir.mkdir(parents=True, exist_ok=True)

        sections = crop_sections(page)
        page_record = {"page": i, "sections": {}}

        for name, crop_img in sections.items():
            out_img = page_dir / f"{name}.png"
            crop_img.save(out_img)

            data = pytesseract.image_to_data(crop_img, output_type=pytesseract.Output.DICT, config=OCR_CONFIG)
            text = " ".join([t for t in data["text"] if t.strip()])

            confs = [int(c) for c in data["conf"] if c.isdigit() and int(c) >= 0]
            mean_conf = sum(confs) / len(confs) if confs else 0

            page_record["sections"][name] = {
                "text": text,
                "confidence": mean_conf,
                "image": str(out_img)
            }

        manifest["pages"].append(page_record)

    with open(out_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"OCR complete: {out_dir}")

if __name__ == "__main__":
    run_ocr(sys.argv[1])

