from subprocess import call
import os
import sys
from logger import Logger
from distutils.dir_util import copy_tree
import shutil


def prepare_project_structure(schema):
    # get project title from schema file
    if 'project_title' in schema.keys():
        project_title = schema['project_title']
    else:
        # if not set by user set it to myProject by default
        project_title = "myProject"
        # set schema project title to default value
        schema['project_title'] = project_title
        Logger("please provide a project_title in the .yaml file", "warning").show()
        Logger("project title is set by default to myProject", "info").show()
    # get main app name
    if 'main_app' in schema.keys():
        main_app = schema['main_app']
    else:
        # if not set by user set it to app1 by default
        main_app = "app1"
        #set schema main app
        schema['main_app'] = main_app
        Logger("please provide a main_app in the .yaml file", "warning").show()
        Logger("main app name is set to app1 by default", "info").show()
    try:
        # start a django app
        call("django-admin startproject {}".format(project_title), shell=True)
        # start an app
        call("python ./{}/manage.py startapp {}".format(project_title, main_app), shell=True)
        # copy  app files into project directory
        copy_tree('./{}'.format(main_app), './{}/{}'.format(project_title, main_app))
        # delete app copied app folder
        shutil.rmtree('./{}'.format(main_app))
        # create empty folders for the rest of the generated files
        os.makedirs('./{}/{}/models_files'.format(project_title, main_app))
        os.makedirs('./{}/{}/graphql'.format(project_title, main_app))
        os.makedirs('./{}/{}/graphql/queries'.format(project_title, main_app))
        os.makedirs('./{}/{}/graphql/mutations'.format(project_title, main_app))
        os.makedirs('./{}/{}/graphql/auth'.format(project_title, main_app))
        # register main app in settings file
        register_app_in_settings(schema)
        # register Auth_sys
        register_auth_system(schema)
        # show progress message
        Logger("project skeleton has been created", "progress").show()
        # register graphql routes
        register_graphql_routes(schema)

    except Exception as ex:
        raise ex
        # Logger("sorry an error occured while creating project structure", "error")
        # Logger(
        #     "make sure that there is no folder exist with same name and you have required permissions to create folders",
        #     "hint")
        # # sys.exit(0)
def register_app_in_settings(schema):
    setting_file = open("./{}/{}/settings.py".format(schema['project_title'], schema['project_title']), "r")
    setting_lines = setting_file.readlines()
    setting_lines[38] = setting_lines[38] + '\t\'graphene_django\',\n\t\'{}\'\n'.format(schema['main_app'])
    setting_file.close()
    setting_file = open("./{}/{}/settings.py".format(schema['project_title'], schema['project_title']), "w")
    setting_file.writelines(setting_lines)
    setting_file.close()
def register_auth_system(schema):
    # read settings file before writing
    setting_file = open("./{}/{}/settings.py".format(schema['project_title'], schema['project_title']), "r")
    setting_lines = setting_file.readlines()
    setting_lines[48] = setting_lines[48] + '\t\'graphql_jwt.middleware.JSONWebTokenMiddleware\',\n'.format(schema['main_app'])
    setting_file.close()
    # adding Graphene schema to settings
    setting_lines.append("GRAPHENE = {\n\t " + "\'SCHEMA\'" + ": \'"+schema['main_app']+ ".graphql.schema.Schema\',\n}\n")
   # adding Auth_Backends
    setting_lines.append("AUTHENTICATION_BACKENDS = [\n\t\'graphql_jwt.backends.JSONWebTokenBackend\',\n\t\'django.contrib.auth.backends.ModelBackend\',\n]")
    # start writing
    setting_file = open("./{}/{}/settings.py".format(schema['project_title'], schema['project_title']), "w")
    setting_file.writelines(setting_lines)
    setting_file.close()
def register_graphql_routes(schema):
    routes_file = open("./{}/{}/urls.py".format(schema['project_title'], schema['project_title']), "w")
    routes_body = """from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
] """
    routes_file.write(routes_body)
    routes_file.close()