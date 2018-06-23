from subprocess import call
import os
import sys
from logger import Logger
from distutils.dir_util import copy_tree
import shutil
def prepare_project_structure(schema):
    print(schema.keys())
    # get project title from schema file
    if 'project_title' in schema.keys():
        project_title = schema['project_title']
    else:
        #if not set by user set it to myProject by default
        project_title = "myProject"
        Logger("please provide a project_title in the .yaml file","hint").show()
        Logger("project title is set by default to myProject","info").show()
    #get main app name
    if 'main_app' in schema.keys():
        main_app = schema['main_app']
    else:
        #if not set by user set it to app1 by default
        main_app = "app1"
        Logger("please provide a main_app in the .yaml file","hint").show()
        Logger("main app title is set by default to myProject","info").show()
    try:
        # start a django app
        call("django-admin startproject {}".format(project_title),shell=True)
        # start an app
        call("python ./{}/manage.py startapp {}".format(project_title,main_app), shell=True)
        # copy  app files into project directory
        copy_tree('./{}'.format(main_app), './{}/{}'.format(project_title,main_app))
        # delete app copied app folder
        shutil.rmtree('./{}'.format(main_app))
        # create empty folders for the rest of the generated files
        os.makedirs('./{}/{}/models_file'.format(project_title, main_app))
        os.makedirs('./{}/{}/graphql'.format(project_title, main_app))
        os.makedirs('./{}/{}/graphql/queries'.format(project_title, main_app))
        os.makedirs('./{}/{}/graphql/mutations'.format(project_title, main_app))
        Logger("project skeleton has been created","progress").show()

    except Exception as ex:
        Logger("sorry an error occured while creating project structure","error")
        Logger("make sure that there is no folder exist with same name and you have required permissions to create folders","hint")
        sys.exit(0)