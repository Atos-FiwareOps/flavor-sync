from flavorsync.exceptions import FlavorBadRequestError, InfrastructureBadRequestError
from flavorsync.validator.validator_factory import ValidatorFactory
from flavorsync.validator.concrete_validators.xml_validator import XMLValidator

class XMLValidatorFactory(ValidatorFactory):
    def create_exception_validator(self):
        return XMLValidator("flavorsync/validator/schema/xml/exception_response.xsd")
    
    def create_flavor_collection_validator(self):
        return XMLValidator("flavorsync/validator/schema/xml/flavor_collection.xsd")
        
    def create_flavor_modification_request_validator(self):
        exception = FlavorBadRequestError()
        return XMLValidator("flavorsync/validator/schema/xml/flavor_modification_request.xsd", exception)
    
    def create_flavor_request_validator(self):
        exception = FlavorBadRequestError()
        return XMLValidator("flavorsync/validator/schema/xml/flavor_request.xsd", exception)
    
    def create_flavor_validator(self):
        return XMLValidator("flavorsync/validator/schema/xml/flavor.xsd")
    
    def create_infrastructure_request_validator(self):
        exception = InfrastructureBadRequestError()
        return XMLValidator("flavorsync/validator/schema/xml/infrastructure_request.xsd", exception)
    
    def create_infrastructure_validator(self):
        return XMLValidator("flavorsync/validator/schema/xml/infrastructure.xsd")