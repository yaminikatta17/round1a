import fitz  # PyMuPDF
import json
import os
import re

def is_valid_heading(text):
    stopwords = {"it", "function", "problem", "uses", "a", "the", "in", "on", "at", "and", "to"}
    first_word = text.split()[0].lower() if text.split() else ""
    if first_word in stopwords:
        return False
    if text.startswith(("•", "-", "*", "·")):
        return False
    if text.endswith((".", ",", ":", ";", "…")):
        return False
    if len(text.split()) > 12:
        return False
    return True

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = ""
                font_sizes = []
                is_bold = False

                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    line_text += text + " "
                    font_sizes.append(span["size"])
                    if span["flags"] & 2:  # Bold bitmask
                        is_bold = True

                line_text = line_text.strip()
                if not line_text or len(font_sizes) == 0 or not is_valid_heading(line_text):
                    continue

                avg_font_size = sum(font_sizes) / len(font_sizes)
                is_all_caps = line_text.isupper()
                starts_with_number = bool(re.match(r"^\d+(\.\d+)*(\s|:)", line_text))
                short_line = len(line_text.split()) <= 12

                level = None
                if (avg_font_size > 16) or (is_bold and avg_font_size > 14) or (is_all_caps and avg_font_size > 13):
                    level = "H1"
                elif avg_font_size > 14 or (is_bold and avg_font_size > 12) or starts_with_number:
                    level = "H2"
                elif avg_font_size > 12 or (is_bold and short_line):
                    level = "H3"
                elif avg_font_size > 10 and short_line:
                    level = "H4"

                if level:
                    headings.append({
                        "level": level,
                        "text": line_text,
                        "page": page_num,
                        "x": block.get("bbox", [0])[0],
                        "y": block.get("bbox", [0, 0, 0, 0])[1],
                    })

    return {
        "title": os.path.basename(pdf_path),
        "outline": merge_adjacent_headings(headings)
    }

def merge_adjacent_headings(headings):
    merged = []
    if not headings:
        return merged

    current = headings[0]
    for i in range(1, len(headings)):
        next_item = headings[i]

        same_page = current["page"] == next_item["page"]
        same_level = current["level"] == next_item["level"]
        close_y = abs(current["y"] - next_item["y"]) < 35
        close_x = abs(current["x"] - next_item["x"]) < 35
        short_next = len(next_item["text"].split()) <= 3

        current_ends_with_join = current["text"].lower().endswith(("and", "or", "with"))

        # Final rule: only merge if continuation makes sense
        should_merge = (
            same_page and same_level and short_next and close_y and close_x and (
                next_item["text"].islower() or
                current_ends_with_join
            )
        )

        if should_merge:
            current["text"] += " " + next_item["text"]
        else:
            merged.append({
                "level": current["level"],
                "text": current["text"],
                "page": current["page"]
            })
            current = next_item

    merged.append({
        "level": current["level"],
        "text": current["text"],
        "page": current["page"]
    })
    return merged




if __name__ == "__main__":
    input_path = "input/sample.pdf"
    output_path = "output/sample.json"

    if not os.path.exists(input_path):
        print("ERROR: PDF not found at input/sample.pdf")
        exit(1)

    result = extract_headings(input_path)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Processed {input_path} → {output_path}")
