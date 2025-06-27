import os
from PIL import Image, ImageFilter
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Ananya.Mehta\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
def extract_text_from_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(path)
        return "".join([page.extract_text() or "" for page in reader.pages])
    elif ext == ".docx":
        from docx import Document
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".txt":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext in [".jpg", ".jpeg", ".png", ".tiff"]:
        try:
            img = Image.open(path)
            img = img.convert('L')  # Convert to grayscale
            img = img.filter(ImageFilter.SHARPEN)  # Optional: sharpen image
            # Optional: apply thresholding for binarization
            img = img.point(lambda x: 0 if x < 140 else 255, '1')

            text = pytesseract.image_to_string(img)
            print("OCR Extracted Text:", text)
            return text
        except Exception as e:
            return f"OCR failed: {e}"
    else:
        raise ValueError(f"Unsupported file type: {ext}")
