import flavorsync.test.util as util

from flavorsync.validator import factory_selector
from flavorsync.validator.concrete_factories.xml_validator_factory import XMLValidatorFactory
from flavorsync.validator.concrete_factories.json_validator_factory import JSONValidatorFactory
from flavorsync.validator.validator_factory import ValidatorFactory
from flavorsync.validator.concrete_validators.xml_validator import XMLValidator
from flavorsync.validator.concrete_validators.json_validator import JSONValidator
from flavorsync.exceptions import UnsupportedMediaTypeError

from lxml.etree import XMLSyntaxError 
from jsonschema.exceptions import ValidationError

def create_xml_validator_factory_test():
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    assert type(factory) is XMLValidatorFactory

def create_json_validator_factory_test():
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    assert type(factory) is JSONValidatorFactory

def create_wrong_mimetype_validator_factory_test():
    factory = factory_selector.get_factory(util.WRONG_MIMETYPE)
    assert type(factory) is ValidatorFactory




def create_xml_ivalidator_test():
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    
    validator = factory.create_flavor_collection_validator()
    assert type(validator) is XMLValidator
    
    validator = factory.create_flavor_modification_request_validator()
    assert type(validator) is XMLValidator
    
    validator = factory.create_flavor_request_validator()
    assert type(validator) is XMLValidator
    
    validator = factory.create_flavor_validator()
    assert type(validator) is XMLValidator
    
    validator = factory.create_infrastructure_request_validator()
    assert type(validator) is XMLValidator
    
    validator = factory.create_infrastructure_validator()
    assert type(validator) is XMLValidator

def create_json_ivalidator_test():
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    
    validator = factory.create_flavor_collection_validator()
    assert type(validator) is JSONValidator
    
    validator = factory.create_flavor_modification_request_validator()
    assert type(validator) is JSONValidator
    
    validator = factory.create_flavor_request_validator()
    assert type(validator) is JSONValidator
    
    validator = factory.create_flavor_validator()
    assert type(validator) is JSONValidator
    
    validator = factory.create_infrastructure_request_validator()
    assert type(validator) is JSONValidator
    
    validator = factory.create_infrastructure_validator()
    assert type(validator) is JSONValidator

def create_wrong_mimetype_ivalidator_test():
    factory = factory_selector.get_factory(util.WRONG_MIMETYPE)
    
    try:
        factory.create_flavor_collection_validator()
        assert False
    except UnsupportedMediaTypeError as e:
        assert True
    
    try:
        factory.create_flavor_modification_request_validator()
        assert False
    except UnsupportedMediaTypeError as e:
        assert True
    
    try:
        factory.create_flavor_request_validator()
        assert False
    except UnsupportedMediaTypeError as e:
        assert True
    
    try:
        factory.create_flavor_validator()
        assert False
    except UnsupportedMediaTypeError as e:
        assert True
    
    try:
        factory.create_infrastructure_request_validator()
        assert False
    except UnsupportedMediaTypeError as e:
        assert True
    
    try:
        factory.create_infrastructure_validator()
        assert False
    except UnsupportedMediaTypeError as e:
        assert True





def validate_xml_exception_payload(self):
    payload = util.load_xml_example_as_string('exception_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_exception_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_xml_flavor_collection_payload(self):
    payload = util.load_xml_example_as_string('flavor_collection_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_flavor_collection_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_empty_xml_flavor_collection_payload(self):
    payload =  '<?xml version="1.0" encoding="UTF-8"?>'
    payload += '<flavors/>'
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_flavor_collection_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_xml_flavor_creation_payload(self):
    payload = util.load_xml_example_as_string('flavor_creation_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_flavor_request_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)
    
def validate_xml_flavor_installation_payload(self):
    payload = util.load_xml_example_as_string('flavor_installation_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_flavor_modification_request_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_xml_flavor_promotion_payload(self):
    payload = util.load_xml_example_as_string('flavor_promotion_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_flavor_modification_request_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_xml_flavor_publication_payload(self):
    payload = util.load_xml_example_as_string('flavor_publication_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_flavor_modification_request_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_xml_flavor_payload(self):
    payload = util.load_xml_example_as_string('flavor_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_flavor_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_xml_infrastructure_request_payload(self):
    payload = util.load_xml_example_as_string('infrastructure_request.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_infrastructure_request_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)

def validate_xml_infrastructure_payload(self):
    payload = util.load_xml_example_as_string('infrastructure_response.xml')
    payload = util.remove_xml_header(payload)
    payload = util.remove_non_usable_characters(payload)
    factory = factory_selector.get_factory(util.XML_MIMETYPE)
    validator = factory.create_infrastructure_validator()
    
    _validate_payload(payload, validator, XMLSyntaxError)




def validate_json_exception_payload(self):
    payload = util.load_json_example_as_string('exception_response.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_exception_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_json_flavor_collection_payload(self):
    payload = util.load_json_example_as_string('flavor_collection_response.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_flavor_collection_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_empty_json_flavor_collection_payload(self):
    payload = '{"flavors":[]}'
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_flavor_collection_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_json_flavor_creation_payload(self):
    payload = util.load_json_example_as_string('flavor_creation_request.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_flavor_request_validator()
    
    _validate_payload(payload, validator, ValidationError)
    
def validate_json_flavor_installation_payload(self):
    payload = util.load_json_example_as_string('flavor_installation_request.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_flavor_modification_request_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_json_flavor_promotion_payload(self):
    payload = util.load_json_example_as_string('flavor_promotion_request.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_flavor_modification_request_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_json_flavor_publication_payload(self):
    payload = util.load_json_example_as_string('flavor_publication_request.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_flavor_modification_request_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_json_flavor_payload(self):
    payload = util.load_json_example_as_string('flavor_response.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_flavor_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_json_infrastructure_request_payload(self):
    payload = util.load_json_example_as_string('infrastructure_request.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_infrastructure_request_validator()
    
    _validate_payload(payload, validator, ValidationError)

def validate_json_infrastructure_payload(self):
    payload = util.load_json_example_as_string('infrastructure_response.json')
    factory = factory_selector.get_factory(util.JSON_MIMETYPE)
    validator = factory.create_infrastructure_validator()
    
    _validate_payload(payload, validator, ValidationError)

def _validate_payload(payload, validator, error):
    try:
        validator.validate(payload)
        assert True
    except ValidationError:
        assert False