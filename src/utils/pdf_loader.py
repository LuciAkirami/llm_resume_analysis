from datetime import datetime
from pypdf import PdfReader


def parse_pdf(uploaded_file):
    """Extract contents from a PDF file"""
    reader = PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


def get_current_date():
    """Gets the Current Date"""
    return datetime.today().strftime("%Y-%b-%d")
