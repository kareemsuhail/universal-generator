from  yaml_schema_parser import Parser
from prepare_project_structure import prepare_project_structure
from models_generator import generate_models
from graphql_types_generator import generate_types
# read schema file
schema = Parser().read()
# create project skeleton
prepare_project_structure(schema)
# generate models and register them
generate_models(schema)
# generate graphql types
generate_types(schema)



