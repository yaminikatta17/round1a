FROM python:3.10-slim

WORKDIR /app

COPY heading_extractor.py .

RUN pip install pymupdf

CMD ["python", "heading_extractor.py"]
