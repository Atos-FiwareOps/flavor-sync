from flavorsync.parser.parser import Parser
from flask import json

class JSONParser(Parser):
	def __init__(self):
		print ("JSON parser initialized")
	
	def from_model(self, data):
		return json.dumps(data.to_dict(), default=lambda o: o.__dict__)