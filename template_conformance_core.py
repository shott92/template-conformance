import logging

from ears_template_conformance import EARSParser
from rupp_template_conformance import RuppParser
from agile_user_story_conformance import AgileUserStoryParser
from quality_checker import QualityAnalyzer

logging.basicConfig(level=logging.DEBUG)

def requirement_formatter(requirement, conformance):
    formatted_req = f"<{conformance}>{requirement}</{conformance}>"
    return formatted_req

def process_requirements(requirements, parser_class):
    results = []
    
    # Handle list input (from file handlers) or string input (from API/String)
    if isinstance(requirements, list):
        iterator = requirements
    else:
        iterator = [requirements]
        
    for text_segment in iterator:
        if not text_segment:
            continue
        # Parse each segment (requirement string)
        doc = parser_class.first_parse(str(text_segment))
        
        for sent in doc.sents:
            parser = parser_class(sent)
            parser.analyze()
            
            # Extract type if available
            req_type = getattr(parser, 'requirement_type', 'N/A')
            if req_type is None:
                req_type = 'N/A'
            
            # Extract System Response for Atomicity Check (if available)
            system_response_text = None
            if hasattr(parser, 'system_response') and parser.system_response:
                system_response_text = parser.system_response.text

            # Run Quality Analysis
            quality_checker = QualityAnalyzer(parser.sent.text, system_response_text)
            quality_issues = quality_checker.analyze()
            quality_score = "Pass" if not quality_issues else "Fail"
                
            tagged_req = requirement_formatter(parser.sent.text, parser.template_conformance)
            
            result_obj = {
                'requirement': parser.sent.text,
                'conformance': parser.template_conformance,
                'type': req_type,
                'quality_score': quality_score,
                'quality_issues': "; ".join(quality_issues),
                'tagged_requirement': tagged_req
            }
            results.append(result_obj)
            
            logging.debug(f"Requirement conformance is : {parser.template_conformance}")
            logging.debug('< < < < ~~~~~~~~ * * * * * * * * ~~~~~~~~ > > > >')
    
    return results

def check_rupp_template_compliance(requirements):
    return process_requirements(requirements, RuppParser)


def check_ears_template_compliance(requirements):
    return process_requirements(requirements, EARSParser)


def check_agile_story_template_conformance(requirements):
    return process_requirements(requirements, AgileUserStoryParser)
