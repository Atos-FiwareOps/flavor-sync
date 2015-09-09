from flavorsync.parser.xml.xml_infrastructure_parser import XMLInfrastructureParser
from flavorsync.parser.xml.xml_flavor_parser import XMLFlavorParser
from flavorsync.parser.parser import Parser
from flavorsync.parser.xml.xml_flavor_collection_parser import XMLFlavorCollectionParser
from flavorsync.parser.xml.xml_exception_parser import XMLExceptionParser

class XMLParserFactory():
	def get_parser(self, type_):
		if type_.__name__ in 'Infrastructure':
			return XMLInfrastructureParser()
		elif type_.__name__ in 'Flavor':
			return XMLFlavorParser()
		elif type_.__name__ in 'FlavorCollection':
			return XMLFlavorCollectionParser()
		elif type_.__name__ in 'FlavorSyncError':
			return XMLExceptionParser()
		else:
			return Parser()