import os
import PyPDF2
import docx2txt
import pdfplumber
from PIL import Image
import pytesseract

def extract_text(file_path):
    try:
        ext = os.path.splitext(file_path)[-1].lower()
        text = ''
        
        if ext == '.pdf':
            # Try to extract text using pdfplumber (more accurate for text-based PDFs)
            with pdfplumber.open(file_path) as pdf:
                text = ''.join([page.extract_text() for page in pdf.pages])
            
            # If no text is found (likely a scanned PDF), use OCR to extract text
            if not text.strip():
                text = extract_text_from_pdf_with_ocr(file_path)
        
        elif ext == '.docx':
            text = docx2txt.process(file_path)
        
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        
        return text
    except Exception as e:
        return f"Error occurred in extracting text from {file_path}: {e}"

def extract_text_from_pdf_with_ocr(file_path):
    try:
        # Open the PDF as an image for OCR extraction
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                img = page.to_image()
                ocr_text = pytesseract.image_to_string(img.original)
                text += ocr_text
        return text
    except Exception as e:
        return f"Error occurred in OCR extraction: {e}"
