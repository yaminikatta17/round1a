# Heading Structure Extractor for PDF (Adobe Hackathon Round 1A)

## 📄 Problem Statement

The task is to parse a PDF and extract:
- The **Title**
- All **headings** with hierarchy: H1, H2, H3, etc.
- Along with the **page number**

The output should be a JSON file in the format:

```json
{
  "title": "Sample Document",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## 🧠 Approach

1. **Parsing**: We use [`PyMuPDF`](https://pymupdf.readthedocs.io/en/latest/) (`fitz`) to extract text and layout info.
2. **Heading Detection**:
   - Font size threshold
   - Bold style (flags)
   - All uppercase
   - Numbered headings (e.g., `1.2`, `2.1.3`)
   - Short text lines (≤ 12 words)
3. **Filtering**:
   - Ignores bullets, long paragraphs, and stopword-starting lines.
   - Filters out body text using heuristics.
4. **Heading Level Classification**:
   - Based on font size + bold + capital casing
   - Maps text to levels: `H1`, `H2`, `H3`, `H4`
5. **Merging Adjacent Headings**:
   - Merges multi-line headings using x/y proximity, short tail lines, and continuation heuristics (e.g., starts with "and", "or", "with").

---

## 🔧 How to Build & Run

### 🐳 Build Docker Image

```bash
docker build -t heading-extractor .
```

> This installs dependencies and copies the app.

### ▶️ Run the Solution

> Make sure your PDF is in the `input/` folder.

```bash
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output heading-extractor
```

✅ Output JSON will be saved in `output/` with the same name as the input PDF (e.g., `sample.json`).

---

## 🧾 File Structure

```
round1a/
├── Dockerfile
├── app/
│   ├── extract.py         # Main logic
│   └── __init__.py
├── input/                 # Input PDFs go here
├── output/                # Output JSONs will be saved here
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---

## 📚 Dependencies

```text
PyMuPDF==1.22.0
```

---

## ✅ Key Notes

- No internet access is required
- Runs within 200MB image size
- Font size alone is not used — multiple heuristics are applied
- Works across simple and complex PDFs

---

## 📌 Author

- **Yamini**: yaminikatta17@gmail.com
- Adobe Hackathon 2025 – Round 1A