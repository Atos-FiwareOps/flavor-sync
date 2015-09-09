from flavorsync.exceptions import FlavorBadRequestError, InfrastructureBadRequestError
from flavorsync.validator.validator_factory import ValidatorFactory
from flavorsync.validator.concrete_validators.xml_validator import XMLValidator

class XMLValidatorFactory(ValidatorFactory):
	def createFlavorCollectionValidator(self):
		return XMLValidator("flavorsync/validator/schema/xml/flavor_collection.xsd")
		
	def createFlavorModificationRequestValidator(self):
		exception = FlavorBadRequestError()
		return XMLValidator("flavorsync/validator/schema/xml/flavor_modification_request.xsd", exception)
	
	def createFlavorRequestValidator(self):
		exception = FlavorBadRequestError()
		return XMLValidator("flavorsync/validator/schema/xml/flavor_request.xsd", exception)
	
	def createFlavorValidator(self):
		return XMLValidator("flavorsync/validator/schema/xml/flavor.xsd")
	
	def createInfrastructureRequestValidator(self):
		exception = InfrastructureBadRequestError()
		return XMLValidator("flavorsync/validator/schema/xml/infrastructure_request.xsd", exception)
	
	def createInfrastructureValidator(self):
		return XMLValidator("flavorsync/validator/schema/xml/infrastructure.xsd")