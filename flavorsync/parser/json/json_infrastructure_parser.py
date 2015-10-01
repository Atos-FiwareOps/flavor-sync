from flask import json

from flavorsync.parser.json.json_parser import JSONParser

class JSONInfrastructureParser(JSONParser):
    def to_dict(self, data):
        return json.loads(data)['infrastructure']