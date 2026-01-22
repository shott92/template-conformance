import xml.etree.ElementTree as ET
import logging

def read_reqif(file_path):
    """
    Parses a ReqIF file (XML) and extracts requirements text.
    This is a simplified parser looking for THE-VALUE inside ATTRIBUTE-VALUE-STRING.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # ReqIF uses namespaces, which complicates finding tags. 
        # We'll search for specific tags ignoring namespaces for simplicity or use wildcard.
        # Structure often: SPEC-OBJECT -> VALUES -> ATTRIBUTE-VALUE-STRING -> THE-VALUE
        
        requirements = []
        
        # Find all ATTRIBUTE-VALUE-STRING elements (where text content is usually stored)
        # Note: This might extract more than just requirements (like IDs, titles), 
        # but for a generic import it's a starting point.
        # A more robust solution would check the DEFINITION-REF.
        
        # Using xpath with namespaces is safer if we knew them, but they vary.
        # Let's simple iteration.
        
        for elem in root.iter():
            if 'THE-VALUE' in elem.tag:
                text = elem.text
                if text and len(text.strip()) > 10: # Heuristic: ignore short strings (IDs, status)
                    requirements.append(text.strip())
                    
        logging.info(f"Read {len(requirements)} potential requirements from {file_path}")
        return requirements
    except Exception as e:
        logging.error(f"Error reading reqif file: {e}")
        raise
