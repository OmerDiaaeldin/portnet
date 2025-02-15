from PyPDF2 import PdfReader

# Load the PDF file

# Extract text from each page


def pdf_to_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    return text