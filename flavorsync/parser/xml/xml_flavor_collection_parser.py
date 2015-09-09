from lxml import etree
from lxml import objectify

from flavorsync.parser.xml.xml_parser import XMLParser
from flavorsync.parser.xml.xml_flavor_parser import XMLFlavorParser

class XMLFlavorCollectionParser(XMLParser):
	def __init__(self):
		print ("XML flavor collection parser initialized")
	
	def from_model(self, flavor_collection):
		self._create_xml_root_element()
		self._insert_flavor_collection_xml_data(flavor_collection)
		self._remove_xml_namespaces()
		
		return etree.tostring(self.xml)
	
	def _create_xml_root_element(self):
		maker = objectify.ElementMaker()
		self.xml = maker.flavors()
	
	def _insert_flavor_collection_xml_data(self, flavor_collection):
		xml_flavors = []
		flavor_parser = XMLFlavorParser()
		for flavor in flavor_collection.flavors:
			flavor_parser.from_model(flavor)
			xml_flavors.append(flavor_parser.xml)
		
		self.xml.flavor = xml_flavors