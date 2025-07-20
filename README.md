# UniversalDocumentExtractor

This repository contains a simple script for extracting email information from a
collection of PDF files. The script relies on OCRmyPDF for optical character
recognition and the Apache Tika server for text extraction.

## Requirements

- Python 3.8+
- [ocrmypdf](https://ocrmypdf.readthedocs.io/)
- [Apache Tika server](https://tika.apache.org/)
- `requests` Python package

## Usage

1. Start the Tika server. Example command:
   ```powershell
   java -jar C:\TIKA\tika-server-standard-3.2.0.jar
   ```
2. Place source PDF files in `d:\test`.
3. Run the script:
   ```powershell
   python extract_emails_from_pdf.py
   ```
4. OCR'd PDFs and the resulting `emails.csv` will be created in `c:\ocr`.

Each row in `emails.csv` contains the file name, date, sender, receiver,
cc, subject, and body of the email extracted from the PDF.
