import os
def generate_schema_file(schema):
    schema_file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/schema.py".format(
        schema['project_title'], schema['main_app'])), "w+")
    head = "import graphene\n"
    imports = "from .query import Query\nfrom .mutation import Mutation\n"
    body = "Schema = graphene.Schema(query=Query,mutation=Mutation)"
    schema_file.write(head+imports+body)
    schema_file.close()