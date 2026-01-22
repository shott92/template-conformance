from docx import Document
import logging

def read_docx(file_path):
    """
    Reads a docx file and returns a list of text from paragraphs.
    """
    try:
        doc = Document(file_path)
        requirements = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                requirements.append(text)
        logging.info(f"Read {len(requirements)} paragraphs from {file_path}")
        return requirements
    except Exception as e:
        logging.error(f"Error reading docx file: {e}")
        raise
