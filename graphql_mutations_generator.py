import os

types = {
    'Int': 'Int()',
    'Float': "Float()",
    'Boolean': 'Boolean()',
    'String': "String()",
    'File': "String()"
}
def generate_mutations(schema):

    for type_name, type_dic in schema['types'].items():
        file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/mutations/{}.py".format(
            schema['project_title'], schema['main_app'], type_name)), "w+")
        file.write("import graphene\n")

        # importing foreign models
        foreign_imports = ""
        for field in type_dic['fields']:
            field_name, field_type = list(field.items())[0]
            if field_type not in types:
                if 'options' in field.keys() and 'many' in field['options']:
                    pass
                else:
                    foreign_imports = foreign_imports + ",{}".format(field_type)
                    file.write("from ..types import {}Type\n".format(field_type))
        file.write("from ...models import {} {}\n".format(type_name,foreign_imports))

        file.write("class Create{}(graphene.Mutation):\n".format(type_name))
        file.write("\t# output\n")
        # step #1 prepare output section
        output_fields = "\tid = graphene.Int()\n"
        for field in type_dic['fields']:
            field_name, field_type = list(field.items())[0]
            if field_type in types:
                output_fields = output_fields + '\t{} = graphene.{}\n'.format(field_name, types[field_type])
            else:
                if 'options' in field.keys() and 'many' in field['options']:
                    pass
                else:
                    output_fields = output_fields + '\t{} = graphene.Field({}Type)\n'.format(field_name,field_type)
        file.write(output_fields)
        # step #2 prepare Arguments class
        file.write("\tclass Arguments:\n")
        arguments_fields = ""
        for field in type_dic['fields']:
            field_name, field_type = list(field.items())[0]
            if field_type in types:
                arguments_fields = arguments_fields + '\t\t{} = graphene.{}\n'.format(field_name, types[field_type])
            else:
                if 'options' in field.keys() and 'many' in field['options']:
                    pass
                else:
                    arguments_fields = arguments_fields + "\t\t{}_id = graphene.Int()\n".format(field_type.lower())

        file.write(arguments_fields)
        # step #3 prepare mutate method for creation of an object
        mutate_function_arguments = ""
        for field in type_dic['fields']:
            field_name, field_type = list(field.items())[0]
            if field_type in types:
                mutate_function_arguments = mutate_function_arguments + '{},'.format(field_name)
            else:
                if 'options' in field.keys() and 'many' in field['options']:
                    pass
                else:
                    mutate_function_arguments = mutate_function_arguments + "{}_id,".format(field_type.lower())
        file.write("\tdef mutate(self,info,{}):\n".format(mutate_function_arguments[:-1]))
        # prepare foreign objects
        for field in type_dic['fields']:
            field_name, field_type = list(field.items())[0]
            if field_type not in types:
                if 'options' in field.keys() and 'many' in field['options']:
                    pass
                else:
                    file.write("\t\t{} = {}.objects.get(pk={}_id)\n".format(field_name,field_type,field_type.lower()))
        constructor_arguments = ""
        for field in type_dic['fields']:
            field_name, field_type = list(field.items())[0]
            if field_type in types:
                constructor_arguments = constructor_arguments + '{} = {} ,'.format(field_name, field_name)
            else:
                if 'options' in field.keys() and 'many' in field['options']:
                    pass
                else:
                    constructor_arguments = constructor_arguments + '{} = {} ,'.format(field_name, field_name)
        file.write("\t\t{} = {}({})\n".format(type_name.lower(),type_name,constructor_arguments[:-1]))
        file.write("\t\t{}.save()\n".format(type_name.lower()))
        # generate return statement
        file.write("\t\treturn Create{}(\n".format(type_name))
        return_arguments = "\t\t{}.id,\n".format(type_name.lower())
        for field in type_dic['fields']:
            field_name, field_type = list(field.items())[0]
            return_arguments = return_arguments + '\t\t{}.{},\n'.format(type_name.lower(),field_name)
        file.write(return_arguments+"\n\t\t)\n")
        file.write("class Mutation(graphene.ObjectType):\n")
        file.write("\tcreate_{} = Create{}.Field()".format(type_name.lower(),type_name))
        file.close()

    mutation_file = open(os.path.join(os.getcwd(), "./{}/{}/graphql/mutation.py".format(
        schema['project_title'], schema['main_app'])), "w+")
    head = "import graphene\n"
    auth_imports = "from .auth.auth import Mutation as AuthMutations\n"
    mutation_file.write(head)
    mutation_file.write(auth_imports)
    temp_import = ""
    for type_name, type_dic in schema['types'].items():
        mutation_file.write("from .mutations.{} import Mutation as {}Mutations\n".format(type_name, type_name))
        temp_import = temp_import + type_name + 'Mutations ,'
    mutation_file.write("class Mutation(AuthMutations,{}graphene.ObjectType):\n".format(temp_import))
    mutation_file.write("\tpass")
    mutation_file.close()
