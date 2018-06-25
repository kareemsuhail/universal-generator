from  yaml_schema_parser import Parser
from prepare_project_structure import prepare_project_structure
from models_generator import generate_models
from graphql_types_generator import generate_types
from graphql_queries_generator import generate_graphql_queries
from graphql_schema_generator import generate_schema_file
from graphql_mutations_generator import  generate_mutations
from auth_system_generator import generate_auth_system
# read schema file
schema = Parser().read()
# create project skeleton
prepare_project_structure(schema)
# generate models and register them
generate_models(schema)
# generate graphql types
generate_types(schema)
# generate graphql queries
generate_graphql_queries(schema)
# generate Mutations
generate_mutations(schema)
# generate graphql schema file
generate_schema_file(schema)
# generate auth system
generate_auth_system(schema)