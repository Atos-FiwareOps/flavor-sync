import json
import flavorsync.test.util as util

from novaclient.v2.flavors import Flavor as OpenStackFlavor

from flavorsync.model import Infrastructure, Flavor, FlavorCollection

def deserialize_xml_infrastructure_test():
    data = util.load_clean_xml_payload('infrastructure_request.xml')
    infrastructure = Infrastructure.deserialize(util.XML_MIMETYPE, data)
    _check_infrastructure_model_contents(infrastructure)

def deserialize_json_infrastructure_test():
    data = util.load_json_from_file('infrastructure_request.json')
    infrastructure = Infrastructure.deserialize(util.JSON_MIMETYPE, json.dumps(data))
    _check_infrastructure_model_contents(infrastructure)
    
def deserialize_wrong_mimetype_infrastructure_test():
    data = util.load_json_from_file('infrastructure_request.json')
    
    try:
        Infrastructure.deserialize(util.WRONG_MIMETYPE, data)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
    
def serialize_xml_infrastructure_test():
    data = util.load_clean_xml_payload('infrastructure_response.xml')
    
    infrastructure = util.create_example_infrastructure()
    
    infrastructure_xml = infrastructure.serialize(util.XML_MIMETYPE).decode('utf-8')
    assert infrastructure_xml in data
    
def serialize_json_infrastructure_test():
    file_json = util.load_json_from_file('infrastructure_response.json')
    
    infrastructure = util.create_example_infrastructure()
    
    infrastructure_json = infrastructure.serialize(util.JSON_MIMETYPE)
    assert util.json_are_equal(infrastructure_json, file_json)
    
def serialize_wrong_mimetype_infrastructure_test():
    infrastructure = util.create_example_infrastructure()
    
    try:
        infrastructure.serialize(util.WRONG_MIMETYPE)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def infrastructure_to_content_dict_test():
    infrastructure = util.create_example_infrastructure()
    assert 'Mordor' in infrastructure._to_content_dict()
    
def infrastructure_to_dict_test():
    expected_dict = {"infrastructure": {"name" : "Mordor"}}
    infrastructure = util.create_example_infrastructure()
    assert expected_dict == infrastructure.to_dict()




def deserialize_xml_flavor_test():
    data = util.load_clean_xml_payload('flavor_creation_request.xml')
    flavor = Flavor.deserialize(util.XML_MIMETYPE, data)
    _check_flavor_model_contents(flavor)

def deserialize_json_flavor_test():
    data = util.load_json_from_file('flavor_creation_request.json')
    flavor = Flavor.deserialize(util.JSON_MIMETYPE, json.dumps(data))
    _check_flavor_model_contents(flavor)
    
def deserialize_wrong_mimetype_flavor_test():
    data = util.load_json_from_file('flavor_creation_request.json')
    
    try:
        Flavor.deserialize(util.WRONG_MIMETYPE, data)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def serialize_xml_flavor_test():
    data = util.load_clean_xml_payload('flavor_response.xml')
    
    flavor = util.create_example_flavor()
    
    flavor_xml = flavor.serialize(util.XML_MIMETYPE).decode('utf-8')
    assert flavor_xml in data
    
def serialize_json_flavor_test():
    file_json = util.load_json_from_file('flavor_response.json')
    
    flavor = util.create_example_flavor()
    
    flavor_json = flavor.serialize(util.JSON_MIMETYPE)
    assert util.json_are_equal(flavor_json, file_json)
    
def serialize_wrong_mimetype_flavor_test():
    flavor = util.create_example_flavor()
    
    try:
        flavor.serialize(util.WRONG_MIMETYPE)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def flavor_to_content_dict_test():
    data = util.load_json_from_file('flavor_response.json')
    
    flavor = util.create_example_flavor()
    
    assert util.json_are_equal(data['flavor'], flavor._to_content_dict())
    
def flavor_to_dict_test():
    expected_dict = util.load_json_from_file('flavor_response.json')
    
    flavor = util.create_example_flavor()
    
    assert util.json_are_equal(expected_dict, flavor.to_dict())
    
def from_openstack_flavor_test():
    data = util.load_json_from_file('flavor_response.json')
    openstackflavor = OpenStackFlavor(None, data['flavor'])
    
    infrastructure = util.create_example_infrastructure()
    
    flavor = util.create_example_flavor()
    
    converted_flavor = Flavor.from_openstack_flavor(openstackflavor, infrastructure)
    
    assert util.json_are_equal(flavor.to_dict(), converted_flavor.to_dict())




