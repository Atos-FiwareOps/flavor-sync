import json
import re

import flavorsync.test.config as config

from lxml import etree, objectify
from flavorsync.model import Infrastructure, Flavor, FlavorCollection

XML_MIMETYPE = 'application/xml'
JSON_MIMETYPE = 'application/json'
WRONG_MIMETYPE = 'application/whatever'

JSON_EXAMPLE_PAYLOADS_DIR = 'flavorsync/test/example_payloads/json/'
XML_EXAMPLE_PAYLOADS_DIR = 'flavorsync/test/example_payloads/xml/'

def load_xml_example_as_string(filename):
    return _load_example_file_as_string(XML_EXAMPLE_PAYLOADS_DIR + filename)

def load_json_example_as_string(filename):
    return _load_example_file_as_string(JSON_EXAMPLE_PAYLOADS_DIR + filename)

def _load_example_file_as_string(file_path):
    file = open(file_path, 'r')
    payload = file.read()
    file.close()
    
    if 'infrastructure_request' in file_path:
        payload = payload.replace("{OPENSTACK_TEST_KEYSTONE_URL}",
                                  config.OPENSTACK_TEST_KEYSTONE_URL)
        payload = payload.replace("{OPENSTACK_TEST_USERNAME}",
                                  config.OPENSTACK_TEST_USERNAME)
        payload = payload.replace("{OPENSTACK_TEST_PASSWORD}",
                                  config.OPENSTACK_TEST_PASSWORD)
        payload = payload.replace("{OPENSTACK_TEST_TENANT}",
                                  config.OPENSTACK_TEST_TENANT)
    
    return payload

def load_xml_from_file(filename):
    contents = load_clean_xml_payload(filename)
    root = objectify.fromstring(contents)
    return root

def load_clean_xml_payload(filename):
    payload = load_xml_example_as_string(filename)
    payload = remove_xml_header(payload)
    payload = remove_non_usable_characters(payload)
    
    return payload

def load_json_from_file(filename):
    contents = load_json_example_as_string(filename)
    data = json.loads(contents)
    
    return data

def remove_xml_header(xml):
    return re.sub("<\?.*\?>", "", xml)
    
def remove_non_usable_characters(xml):
    parsed_xml = re.sub("\\n", "", xml)
    parsed_xml = re.sub(" +<", "<", parsed_xml)
    parsed_xml = re.sub("> +", ">", parsed_xml)
    return parsed_xml

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
       
def create_example_infrastructure():
    return Infrastructure('Mordor',
                          config.OPENSTACK_TEST_KEYSTONE_URL,
                          config.OPENSTACK_TEST_USERNAME,
                          config.OPENSTACK_TEST_PASSWORD,
                          config.OPENSTACK_TEST_TENANT)

def _create_secondary_example_infrastructure():
    return Infrastructure('SaoPaulo', 'http://55.66.77.88:35357/',
                          'myUsername', 'myPassword', 'myTenant')

def create_example_flavor(infrastructure=None):
    if not infrastructure:
        infrastructure = create_example_infrastructure()
    
    infrastructures = [infrastructure]
    
    return Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                  1232896, 1262485504, 0, False, False, infrastructures)

def create_secondary_example_flavor(infrastructure=None):
    if not infrastructure:
        infrastructure = _create_secondary_example_infrastructure()
    
    infrastructures = [infrastructure]
    
    return Flavor('857dc211-e1f4-4cbe-b498-6847c14acb26', 'hpc', 16,
                  5120, 100, 0, False, True, infrastructures)

def create_example_flavor_collection(infrastructure=None):
    flavors = [create_example_flavor(infrastructure), create_secondary_example_flavor(infrastructure)]
    
    return FlavorCollection(flavors)