import fitz  # PyMuPDF
import os
import json
from collections import Counter
import re

# --- NEW: Use the script's location to define absolute paths ---
# This makes the script runnable from anywhere.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, "input")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")


# --- END NEW ---

def clean_text(text):
    """Removes leading/trailing whitespace and non-printable characters."""
    return re.sub(r'[^A-Za-z0-9\s.,;\'"-:]+', '', text).strip()


def identify_heading_styles(doc):
    """
    Analyzes the document to find font sizes for Title, H1, H2, H3.
    This is a heuristic-based approach.
    """
    font_counts = Counter()
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        size = round(span["size"])
                        font_counts[size] += 1

    if not font_counts:
        return {}

    if len(font_counts) > 1:
        most_common_size = font_counts.most_common(1)[0][0]
        del font_counts[most_common_size]

    sorted_sizes = sorted(font_counts.keys(), reverse=True)

    styles = {}
    if len(sorted_sizes) > 0: styles["title"] = sorted_sizes[0]
    if len(sorted_sizes) > 1: styles["H1"] = sorted_sizes[1]
    if len(sorted_sizes) > 2: styles["H2"] = sorted_sizes[2]
    if len(sorted_sizes) > 3: styles["H3"] = sorted_sizes[3]

    return styles


def extract_document_structure(pdf_path):
    """
    Extracts the title and a hierarchical outline (H1, H2, H3) from a PDF.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"  [!] Error opening {os.path.basename(pdf_path)}: {e}")
        return None

    styles = identify_heading_styles(doc)
    if not styles:
        doc.close()
        return {"title": "Unknown Title (No styles found)", "outline": []}

    title = "Untitled Document"
    outline = []

    title_size = styles.get("title")
    if title_size:
        first_page = doc[0]
        for block in first_page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if round(span["size"]) == title_size:
                            title_text = clean_text(span["text"])
                            if title_text:
                                title = title_text
                                break
                    if title != "Untitled Document": break
                if title != "Untitled Document": break

    for page_num, page in enumerate(doc):
        blocks = sorted(page.get_text("dict")["blocks"], key=lambda b: b['bbox'][1])
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    if line["spans"]:
                        span = line["spans"][0]
                        span_size = round(span["size"])
                        text = clean_text("".join(s["text"] for s in line["spans"]))

                        if not text:
                            continue

                        level = None
                        if span_size == styles.get("H1"):
                            level = "H1"
                        elif span_size == styles.get("H2"):
                            level = "H2"
                        elif span_size == styles.get("H3"):
                            level = "H3"

                        if level:
                            outline.append({
                                "level": level,
                                "text": text,
                                "page": page_num + 1
                            })
    doc.close()
    return {"title": title, "outline": outline}


if __name__ == "__main__":
    print(f"Starting PDF processing...")
    print(f"Input directory: {INPUT_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print("Created output directory.")

    # Check if the input directory exists
    if not os.path.isdir(INPUT_DIR):
        print(f"[ERROR] Input directory not found at '{INPUT_DIR}'. Please check your folder structure.")
    else:
        pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
        if not pdf_files:
            print("[INFO] No PDF files found in the input directory.")
        else:
            for filename in pdf_files:
                pdf_path = os.path.join(INPUT_DIR, filename)
                print(f"-> Processing {filename}...")

                structure = extract_document_structure(pdf_path)

                if structure:
                    base_filename = os.path.splitext(filename)[0]
                    json_path = os.path.join(OUTPUT_DIR, f"{base_filename}.json")

                    with open(json_path, 'w') as f:
                        json.dump(structure, f, indent=4)

                    print(f"   Successfully created {json_path}")

    print("\nProcessing complete.")