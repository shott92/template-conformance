import logging

def read_text(file_path):
    """
    Reads a text file and returns a list of non-empty lines.
    """
    try:
        requirements = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                text = line.strip()
                if text:
                    requirements.append(text)
        logging.info(f"Read {len(requirements)} lines from {file_path}")
        return requirements
    except Exception as e:
        logging.error(f"Error reading text file: {e}")
        raise
