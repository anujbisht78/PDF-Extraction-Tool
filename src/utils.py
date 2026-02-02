import re
import cv2
import pytesseract
import numpy as np
from PIL import Image

# Robust figure caption detection

FIGURE_REGEX = re.compile(
    r'figure\s+(\d+\.\d+)',
    re.IGNORECASE
)

def detect_figure_captions(text: str):
    """
    Detect captions like:
      Figure 1.1
      Figure   2.3
    Returns:
      ['Figure_1.1', 'Figure_2.3']
    """
    if not text:
        return []
    matches = FIGURE_REGEX.findall(text)
    return [f"Figure_{m}" for m in matches]

# Text quality detection (NCERT fonts)

def is_text_garbled(text: str) -> bool:
    """
    Heuristic for NCERT broken Unicode text.
    If >30% characters are non-ASCII -> unreadable.
    """
    if not text or not text.strip():
        return True
    non_ascii = sum(1 for c in text if ord(c) > 127)
    return (non_ascii / len(text)) > 0.30

# OCR fallback

def ocr_image(pil_image: Image.Image) -> str:
    """
    OCR a page image using Tesseract.
    """
    img = np.array(pil_image)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return pytesseract.image_to_string(img)
