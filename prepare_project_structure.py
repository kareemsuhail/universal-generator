from subprocess import call
from logger import Logger
def prepare_project_structure(schema):
    # get project title from schema file
    if 'project_title' in schema.keys():
        project_title = schema['project_title']
    else:
        #if not set by user set it to myProject by default
        project_title = "myProject"
        Logger("please provide a project_title in the .yaml file","info")
        Logger("project title is set by default to myProject","info")
