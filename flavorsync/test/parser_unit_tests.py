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
    _create_parser_factory_test(util.XML_MIMETYPE, Infrastructure, XMLInfrastructureParser)
    
def create_xml_flavor_parser_factory_test():
    _create_parser_factory_test(util.XML_MIMETYPE, Flavor, XMLFlavorParser)
    
def create_xml_flavor_collection_parser_factory_test():
    _create_parser_factory_test(util.XML_MIMETYPE, FlavorCollection, XMLFlavorCollectionParser)
    
def create_xml_exception_parser_factory_test():
    _create_parser_factory_test(util.XML_MIMETYPE, FlavorSyncError, XMLExceptionParser)




def create_json_infrastructure_parser_factory_test():
    _create_parser_factory_test(util.JSON_MIMETYPE, Infrastructure, JSONInfrastructureParser)
    
def create_json_flavor_parser_factory_test():
    _create_parser_factory_test(util.JSON_MIMETYPE, Flavor, JSONFlavorParser)
    
def create_json_flavor_collection_parser_factory_test():
    _create_parser_factory_test(util.JSON_MIMETYPE, FlavorCollection, JSONFlavorCollectionParser)
    
def create_json_exception_parser_factory_test():
    _create_parser_factory_test(util.JSON_MIMETYPE, FlavorSyncError, JSONExceptionParser)




def create_wrong_mimetype_infrastructure_parser_factory_test():
    _create_parser_factory_test(util.WRONG_MIMETYPE, Infrastructure, Parser)
    
def create_wrong_mimetype_flavor_parser_factory_test():
    _create_parser_factory_test(util.WRONG_MIMETYPE, Flavor, Parser)
    
def create_wrong_mimetype_flavor_collection_parser_factory_test():
    _create_parser_factory_test(util.WRONG_MIMETYPE, FlavorCollection, Parser)
    
def create_wrong_mimetype_exception_parser_factory_test():
    _create_parser_factory_test(util.WRONG_MIMETYPE, FlavorSyncError, Parser)




def create_xml_wrong_type_parser_factory_test():
    _create_parser_factory_test(util.XML_MIMETYPE, FlavorInfrastructureLink, Parser)
    
def create_json_wrong_type_parser_factory_test():
    _create_parser_factory_test(util.JSON_MIMETYPE, FlavorInfrastructureLink, Parser)




def xml_infrastructure_to_dict_parser_test():
    payload = util.load_clean_xml_payload('infrastructure_request.xml')
    infrastructure_factory = _create_factory(util.XML_MIMETYPE, Infrastructure)
    
    infrastructure = infrastructure_factory.to_dict(payload)
    _check_infrastructure_dict_contents(infrastructure)

