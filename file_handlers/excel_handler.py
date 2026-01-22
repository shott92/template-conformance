import openpyxl
import logging

def read_excel(file_path):
    """
    Reads an excel file and looks for a column named 'Requirement' or 'Description',
    or falls back to the first column. Returns a list of cell values.
    """
    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active # Use the active sheet
        
        headers = [cell.value for cell in sheet[1]]
        target_col_index = 0 # Default to first column
        
        # Try to find a relevant column
        for i, header in enumerate(headers):
            if header and isinstance(header, str):
                if 'requirement' in header.lower() or 'description' in header.lower():
                    target_col_index = i
                    logging.info(f"Found requirement column: {header} at index {i}")
                    break
        
        requirements = []
        # Iterate from row 2 (skip header)
        for row in sheet.iter_rows(min_row=2, min_col=target_col_index+1, max_col=target_col_index+1):
             for cell in row:
                 if cell.value:
                     requirements.append(str(cell.value).strip())
                     
        logging.info(f"Read {len(requirements)} requirements from {file_path}")
        return requirements
    except Exception as e:
        logging.error(f"Error reading excel file: {e}")
        raise
