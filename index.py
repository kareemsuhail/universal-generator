from  yaml_schema_parser import Parser
from prepare_project_structure import prepare_project_structure
schema = Parser().read()
prepare_project_structure(schema)


