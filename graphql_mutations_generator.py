import os
def generate_mutations(schema):
    mutation_file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/mutation.py".format(
        schema['project_title'], schema['main_app'])), "w+")
    head = "import graphene\n"
    mutation_file.write(head)
    temp_imports = "from .auth.auth import Mutation as AuthMutations"
    # for type_name, type_dic in schema['types'].items():
    #     mutation_file.write("from .queries.{} import {}Query\n".format(type_name, type_name))
    #     temp_import = temp_import + type_name + 'Query ,'
    # mutation_file.write("class Mutation({}graphene.ObjectType):\n".format(temp_import))
    mutation_file.write("class Mutation(AuthMutation,graphene.ObjectType):\n")
    mutation_file.write("\tpass")
    mutation_file.close()