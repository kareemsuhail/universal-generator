from  yaml_schema_parser import Parser
from prepare_project_structure import prepare_project_structure
from models_generator import generate_models
# read schema file
schema = Parser().read()
# create project skeleton
prepare_project_structure(schema)
generate_models(schema)


