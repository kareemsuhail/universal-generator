import os
def generate_graphql_queries(schema):
    head = "import graphene\n"
    for type_name,type_dic in schema['types'].items():
        file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/queries/{}.py".format(
            schema['project_title'],schema['main_app'],type_name)), "w+")
        file.write("import graphene\n")
        file.write("from ...models import {}\n".format(type_name))
        file.write("from ..types import {}Type\n".format(type_name))
        file.write("class {}Query(graphene.AbstractType):\n".format(type_name))
        file.write("\tall_{} = graphene.List({}Type)\n".format(type_name,type_name))
        file.write("\tdef resolve_all_{}(self, *args, **kwargs):\n".format(type_name))
        file.write("\t\treturn {}.objects.all()".format(type_name))
        file.close()
    query_file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/query.py".format(
            schema['project_title'],schema['main_app'])), "w+")
    query_file.write(head)
    temp_import = ""
    for type_name, type_dic in schema['types'].items():
        query_file.write("from .queries.{} import {}Query\n".format(type_name,type_name))
        temp_import = temp_import + type_name + 'Query ,'
    query_file.write("class Query({}graphene.ObjectType):\n".format(temp_import))
    query_file.write("\tpass")
    query_file.close()