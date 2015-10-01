from flask import json

from flavorsync.parser.json.json_parser import JSONParser

class JSONFlavorCollectionParser(JSONParser):
    def __init__(self):
        super(JSONFlavorCollectionParser, self).__init__()