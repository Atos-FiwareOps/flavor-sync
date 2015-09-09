from lxml import etree
from lxml import objectify

from flavorsync.parser.xml.xml_parser import XMLParser

class XMLInfrastructureParser(XMLParser):
    def __init__(self):
        print ("XML node parser initialized")
    
    def to_dict(self, xml_data):
        obj = objectify.fromstring(xml_data)
        
        self.dict = {
                "name" : str(obj.name),
                "nova_url": str(obj.nova_url),
                "keystone_url" : str(obj.keystone_url),
                "username" : str(obj.username),
                "password" : str(obj.password),
                "tenant" : str(obj.tenant)
            }
        
        return self.dict
    
    def from_model(self, infrastructure):
        self._create_xml_root_element()
        self._insert_infrastructure_xml_data(infrastructure)
        self._remove_xml_namespaces()
        
        return etree.tostring(self.xml)
    
    def _create_xml_root_element(self):
        maker = objectify.ElementMaker()
        self.xml = maker.infrastructure()
    
    def _insert_infrastructure_xml_data(self, infrastructure):
        self.xml.name = infrastructure.name