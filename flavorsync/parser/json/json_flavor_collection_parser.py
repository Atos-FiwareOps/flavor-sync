from flask import json

from flavorsync.parser.json.json_parser import JSONParser

class JSONFlavorCollectionParser(JSONParser):
	def __init__(self):
		print ("JSON flavor collection parser initialized")
	
	def to_dict(self, data):
		return json.loads(data)
	