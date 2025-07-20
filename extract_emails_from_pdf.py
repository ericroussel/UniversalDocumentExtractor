import os
import csv
import subprocess
from email import message_from_string
import requests

TIKA_SERVER_URL = 'http://localhost:9998/tika'
SOURCE_DIR = r'd:\test'
OCR_DIR = r'c:\ocr'
OUTPUT_CSV = os.path.join(OCR_DIR, 'emails.csv')


def ocr_pdf(src_path, dest_path):
    """Run OCRmyPDF on the given PDF."""
    subprocess.run([
        'ocrmypdf',
        '--skip-text',
        src_path,
        dest_path
    ], check=True)


def extract_text_with_tika(pdf_path):
    """Extract text from a PDF using Tika server."""
    with open(pdf_path, 'rb') as f:
        response = requests.put(
            TIKA_SERVER_URL,
            data=f,
            headers={'Accept': 'text/plain'}
        )
    response.raise_for_status()
    return response.text


def parse_email(text):
    """Parse email message from text."""
    try:
        msg = message_from_string(text)
    except Exception:
        return None
    return {
        'date': msg.get('Date', ''),
        'sender': msg.get('From', ''),
        'receiver': msg.get('To', ''),
        'cc': msg.get('Cc', ''),
        'subject': msg.get('Subject', ''),
        'body': msg.get_payload()
    }


def process_pdfs():
    os.makedirs(OCR_DIR, exist_ok=True)
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['pdf_file', 'date', 'sender', 'receiver', 'cc', 'subject', 'body']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(SOURCE_DIR):
            for name in files:
                if not name.lower().endswith('.pdf'):
                    continue
                src_pdf = os.path.join(root, name)
                ocr_pdf_path = os.path.join(OCR_DIR, name)
                print(f'OCR processing {src_pdf} -> {ocr_pdf_path}')
                ocr_pdf(src_pdf, ocr_pdf_path)

                text = extract_text_with_tika(ocr_pdf_path)
                email_data = parse_email(text)
                if email_data:
                    email_data['pdf_file'] = name
                    writer.writerow(email_data)
                else:
                    print(f'Could not parse email from {name}')


if __name__ == '__main__':
    process_pdfs()
