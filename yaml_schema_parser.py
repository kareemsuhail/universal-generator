import yaml
import sys
from logger import Logger
class Parser:
    def __init__(self,schema_path="schema.yaml"):
        self.schema_path = schema_path
    def read(self):
        with open(self.schema_path, 'r') as stream:
            try:
                print(yaml.load(stream))
            except yaml.YAMLError as exc:
                Logger("An error occurred while reading Yaml file","error").show()
                Logger("make sure that your schema file is in correct format","hint").show()

                sys.exit(0)