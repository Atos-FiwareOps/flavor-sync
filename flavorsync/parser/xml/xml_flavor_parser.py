from lxml import etree
from lxml import objectify

from flavorsync.parser.xml.xml_parser import XMLParser

class XMLFlavorParser(XMLParser):
    def __init__(self):
        super(XMLFlavorParser, self).__init__()
        print ("XML node parser initialized")
    
    def to_dict(self, xml_data):
        obj = objectify.fromstring(xml_data)
        
        if 'name' in objectify.dump(obj):
            self.dict["name"] = str(obj.name)
            
        if 'vcpus' in objectify.dump(obj):
            self.dict["vcpus"] = int(obj.vcpus)
            
        if 'ram' in objectify.dump(obj):
            self.dict["ram"] = int(obj.ram)
            
        if 'disk' in objectify.dump(obj):
            self.dict["disk"] = int(obj.disk)
            
        if 'swap' in objectify.dump(obj):
            self.dict["swap"] = int(obj.swap)
            
        if 'public' in objectify.dump(obj):
            self.dict["public"] = bool(obj.public)
            
        if 'promoted' in objectify.dump(obj):
            self.dict["promoted"] = bool(obj.promoted)
        
        nodes = []
        if 'node' in objectify.dump(obj):
            for node in obj.node:
                nodes.append(str(node))
        self.dict["nodes"]=nodes
        
        return self.dict
    
    def from_model(self, flavor):
        self._create_xml_root_element()
        self._insert_flavor_xml_data(flavor)
        self._remove_xml_namespaces()
        
        return etree.tostring(self.xml)
    
    def _create_xml_root_element(self):
        maker = objectify.ElementMaker()
        self.xml = maker.flavor()
    
    def _insert_flavor_xml_data(self, flavor):
        self.xml.set('id', flavor.id)
        self.xml.name = flavor.name
        self.xml.vcpus = flavor.vcpus
        self.xml.ram = flavor.ram
        self.xml.disk = flavor.disk
        self.xml.swap = flavor.swap
        self.xml.promoted = flavor.promoted
        self.xml.public = flavor.public
        
        nodes = []
        for node in flavor.nodes:
            nodes.append(node.name)
            
        self.xml.node = nodes