def serialize_xml_flavor_collection_test():
    data = util.load_clean_xml_payload('flavor_collection_response.xml')
    
    flavor_collection = util.create_example_flavor_collection()
    
    flavor_collection_xml = flavor_collection.serialize(util.XML_MIMETYPE).decode('utf-8')
    assert flavor_collection_xml in data
    
def serialize_xml_empty_flavor_collection_test():
    data =  '<?xml version="1.0" encoding="UTF-8"?>'
    data += '<flavors/>'
    
    flavor_collection = FlavorCollection([])
    
    flavor_collection_xml = flavor_collection.serialize(util.XML_MIMETYPE).decode('utf-8')
    assert flavor_collection_xml in data
    
def serialize_json_flavor_collection_test():
    file_json = util.load_json_from_file('flavor_collection_response.json')
    
    flavor_collection = util.create_example_flavor_collection()
    
    flavor_collection_json = flavor_collection.serialize(util.JSON_MIMETYPE)
    assert util.json_are_equal(flavor_collection_json, file_json)
    
def serialize_json_empty_flavor_collection_test():
    data =  '{"flavors":[]}'
    
    flavor_collection = FlavorCollection([])
    
    flavor_collection_json = flavor_collection.serialize(util.JSON_MIMETYPE)
    assert util.json_are_equal(flavor_collection_json, data)
    
def serialize_wrong_mimetype_flavor_collection_test():
    flavor_collection = util.create_example_flavor_collection()
    
    try:
        flavor_collection.serialize(util.WRONG_MIMETYPE)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def flavor_collection_to_dict_test():
    expected_dict = util.load_json_from_file('flavor_collection_response.json')
    
    flavor_collection = util.create_example_flavor_collection()
    
    assert util.json_are_equal(expected_dict, flavor_collection.to_dict())
    
def emtpy_flavor_collection_to_dict_test():
    expected_dict =  {"flavors":[]}
    
    flavor_collection = FlavorCollection([])
    
    assert util.json_are_equal(expected_dict, flavor_collection.to_dict())
    
def from_openstack_flavor_list_test():
    data = util.load_json_from_file('flavor_collection_response.json')
    
    for flavor in data['flavors']:
        del(flavor['nodes'])
    
    openstackflavors = [OpenStackFlavor(None, data['flavors'][0]),
                        OpenStackFlavor(None, data['flavors'][1])]
    
    mordor = util.create_example_infrastructure()
    
    flavor_collection = util.create_example_flavor_collection(mordor)
    for flavor in flavor_collection.flavors:
        flavor.public = False
    
    converted_collection = FlavorCollection.from_openstack_flavor_list(
                                                    openstackflavors, mordor)
    
    assert util.json_are_equal(
                flavor_collection.to_dict(), converted_collection.to_dict())
    
def from_empty_openstack_flavor_list_test():
    mordor = util.create_example_infrastructure()
    
    flavor_collection = FlavorCollection([])
    
    converted_collection = FlavorCollection.from_openstack_flavor_list(
                                                    [], mordor)
    
    assert util.json_are_equal(
                flavor_collection.to_dict(), converted_collection.to_dict())
    
def flavor_collection_extend_list_test():
    flavor1 = util.create_example_flavor()
    flavor2 = util.create_secondary_example_flavor()
    
    flavor_collection1 = FlavorCollection([])
    flavor_collection2 = FlavorCollection([flavor1])
    flavor_collection3 = FlavorCollection([flavor2])
    
    flavors = [flavor1]
    flavor_collection1.extend(flavor_collection2)
    
    assert flavor_collection1.flavors == flavors
    
    flavors = [flavor1, flavor2]
    flavor_collection1.extend(flavor_collection3)
    
    assert flavor_collection1.flavors == flavors

def _check_infrastructure_model_contents(model):
    expected_infrastructure = util.create_example_infrastructure()
    
    assert expected_infrastructure.name in model.name
    assert expected_infrastructure.keystone_url in model.keystone_url
    assert expected_infrastructure.username in model.username
    assert expected_infrastructure.password in model.password
    assert expected_infrastructure.tenant in model.tenant

def _check_flavor_model_contents(model):
    expected_flavor = util.create_example_flavor()
    
    assert expected_flavor.name in model.name
    assert expected_flavor.vcpus == model.vcpus
    assert expected_flavor.ram == model.ram
    assert expected_flavor.disk == model.disk
    assert expected_flavor.swap == model.swap