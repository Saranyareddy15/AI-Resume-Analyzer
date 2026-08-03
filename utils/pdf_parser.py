"""
Extracts plain text from an uploaded resume PDF.
"""

import pdfplumber


def extract_text_from_pdf(file_stream):
    """
    file_stream: a file-like object (e.g. Flask's request.files['resume'])
    Returns the extracted text as a single string.
    """
    text_parts = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)
