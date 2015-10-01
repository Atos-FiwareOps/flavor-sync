import json

from lxml import etree, objectify
from novaclient.v2.flavors import Flavor as OpenStackFlavor

from flavorsync.model import Infrastructure, Flavor, FlavorCollection
from flavorsync.test.util import XML_MIMETYPE, JSON_MIMETYPE, json_are_equal,\
    WRONG_MIMETYPE

JSON_EXAMPLE_PAYLOADS_DIR = 'flavorsync/test/example_payloads/json/'
XML_EXAMPLE_PAYLOADS_DIR = 'flavorsync/test/example_payloads/xml/'

def deserialize_xml_infrastructure_test():
    data = _load_xml_from_file('infrastructure_request.xml')
    decoded_data = etree.tostring(data).decode('utf-8')
    infrastructure = Infrastructure.deserialize(XML_MIMETYPE, decoded_data)
    _check_infrastructure_model_contents(
        infrastructure, 'Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')

def deserialize_json_infrastructure_test():
    data = _load_json_from_file('infrastructure_request.json')
    infrastructure = Infrastructure.deserialize(JSON_MIMETYPE, json.dumps(data))
    _check_infrastructure_model_contents(
        infrastructure, 'Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
def deserialize_wrong_mimetype_infrastructure_test():
    data = _load_json_from_file('infrastructure_request.json')
    
    try:
        infrastructure = Infrastructure.deserialize(WRONG_MIMETYPE, data)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
    
def serialize_xml_infrastructure_test():
    data = _load_xml_from_file('infrastructure_response.xml')
    decoded_data = etree.tostring(data).decode('utf-8')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructure_xml = infrastructure.serialize(XML_MIMETYPE).decode('utf-8')
    assert infrastructure_xml in decoded_data
    
def serialize_json_infrastructure_test():
    file_json = _load_json_from_file('infrastructure_response.json')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructure_json = infrastructure.serialize(JSON_MIMETYPE)
    assert json_are_equal(infrastructure_json, file_json)
    
def serialize_wrong_mimetype_infrastructure_test():
    file_json = _load_json_from_file('infrastructure_response.json')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    try:
        infrastructure_json = infrastructure.serialize(WRONG_MIMETYPE)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def infrastructure_to_content_dict_test():
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    assert 'Mordor' in infrastructure._to_content_dict()
    
def infrastructure_to_dict_test():
    expected_dict = {"infrastructure": {"name" : "Mordor"}}
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    assert expected_dict == infrastructure.to_dict()




def deserialize_xml_flavor_test():
    data = _load_xml_from_file('flavor_creation_request.xml')
    decoded_data = etree.tostring(data).decode('utf-8')
    flavor = Flavor.deserialize(XML_MIMETYPE, decoded_data)
    _check_flavor_model_contents(
        flavor, 'insane', 640, 1232896, 1262485504, 0)

def deserialize_json_flavor_test():
    data = _load_json_from_file('flavor_creation_request.json')
    flavor = Flavor.deserialize(JSON_MIMETYPE, json.dumps(data))
    _check_flavor_model_contents(
        flavor, 'insane', 640, 1232896, 1262485504, 0)
    
def deserialize_wrong_mimetype_flavor_test():
    data = _load_json_from_file('flavor_creation_request.json')
    
    try:
        flavor = Flavor.deserialize(WRONG_MIMETYPE, data)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def serialize_xml_flavor_test():
    data = _load_xml_from_file('flavor_response.xml')
    decoded_data = etree.tostring(data).decode('utf-8')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    flavor_xml = flavor.serialize(XML_MIMETYPE).decode('utf-8')
    assert flavor_xml in decoded_data
    
def serialize_json_flavor_test():
    file_json = _load_json_from_file('flavor_response.json')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    flavor_json = flavor.serialize(JSON_MIMETYPE)
    assert json_are_equal(flavor_json, file_json)
    
def serialize_wrong_mimetype_flavor_test():
    file_json = _load_json_from_file('flavor_response.json')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    try:
        flavor_json = flavor.serialize(WRONG_MIMETYPE)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def flavor_to_content_dict_test():
    data = _load_json_from_file('flavor_response.json')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    assert json_are_equal(data['flavor'], flavor._to_content_dict())
    
def flavor_to_dict_test():
    expected_dict = _load_json_from_file('flavor_response.json')
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    assert json_are_equal(expected_dict, flavor.to_dict())
    
def from_openstack_flavor_test():
    data = _load_json_from_file('flavor_creation_request.json')
    openstackflavor = OpenStackFlavor(None, data['flavor'])
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    converted_flavor = Flavor.from_openstack_flavor(flavor, infrastructure)
    
    assert json_are_equal(flavor.to_dict(), converted_flavor.to_dict())




def serialize_xml_flavor_collection_test():
    data = _load_xml_from_file('flavor_collection_response.xml')
    decoded_data = etree.tostring(data).decode('utf-8')
    
    saopaulo = Infrastructure('SaoPaulo', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    mordor = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures1 = [saopaulo]
    infrastructures2 = [mordor]
    
    flavor1 = Flavor('d1fb4620-f711-4393-b9f3-f2d476464daf', 'hpc', 16,
                16384, 100, 0, False, True, infrastructures1)
    flavor2 = Flavor('857dc211-e1f4-4cbe-b498-6847c14acb26', 'my_flavor', 2,
                512, 3, 0, False, False, infrastructures2)
    
    flavors = [flavor1, flavor2]
    flavor_collection = FlavorCollection(flavors)
    
    flavor_collection_xml = flavor_collection.serialize(XML_MIMETYPE).decode('utf-8')
    assert flavor_collection_xml in decoded_data
    
def serialize_json_flavor_collection_test():
    file_json = _load_json_from_file('flavor_collection_response.json')
    
    saopaulo = Infrastructure('SaoPaulo', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    mordor = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures1 = [saopaulo]
    infrastructures2 = [mordor]
    
    flavor1 = Flavor('d1fb4620-f711-4393-b9f3-f2d476464daf', 'hpc', 16,
                16384, 100, 0, False, True, infrastructures1)
    flavor2 = Flavor('857dc211-e1f4-4cbe-b498-6847c14acb26', 'my_flavor', 2,
                512, 3, 0, False, False, infrastructures2)
    
    flavors = [flavor1, flavor2]
    flavor_collection = FlavorCollection(flavors)
    
    flavor_collection_json = flavor_collection.serialize(JSON_MIMETYPE)
    assert json_are_equal(flavor_collection_json, file_json)
    
def serialize_wrong_mimetype_flavor_collection_test():
    file_json = _load_json_from_file('flavor_collection_response.json')
    
    saopaulo = Infrastructure('SaoPaulo', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    mordor = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures1 = [saopaulo]
    infrastructures2 = [mordor]
    
    flavor1 = Flavor('d1fb4620-f711-4393-b9f3-f2d476464daf', 'hpc', 16,
                16384, 100, 0, False, True, infrastructures1)
    flavor2 = Flavor('857dc211-e1f4-4cbe-b498-6847c14acb26', 'my_flavor', 2,
                512, 3, 0, False, False, infrastructures2)
    
    flavors = [flavor1, flavor2]
    flavor_collection = FlavorCollection(flavors)
    
    try:
        flavor_collection_json = flavor_collection.serialize(WRONG_MIMETYPE)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def flavor_collection_to_dict_test():
    expected_dict = _load_json_from_file('flavor_collection_response.json')
    
    saopaulo = Infrastructure('SaoPaulo', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    mordor = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures1 = [saopaulo]
    infrastructures2 = [mordor]
    
    flavor1 = Flavor('d1fb4620-f711-4393-b9f3-f2d476464daf', 'hpc', 16,
                16384, 100, 0, False, True, infrastructures1)
    flavor2 = Flavor('857dc211-e1f4-4cbe-b498-6847c14acb26', 'my_flavor', 2,
                512, 3, 0, False, False, infrastructures2)
    
    flavors = [flavor1, flavor2]
    flavor_collection = FlavorCollection(flavors)
    
    assert json_are_equal(expected_dict, flavor_collection.to_dict())
    
def from_openstack_flavor_list_test():
    data = _load_json_from_file('flavor_collection_response.json')
    
    for flavor in data['flavors']:
        del(flavor['nodes'])
    
    openstackflavor1 = OpenStackFlavor(None, data['flavors'][0])
    openstackflavor2 = OpenStackFlavor(None, data['flavors'][1])
    openstackflavors = [openstackflavor1, openstackflavor2]
    
    mordor = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [mordor]
    
    flavor1 = Flavor('d1fb4620-f711-4393-b9f3-f2d476464daf', 'hpc', 16,
                16384, 100, 0, False, False, infrastructures)
    flavor2 = Flavor('857dc211-e1f4-4cbe-b498-6847c14acb26', 'my_flavor', 2,
                512, 3, 0, False, False, infrastructures)
    
    flavors = [flavor1, flavor2]
    flavor_collection = FlavorCollection(flavors)
    
    converted_collection = FlavorCollection.from_openstack_flavor_list(
                                                    openstackflavors, mordor)
    
    assert json_are_equal(
                flavor_collection.to_dict(), converted_collection.to_dict())
    
def flavor_collection_extend_list_test():
    mordor = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    flavor1 = Flavor('d1fb4620-f711-4393-b9f3-f2d476464daf', 'hpc', 16,
                16384, 100, 0, False, True, [mordor])
    flavor2 = Flavor('857dc211-e1f4-4cbe-b498-6847c14acb26', 'my_flavor', 2,
                512, 3, 0, False, False, [mordor])
    flavor3 = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, [mordor])
    
    flavor_collection1 = FlavorCollection([])
    flavor_collection2 = FlavorCollection([flavor1])
    flavor_collection3 = FlavorCollection([flavor2, flavor3])
    
    flavors = [flavor1]
    flavor_collection1.extend(flavor_collection2)
    
    assert flavor_collection1.flavors == flavors
    
    flavors = [flavor1, flavor2, flavor3]
    flavor_collection1.extend(flavor_collection3)
    
    assert flavor_collection1.flavors == flavors


def _load_json_from_file(filename):
    full_path = JSON_EXAMPLE_PAYLOADS_DIR + filename
    
    with open(full_path) as payload_file:
        data = json.load(payload_file)
    
    return data

def _load_xml_from_file(filename):
    full_path = XML_EXAMPLE_PAYLOADS_DIR + filename
    
    with open(full_path) as payload_file:
        data = objectify.parse(payload_file)
    
    return data.getroot()

def _check_infrastructure_model_contents(model, name, nova_url, keystone_url,
                                    username, password, tenant):
    assert name in model.name
    assert nova_url in model.nova_url
    assert keystone_url in model.keystone_url
    assert username in model.username
    assert password in model.password
    assert tenant in model.tenant

def _check_flavor_model_contents(model, name, vcpus, ram, disk, swap):
    assert name in model.name
    assert vcpus == model.vcpus
    assert ram == model.ram
    assert disk == model.disk
    assert swap == model.swap