def xml_flavor_to_dict_parser_test():
    payload = util.load_clean_xml_payload('flavor_creation_request.xml')
    flavor_factory = _create_factory(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    _check_flavor_dict_contents(flavor)

def xml_flavor_publication_to_dict_parser_test():
    payload = util.load_clean_xml_payload('flavor_publication_request.xml')
    flavor_factory = _create_factory(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['public']

def xml_flavor_promotion_to_dict_parser_test():
    payload = util.load_clean_xml_payload('flavor_promotion_request.xml')
    flavor_factory = _create_factory(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['promoted']

def xml_flavor_installation_to_dict_parser_test():
    payload = util.load_clean_xml_payload('flavor_installation_request.xml')
    flavor_factory = _create_factory(util.XML_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert len(flavor['nodes']) == 1
    assert 'Mordor' in flavor['nodes'][0]




def json_infrastructure_to_dict_parser_test():
    payload = util.load_json_example_as_string('infrastructure_request.json')
    infrastructure_factory = _create_factory(util.JSON_MIMETYPE, Infrastructure)
    
    infrastructure = infrastructure_factory.to_dict(payload)
    _check_infrastructure_dict_contents(infrastructure)

def json_flavor_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_creation_request.json')
    flavor_factory = _create_factory(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    _check_flavor_dict_contents(flavor)

def json_flavor_publication_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_publication_request.json')
    flavor_factory = _create_factory(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['public']

def json_flavor_promotion_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_promotion_request.json')
    flavor_factory = _create_factory(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert flavor['promoted']

def json_flavor_installation_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_installation_request.json')
    flavor_factory = _create_factory(util.JSON_MIMETYPE, Flavor)
    
    flavor = flavor_factory.to_dict(payload)
    assert len(flavor['nodes']) == 1
    assert 'Mordor' in flavor['nodes'][0]




def xml_flavor_collection_to_dict_parser_test():
    payload = util.load_clean_xml_payload('flavor_collection_response.xml')
    type_factory = _create_factory(util.XML_MIMETYPE, FlavorCollection)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)

def xml_exception_to_dict_parser_test():
    payload = util.load_clean_xml_payload('exception_response.xml')
    type_factory = _create_factory(util.XML_MIMETYPE, FlavorSyncError)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)

def json_flavor_collection_to_dict_parser_test():
    payload = util.load_json_example_as_string('flavor_collection_response.json')
    type_factory = _create_factory(util.JSON_MIMETYPE, FlavorCollection)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)
    
def json_exception_to_dict_parser_test():
    payload = util.load_json_example_as_string('exception_response.json')
    type_factory = _create_factory(util.JSON_MIMETYPE, FlavorSyncError)
    
    try:
        type_factory.to_dict(payload)
        assert False
    except NotImplementedError as e:
        assert 'Unrecognized mimetype or model type' in str(e)




def xml_infrastructure_from_model_parser_test():
    payload = util.load_clean_xml_payload('infrastructure_response.xml')
    
    infrastructure = util.create_example_infrastructure()
    
    infrastructure_factory = _create_factory(util.XML_MIMETYPE, Infrastructure)
    
    response = infrastructure_factory.from_model(infrastructure)
    assert response.decode("utf-8") in payload
    
def xml_flavor_from_model_parser_test():
    payload = util.load_clean_xml_payload('flavor_response.xml')
    
    flavor = util.create_example_flavor()
    
    flavor_factory = _create_factory(util.XML_MIMETYPE, Flavor)
    
    response = flavor_factory.from_model(flavor)
    assert response.decode("utf-8") in payload
    
def xml_flavor_collection_from_model_parser_test():
    payload = util.load_clean_xml_payload('flavor_collection_response.xml')
    
    flavor_collection = util.create_example_flavor_collection()
    
    collection_factory = _create_factory(util.XML_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert response.decode("utf-8") in payload
    
def xml_empty_flavor_collection_from_model_parser_test():
    payload =  '<?xml version="1.0" encoding="UTF-8"?>'
    payload += '<flavors/>'
    
    flavor_collection = FlavorCollection([])
    
    collection_factory = _create_factory(util.XML_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert response.decode("utf-8") in payload
    
def xml_error_from_model_parser_test():
    payload = util.load_clean_xml_payload('exception_response.xml')
    
    type_factory = _create_factory(util.XML_MIMETYPE, FlavorSyncError)
    
    error = FlavorSyncError('Error message')
    
    response = type_factory.from_model(error)
    assert response.decode("utf-8") in payload




def json_infrastructure_from_model_parser_test():
    payload = util.load_json_from_file('infrastructure_response.json')
    infrastructure = util.create_example_infrastructure()
    
    infrastructure_factory = _create_factory(util.JSON_MIMETYPE, Infrastructure)
    
    response = infrastructure_factory.from_model(infrastructure)
    assert util.json_are_equal(response, payload)
    
def json_flavor_from_model_parser_test():
    payload = util.load_json_from_file('flavor_response.json')
    flavor = util.create_example_flavor()
    
    flavor_factory = _create_factory(util.JSON_MIMETYPE, Flavor)
    
    response = flavor_factory.from_model(flavor)
    assert util.json_are_equal(response, payload)
    
def json_flavor_collection_from_model_parser_test():
    payload = util.load_json_from_file('flavor_collection_response.json')
    
    flavor_collection = util.create_example_flavor_collection()
    
    collection_factory = _create_factory(util.JSON_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert util.json_are_equal(response, payload)
    
def json_empty_flavor_collection_from_model_parser_test():
    payload =  '{"flavors":[]}'
    
    flavor_collection = FlavorCollection([])
    
    collection_factory = _create_factory(util.JSON_MIMETYPE, FlavorCollection)
    
    response = collection_factory.from_model(flavor_collection)
    assert util.json_are_equal(response, payload)
    
def json_error_from_model_parser_test():
    payload = util.load_json_from_file('exception_response.json')
    
    factory = ParserFactory()
    type_factory = factory.get_parser(util.JSON_MIMETYPE, FlavorSyncError)
    
    error = FlavorSyncError('Error message')
    
    response = type_factory.from_model(error)
    assert util.json_are_equal(response, payload)




def _create_parser_factory_test(mimetype, needed_class, expected_factory):
    type_factory = _create_factory(mimetype, needed_class)
    assert type(type_factory) is expected_factory

def _create_factory(mimetype, needed_class):
    factory = ParserFactory()
    return factory.get_parser(mimetype, needed_class)

def _check_infrastructure_dict_contents(dictionary):
    expected_infrastructure = util.create_example_infrastructure()
    
    assert expected_infrastructure.name in dictionary['name']
    assert expected_infrastructure.keystone_url in dictionary['keystone_url']
    assert expected_infrastructure.username in dictionary['username']
    assert expected_infrastructure.password in dictionary['password']
    assert expected_infrastructure.tenant in dictionary['tenant']

def _check_flavor_dict_contents(dictionary):
    expected_flavor = util.create_example_flavor()
    
    assert expected_flavor.name in dictionary['name']
    assert expected_flavor.vcpus == dictionary['vcpus']
    assert expected_flavor.ram == dictionary['ram']
    assert expected_flavor.disk == dictionary['disk']
    assert expected_flavor.swap == dictionary['swap']