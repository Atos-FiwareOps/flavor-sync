import flavorsync.test.util as util

from flavorsync.parser.parser_factory import ParserFactory
from flavorsync.model import Infrastructure, Flavor, FlavorCollection, FlavorInfrastructureLink
from flavorsync.parser.xml.xml_infrastructure_parser import XMLInfrastructureParser
from flavorsync.exceptions import FlavorSyncError
from flavorsync.parser.xml.xml_flavor_collection_parser import XMLFlavorCollectionParser
from flavorsync.parser.xml.xml_exception_parser import XMLExceptionParser
from flavorsync.parser.xml.xml_flavor_parser import XMLFlavorParser
from flavorsync.parser.json.json_infrastructure_parser import JSONInfrastructureParser
from flavorsync.parser.json.json_flavor_parser import JSONFlavorParser
from flavorsync.parser.json.json_flavor_collection_parser import JSONFlavorCollectionParser
from flavorsync.parser.json.json_exception_parser import JSONExceptionParser
from flavorsync.parser.parser import Parser

def create_xml_infrastructure_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, Infrastructure)
    
    assert type(type_factory) is XMLInfrastructureParser
    
def create_xml_flavor_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, Flavor)
    
    assert type(type_factory) is XMLFlavorParser
    
def create_xml_flavor_collection_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, FlavorCollection)
    
    assert type(type_factory) is XMLFlavorCollectionParser
    
def create_xml_exception_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, FlavorSyncError)
    
    assert type(type_factory) is XMLExceptionParser




def create_json_infrastructure_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, Infrastructure)
    
    assert type(type_factory) is JSONInfrastructureParser
    
def create_json_flavor_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, Flavor)
    
    assert type(type_factory) is JSONFlavorParser
    
def create_json_flavor_collection_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorCollection)
    
    assert type(type_factory) is JSONFlavorCollectionParser
    
def create_json_exception_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorSyncError)
    
    assert type(type_factory) is JSONExceptionParser




def create_wrong_mimetype_infrastructure_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.WRONG_MIMETYPE, Infrastructure)
    
    assert type(type_factory) is Parser
    
def create_wrong_mimetype_flavor_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.WRONG_MIMETYPE, Flavor)
    
    assert type(type_factory) is Parser
    
def create_wrong_mimetype_flavor_collection_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.WRONG_MIMETYPE, FlavorCollection)
    
    assert type(type_factory) is Parser
    
def create_wrong_mimetype_exception_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.WRONG_MIMETYPE, FlavorSyncError)
    
    assert type(type_factory) is Parser




def create_xml_wrong_type_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, FlavorInfrastructureLink)
    
    assert type(type_factory) is Parser
    
def create_json_wrong_type_parser_factory_test():
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorInfrastructureLink)
    
    assert type(type_factory) is Parser




