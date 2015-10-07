from flavorsync.validator.validator_factory import ValidatorFactory
from flavorsync.validator.concrete_validators.json_validator import JSONValidator
from flavorsync.exceptions import FlavorBadRequestError, InfrastructureBadRequestError

class JSONValidatorFactory(ValidatorFactory):
    def create_exception_validator(self):
        return JSONValidator("flavorsync/validator/schema/json/exception_response.schema.json")
    
    def create_flavor_collection_validator(self):
        return JSONValidator("flavorsync/validator/schema/json/flavor_collection.schema.json")
        
    def create_flavor_modification_request_validator(self):
        exception = FlavorBadRequestError()
        return JSONValidator("flavorsync/validator/schema/json/flavor_modification_request.schema.json", exception)
    
    def create_flavor_request_validator(self):
        exception = FlavorBadRequestError()
        return JSONValidator("flavorsync/validator/schema/json/flavor_request.schema.json", exception)
    
    def create_flavor_validator(self):
        return JSONValidator("flavorsync/validator/schema/json/flavor.schema.json")
    
    def create_infrastructure_request_validator(self):
        exception = InfrastructureBadRequestError()
        return JSONValidator("flavorsync/validator/schema/json/infrastructure_request.schema.json", exception)
    
    def create_infrastructure_validator(self):
        return JSONValidator("flavorsync/validator/schema/json/infrastructure.schema.json")