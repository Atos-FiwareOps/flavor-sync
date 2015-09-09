from flavorsync.validator.validator_factory import ValidatorFactory
from flavorsync.validator.concrete_factories.json_validator_factory import JSONValidatorFactory
from flavorsync.validator.concrete_factories.xml_validator_factory import XMLValidatorFactory

def get_factory(mimetype):
	ValidatorFactory.mime = mimetype
	if 'application/json' in mimetype:
		concrete_factory = JSONValidatorFactory()
	elif 'application/xml' in mimetype:
		concrete_factory = XMLValidatorFactory()
	else:
		concrete_factory = ValidatorFactory(mimetype)
	
	return concrete_factory