def xml_infrastructure_to_dict_parser_test():
    payload = util.load_xml_example_as_string('infrastructure_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = ParserFactory()
    infrastructure_factory = factory.get_parser(util.XML_MIMETYPE, Infrastructure)
    
    infrastructure = infrastructure_factory.to_dict(payload)
    _check_infrastructure_dict_contents(
        infrastructure, 'Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')

def xml_flavor_to_dict_parser_test():
    payload = util.load_xml_example_as_string('flavor_creation_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    _check_flavor_dict_contents(
        flavor, 'insane', 640, 1232896, 1262485504, 0)

def xml_flavor_publication_to_dict_parser_test():
    payload = util.load_xml_from_file('flavor_publication_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['public']

def xml_flavor_promotion_to_dict_parser_test():
    payload = util.load_xml_example_as_string('flavor_promotion_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['promoted']

def xml_flavor_installation_to_dict_parser_test():
    payload = util.load_xml_example_as_string('flavor_installation_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert len(flavor['nodes']) == 1
    assert 'Mordor' in flavor['nodes'][0]




def json_infrastructure_to_dict_parser_test():
    payload = util.load_json_example_as_string('infrastructure_request.json')
    factory = ParserFactory()
    infrastructure_factory = factory.get_parser(util.JSON_MIMETYPE, Infrastructure)
    
    infrastructure = infrastructure_factory.to_dict(payload)
    _check_infrastructure_dict_contents(
        infrastructure, 'Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')

def json_flavor_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_creation_request.json')
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    _check_flavor_dict_contents(
        flavor, 'insane', 640, 1232896, 1262485504, 0)

def json_flavor_publication_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_publication_request.json')
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['public']

def json_flavor_promotion_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_promotion_request.json')
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['promoted']

def json_flavor_installation_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_installation_request.json')
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert len(flavor['nodes']) == 1
    assert 'Mordor' in flavor['nodes'][0]




def xml_flavor_collection_to_dict_parser_test():
    payload = util.load_xml_example_as_string('flavor_collection_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, FlavorCollection)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)

def xml_exception_to_dict_parser_test():
    payload = util.load_xml_example_as_string('exception_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, FlavorSyncError)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)

def json_flavor_collection_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_collection_response.json')
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorCollection)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def json_exception_to_dict_parser_test():
    payload = util.load_json_example_as_string('exception_response.json')
    
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorSyncError)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)




def xml_infrastructure_from_model_parser_test():
    payload = util.load_xml_example_as_string('infrastructure_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    factory = ParserFactory()
    infrastructure_factory = factory.get_parser(util.XML_MIMETYPE, Infrastructure)
    
    response = infrastructure_factory.from_model(infrastructure)
    assert response.decode("utf-8") in payload
    
def xml_flavor_from_model_parser_test():
    payload = util.load_xml_example_as_string('flavor_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.XML_MIMETYPE, Flavor)
    
    response = flavor_factory.from_model(flavor)
    assert response.decode("utf-8") in payload
    
def xml_flavor_collection_from_model_parser_test():
    payload = util.load_xml_example_as_string('flavor_collection_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    
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
    
    factory = ParserFactory()
    collection_factory = factory.get_parser(util.XML_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert response.decode("utf-8") in payload
    
def xml_empty_flavor_collection_from_model_parser_test():
    payload =  '<?xml version="1.0" encoding="UTF-8"?>'
    payload += '<flavors/>'
    
    flavor_collection = FlavorCollection([])
    
    factory = ParserFactory()
    collection_factory = factory.get_parser(util.XML_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert response.decode("utf-8") in payload
    
def xml_error_from_model_parser_test():
    payload = util.load_xml_example_as_string('exception_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    
    factory = ParserFactory()
    type_factory = factory.get_parser(util.XML_MIMETYPE, FlavorSyncError)
    
    error = FlavorSyncError('Error message')
    
    response = type_factory.from_model(error)
    assert response.decode("utf-8") in payload




def json_infrastructure_from_model_parser_test():
    payload = util.load_json_from_file('infrastructure_response.json')
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    factory = ParserFactory()
    infrastructure_factory = factory.get_parser(util.JSON_MIMETYPE, Infrastructure)
    
    response = infrastructure_factory.from_model(infrastructure)
    assert util.json_are_equal(response, payload)
    
def json_flavor_from_model_parser_test():
    payload = util.load_json_from_file('flavor_response.json')
    infrastructure = Infrastructure('Mordor', 'http://11.22.33.44:8776/',
        'http://55.66.77.88:35357/', 'myUsername', 'myPassword', 'myTenant')
    
    infrastructures = [infrastructure]
    
    flavor = Flavor('567b200e-0aca-49e0-8e9a-8c1f6ad3abe2', 'insane', 640,
                1232896, 1262485504, 0, False, False, infrastructures)
    
    factory = ParserFactory()
    flavor_factory = factory.get_parser(util.JSON_MIMETYPE, Flavor)
    
    response = flavor_factory.from_model(flavor)
    assert util.json_are_equal(response, payload)
    
def json_flavor_collection_from_model_parser_test():
    payload = util.load_json_from_file('flavor_collection_response.json')
    
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
    
    factory = ParserFactory()
    collection_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert util.json_are_equal(response, payload)
    
def json_empty_flavor_collection_from_model_parser_test():
    payload =  '{"flavors":[]}'
    
    flavor_collection = FlavorCollection([])
    
    factory = ParserFactory()
    collection_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert util.json_are_equal(response, payload)
    
def json_error_from_model_parser_test():
    payload = util.load_json_from_file('exception_response.json')
    
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorSyncError)
    
    error = FlavorSyncError('Error message')
    
    response = type_factory.from_model(error)
    assert util.json_are_equal(response, payload)

def _check_infrastructure_dict_contents(dictionary, name, nova_url,
                                    keystone_url, username, password, tenant):
    assert name in dictionary['name']
    assert nova_url in dictionary['nova_url']
    assert keystone_url in dictionary['keystone_url']
    assert username in dictionary['username']
    assert password in dictionary['password']
    assert tenant in dictionary['tenant']

def _check_flavor_dict_contents(dictionary, name, vcpus, ram, disk, swap):
    assert name in dictionary['name']
    assert vcpus == dictionary['vcpus']
    assert ram == dictionary['ram']
    assert disk == dictionary['disk']
    assert swap == dictionary['swap']