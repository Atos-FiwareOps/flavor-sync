from flask import json

from flavorsync.parser.json.json_parser import JSONParser

class JSONFlavorParser(JSONParser):
	def __init__(self):
		print ("JSON flavor parser initialized")
	
	def to_dict(self, data):
		return json.loads(data)['flavor']