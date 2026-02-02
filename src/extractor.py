from pathlib import Path
import pdfplumber
import fitz
import cv2
import numpy as np
from utils import detect_figure_captions, is_text_garbled, ocr_image

# TEXT EXTRACTION

def extract_text(pdf_path, text_dir, report):
    text_dir.mkdir(parents=True, exist_ok=True)
    page_text_map = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if not text or is_text_garbled(text):
                report.append(
                    f"WARNING: Page {page_num} unreadable → OCR fallback"
                )
                img = page.to_image(resolution=300).original
                text = ocr_image(img)

            out_file = text_dir / f"page_{page_num:03d}.txt"
            out_file.write_text(text or "", encoding="utf-8")
            page_text_map[page_num] = str(out_file)

    return page_text_map

# DIAGRAM VALIDATION HEURISTICS

def is_text_heavy(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    small = [c for c in contours if cv2.contourArea(c) < 300]
    return len(small) > 100

def has_bad_aspect_ratio(img):
    h, w = img.shape[:2]
    return h / w > 1.6


def crop_diagram_only(img_path):
    img = cv2.imread(str(img_path))
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(
        bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return False

    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    cropped = img[y:y+h, x:x+w]

    if is_text_heavy(cropped) or has_bad_aspect_ratio(cropped):
        return False

    cv2.imwrite(str(img_path), cropped)
    return True

# FIGURE EXTRACTION (OCR-DRIVEN + FILTERED)

def extract_figures_by_rendering(pdf_path, image_dir, report, text_map):
    doc = fitz.open(pdf_path)
    image_dir.mkdir(parents=True, exist_ok=True)

    figure_map = {}

    for page_num, page in enumerate(doc, start=1):
        figure_map[page_num] = []

        text_file = text_map.get(page_num)
        if not text_file:
            continue

        text = Path(text_file).read_text(
            encoding="utf-8", errors="ignore"
        )

        figures = detect_figure_captions(text)
        if not figures:
            continue

        h, w = page.rect.height, page.rect.width

        clip_rect = fitz.Rect(
            0, h * 0.25,
            w, h * 0.90
        )

        pix = page.get_pixmap(
            matrix=fitz.Matrix(3, 3),
            clip=clip_rect
        )

        for fig in figures:
            out_path = image_dir / f"{fig}.png"
            counter = 1
            while out_path.exists():
                out_path = image_dir / f"{fig}_{counter}.png"
                counter += 1

            pix.save(out_path)

            # 🔥 KEEP ONLY REAL DIAGRAMS
            if crop_diagram_only(out_path):
                figure_map[page_num].append(str(out_path))
            else:
                out_path.unlink()

    return figure_map
