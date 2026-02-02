# PDF-Extraction-Tool
# 📘 CBSE / NCERT Textbook Diagram & Text Extraction Tool

## 📌 Project Title
**CBSE / NCERT Class 10 Science PDF – Text & Diagram Extraction Tool**

---

## 📖 Project Overview

This project is a **Python-based PDF extraction system** built specifically for **CBSE / NCERT textbooks**, with a primary focus on the **NCERT Class 10 Science textbook**.

Unlike normal PDFs, NCERT textbooks contain:
- Custom embedded fonts
- Non-Unicode glyph mappings
- Vector-based diagrams (not raster images)
- Scanned or semi-scanned pages

Because of this, traditional PDF extraction tools fail to correctly extract **text and figures**.  
This project solves that problem using a **hybrid OCR + visual rendering + image-processing pipeline**.

---

## 🎯 Objectives

- Extract **page-wise readable text**
- Extract **only real diagrams (figures)** from the textbook
- ❌ Exclude activity boxes, paragraph screenshots, and grey instruction panels
- Handle **OCR fallback** for garbled or scanned pages
- Produce a structured, ML-friendly output

---

## ✅ Features

### 📝 Text Extraction
- Page-wise text extraction
- Automatic detection of garbled / non-Unicode text
- OCR fallback using **Tesseract**
- One `.txt` file per page

### 🖼️ Diagram (Figure) Extraction
- Extracts **only actual diagrams**:
  - Apparatus diagrams
  - Schematic figures
  - Labeled drawings
- ❌ Rejects:
  - Activity boxes
  - Paragraph screenshots
  - Grey instructional panels
- Works even when diagrams are **vector drawings** (not embedded images)

### 📊 Metadata & Logging
- `manifest.json` mapping pages → extracted text & diagrams
- `extraction_report.txt` for OCR and extraction warnings

---

## 🧠 Why NCERT PDFs Are Difficult

NCERT textbooks differ from normal PDFs because they use:

- Custom fonts with broken Unicode mappings
- Vector graphics instead of images
- Mixed scanned and digital content
- No bounding boxes for figures

👉 This tool **does not rely on PDF image objects**  
👉 It **renders page regions visually** and applies **vision-based heuristics**

---

## 📂 Output Directory Structure

```
output/
├── text_pages/
│   ├── page_001.txt
│   ├── page_002.txt
│   ├── page_003.txt
│   └── ...
│
├── images/
│   ├── Figure_1.1.png
│   ├── Figure_1.2.png
│   ├── Figure_1.3.png
│   ├── Figure_2.1.png
│   └── ...
│
├── manifest.json
└── extraction_report.txt
```

