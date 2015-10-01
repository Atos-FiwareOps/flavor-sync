import json

XML_MIMETYPE = 'application/xml'
JSON_MIMETYPE = 'application/json'
WRONG_MIMETYPE = 'application/whatever'

def json_are_equal(payload1, payload2):
	if type(payload1) is dict:
		payload1_json = payload1
	elif type(payload1) is str:
		payload1_json = json.loads(payload1)
	
	if type(payload2) is dict:
		payload2_json = payload2
	elif type(payload2) is str:
		payload2_json = json.loads(payload2)
	
	return _order_json_data(payload1_json) == _order_json_data(payload2_json)

def _order_json_data(obj):
    if isinstance(obj, dict):
        return sorted((k, _order_json_data(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(_order_json_data(x) for x in obj)
    else:
        return obj