import os
def generate_types(schema):
    types_file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/types.py".format(
        schema['project_title'], schema['main_app'])), "w+")
    file_head = 'from graphene_django import DjangoObjectType\nimport graphene\n'

    # import models
    for type_name, type_dic in schema['types'].items():
        file_head = file_head + "from ..models import {}\n".format(type_name, type_name)
    types_file.write(file_head)
    for type_name, type_dic in schema['types'].items():
        many_to_many = checkIfContainMany(type_dic)
        temp_head = ""
        temp_resolver = ""
        if len(many_to_many) > 0:
            for many_field in many_to_many:
                temp_head = temp_head + "\t{} = graphene.List({}Type)\n".format(many_field['name'], many_field['type'])
                temp_resolver = temp_resolver + "\t@graphene.resolve_only_args\n\tdef resolve_{}(self):\n\t\treturn self.{}.all()\n".format(
                    many_field['name'], many_field['name'])
        types_file.write("class {}Type(DjangoObjectType):\n".format(type_name))
        types_file.write(temp_head)
        types_file.write(temp_resolver)
        types_file.write("\tclass Meta:\n")
        types_file.write("\t\tmodel={}\n".format(type_name))
    types_file.close()


def checkIfContainMany(type):
    result = []
    for field in type['fields']:
        if ('options' in field and 'many' in field['options']):
            result.append(field)
    return result
