import os,sys
from logger import  Logger
types = {
         'Int': 'IntegerField()',
         'Float': "FloatField()",
         'Boolean': 'BooleanField()',
         'String': "CharField(max_length=200)",
         'File': "FileField(upload_to='uploads/')"
         }


def generate_models(schema):
    head = 'from django.db import models\n'
    for type_name,type_dic in schema['types'].items():
        file = open(os.path.join(os.getcwd(), "./{}/{}/models_files/{}.py".format(
            schema['project_title'], schema['main_app'], type_name)), "w+")
        body = 'class {}(models.Model):\n'.format(type_name)
        for field in type_dic['fields']:
            field_name,field_type = list(field.items())[0]
            if field_type in types:
                tempField = '\t{} = models.{}\n'.format(field_name, types[field_type])
            else:
                if 'options' in field.keys() and 'many' in field['options']:
                    tempField = "\t{} = models.ManyToManyField('{}')\n".format(field_name, field_type)
                else:
                    tempField = "\t{} = models.ForeignKey('{}',on_delete=models.CASCADE)\n".format(field_name,
                                                                                                   field_type)
            body = body + tempField
        file.write(head + body)
        # register models
        register_models(schema)
def register_models(schema):
    with open("./{}/{}/models.py".format(schema['project_title'],schema['main_app']),"w") as stream:
        try:
            header = "from django.db import models\n"
            body = ""
            for type_name,type_dic in schema['types'].items():
                body = body + "from .models_files.{} import {}".format(type_name,type_name)
            stream.write(header+body)
        except Exception as ex:
            Logger("an error occurred while registering models","error")
            sys.exit(0)