import logging

from ears_template_conformance import EARSParser
from rupp_template_conformance import RuppParser
from agile_user_story_conformance import AgileUserStoryParser

logging.basicConfig(level=logging.DEBUG)

def requirement_formatter(requirement, conformance):
    formatted_req = f"<{conformance}>{requirement}</{conformance}>"
    return formatted_req

def process_requirements(requirements, parser_class):
    requirement_list = []
    conformance_list = []
    doc = parser_class.first_parse(requirements)
    for sent in doc.sents:
        parser = parser_class(sent)
        parser.analyze()
        
        requirement_list.append(parser.sent.text)
        conformance_list.append(parser.template_conformance)
        logging.debug(f"Requirement conformance is : {parser.template_conformance}")
        logging.debug('< < < < ~~~~~~~~ * * * * * * * * ~~~~~~~~ > > > >')
    
    tagged_requirements_list = [requirement_formatter(req, conf) for req, conf in zip(requirement_list, conformance_list)]
    return tagged_requirements_list

def check_rupp_template_compliance(requirements):
    return process_requirements(requirements, RuppParser)


def check_ears_template_compliance(requirements):
    return process_requirements(requirements, EARSParser)


def check_agile_story_template_conformance(requirements):
    return process_requirements(requirements, AgileUserStoryParser)
