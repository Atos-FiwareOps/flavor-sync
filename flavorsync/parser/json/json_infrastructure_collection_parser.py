from flask import json

from flavorsync.parser.json.json_parser import JSONParser

class JSONInfrastructureCollectionParser(JSONParser):
    def __init__(self):
        super(JSONInfrastructureCollectionParser, self).__init__()