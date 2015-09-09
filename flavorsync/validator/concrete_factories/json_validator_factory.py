from flavorsync.validator.validator_factory import ValidatorFactory
from flavorsync.validator.concrete_validators.json_validator import JSONValidator
from flavorsync.exceptions import FlavorBadRequestError, InfrastructureBadRequestError

class JSONValidatorFactory(ValidatorFactory):
	def createFlavorCollectionValidator(self):
		return JSONValidator("flavorsync/validator/schema/json/flavor_collection.schema.json")
		
	def createFlavorModificationRequestValidator(self):
		exception = FlavorBadRequestError()
		return JSONValidator("flavorsync/validator/schema/json/flavor_modification_request.schema.json", exception)
	
	def createFlavorRequestValidator(self):
		exception = FlavorBadRequestError()
		return JSONValidator("flavorsync/validator/schema/json/flavor_request.schema.json", exception)
	
	def createFlavorValidator(self):
		return JSONValidator("flavorsync/validator/schema/json/flavor.schema.json")
	
	def createInfrastructureRequestValidator(self):
		exception = InfrastructureBadRequestError()
		return JSONValidator("flavorsync/validator/schema/json/infrastructure_request.schema.json", exception)
	
	def createInfrastructureValidator(self):
		return JSONValidator("flavorsync/validator/schema/json/infrastructure.schema.json")