import argparse
import json
from pathlib import Path

from extractor import extract_text, extract_figures_by_rendering

def main():
    parser = argparse.ArgumentParser(
        description="NCERT / CBSE PDF Extraction Tool"
    )
    parser.add_argument(
        "pdf",
        help="Path to the full NCERT textbook PDF"
    )
    parser.add_argument(
        "--out",
        default="output",
        help="Output directory"
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    report = []

    # Page-wise text extraction (OCR fallback inside)
    text_map = extract_text(
        args.pdf,
        out_dir / "text_pages",
        report
    )

    # Figure extraction by rendering (NCERT-correct)
    figure_map = extract_figures_by_rendering(
        args.pdf,
        out_dir / "images",
        report,
        text_map
    )

    manifest = {
        "text_pages": text_map,
        "figures": figure_map
    }

    with open(out_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    (out_dir / "extraction_report.txt").write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("Extraction complete")

if __name__ == "__main__":
    main()
