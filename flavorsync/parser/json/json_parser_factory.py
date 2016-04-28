from flavorsync.parser.json.json_infrastructure_parser import JSONInfrastructureParser
from flavorsync.parser.json.json_flavor_parser import JSONFlavorParser
from flavorsync.parser.parser import Parser
from flavorsync.parser.json.json_flavor_collection_parser import JSONFlavorCollectionParser
from flavorsync.parser.json.json_infrastructure_collection_parser import JSONInfrastructureCollectionParser
from flavorsync.parser.json.json_exception_parser import JSONExceptionParser

class JSONParserFactory():
    def get_parser(self, type_):
        if type_.__name__ in 'Infrastructure':
            return JSONInfrastructureParser()
        elif type_.__name__ in 'InfrastructureCollection':
            return JSONInfrastructureCollectionParser()
        elif type_.__name__ in 'Flavor':
            return JSONFlavorParser()
        elif type_.__name__ in 'FlavorCollection':
            return JSONFlavorCollectionParser()
        elif type_.__name__ in 'FlavorSyncError':
            return JSONExceptionParser()
        else:
            return Parser()