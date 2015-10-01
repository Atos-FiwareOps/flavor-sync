from flavorsync.database import db
from flavorsync.parser.parser_factory import ParserFactory
import re
from flavorsync.exceptions import FlavorInfrastructureNotFoundError

class ParseableModel():
    @classmethod
    def deserialize(cls, mimetype, data):
        parser_factory = ParserFactory()
        parser = parser_factory.get_parser(mimetype, cls)
        return parser.to_dict(data)
    
    def serialize(self, mimetype):
        parser_factory = ParserFactory()
        parser = parser_factory.get_parser(mimetype, self.__class__)
        return parser.from_model(self)

# DB classes
class Infrastructure(db.Model, ParseableModel):
    __tablename__ = 'infrastructure'
    
    name = db.Column(db.String(30), primary_key = True)
    nova_url = db.Column(db.String(30))
    keystone_url = db.Column(db.String(30))
    username = db.Column(db.String(20))
    password = db.Column(db.String(30))
    tenant = db.Column(db.String(20))
    
    def __init__(self, name="", nova_url="", keystone_url="",
                username="", password="", tenant=""):
        self.name = name
        self.nova_url = nova_url
        self.keystone_url = keystone_url
        self.username = username
        self.password = password
        self.tenant = tenant
        
    def __repr__(self):
        return '<Infrastructure %r>' % self.name
    
    @classmethod
    def deserialize(cls, mimetype, data):
        infrastructure_dict = super(Infrastructure, cls).deserialize(mimetype, data)
        return Infrastructure(
                            infrastructure_dict['name'],
                            infrastructure_dict['nova_url'], 
                            infrastructure_dict['keystone_url'],
                            infrastructure_dict['username'], 
                            infrastructure_dict['password'],
                            infrastructure_dict['tenant'])
    
    def serialize(self, mimetype):
        return ParseableModel.serialize(self, mimetype)
    
    def _to_content_dict(self):
        return self.name
    
    def to_dict(self):
        return {"infrastructure": {"name" : self.name}}
    

class Flavor(db.Model, ParseableModel):
    __tablename__ = 'flavor'
    
    id = db.Column(db.String(36), primary_key = True)
    name = db.Column(db.String(30), unique =True)
    vcpus = db.Column(db.Integer)
    ram = db.Column(db.Integer)
    disk = db.Column(db.Integer)
    swap = db.Column(db.Integer)
    public = db.Column(db.Boolean)
    promoted = db.Column(db.Boolean)
    nodes = db.relationship(
        'Infrastructure',
        secondary = 'flavor_infrastructure_link'
    )
    
    def __init__(self, flavor_id=None, name=None, vcpus=-1, ram=-1,disk=-1, 
                swap=0, promoted=False, public=False, nodes=[]):
        self.id = flavor_id
        self.name = name
        self.vcpus = vcpus
        self.ram = ram
        self.disk = disk
        self.swap = swap
        self.promoted = promoted
        self.public = public
        self.nodes=nodes
        
    def __repr__(self):
        return '<Flavor %r>' % self.name
    
    @classmethod
    def deserialize(cls, mimetype, data):
        flavor_dict = super(Flavor, cls).deserialize(mimetype, data)
        
        nodes = []
        if 'nodes' in flavor_dict.keys():
            for node_name in flavor_dict.get('nodes'):
                try:
                    node = Infrastructure.query.get(node_name)
                except:
                    raise FlavorInfrastructureNotFoundError(node_name)
                nodes.append(node)
        
        return Flavor(
                    flavor_dict.get('id'), flavor_dict.get('name'),
                    flavor_dict.get('vcpus'), flavor_dict.get('ram'),
                    flavor_dict.get('disk'), flavor_dict.get('swap'),
                    flavor_dict.get('promoted'), flavor_dict.get('public'),
                    nodes)
    
    @classmethod
    def from_openstack_flavor(cls, flavor, infrastructure):
        number_regex = "[0-9]+"
        if type(flavor.swap) is str and re.match(number_regex, flavor.swap):
            swap = int(flavor.swap)
        else:
            swap = 0
        
        return (Flavor(
                    flavor.id, flavor.name, flavor.vcpus, flavor.ram,
                    flavor.disk, swap, False, False, [infrastructure]
                    )
                ) 
    
    def serialize(self, mimetype):
        return ParseableModel.serialize(self, mimetype)
    
    def _to_content_dict(self):
        nodes_dict = []
        for node in self.nodes:
            nodes_dict.append(node._to_content_dict())
        
        return {
                   "id" : self.id,
                   "name" : self.name,
                   "vcpus": self.vcpus,
                   "ram" : self.ram,
                   "disk" : self.disk,
                   "swap" : self.swap,
                   "public": self.public,
                   "promoted" : self.promoted,
                   "nodes" : nodes_dict
               }
    
    def to_dict(self):
        return {"flavor" : self._to_content_dict()}
    
class FlavorInfrastructureLink(db.Model):
    __tablename__ = 'flavor_infrastructure_link'
    
    flavor_id = db.Column(db.String(36), db.ForeignKey('flavor.id'), primary_key = True)
    infrastructure_name = db.Column(db.String(30), db.ForeignKey('infrastructure.name'), primary_key = True)

class FlavorCollection(ParseableModel):
    def __init__(self, flavors):
        self.flavors = flavors
    
    @classmethod
    def from_openstack_flavor_list(cls, flavor_list, infrastructure):
        flavors = []
        for flavor in flavor_list:
            flavors.append(Flavor.from_openstack_flavor(flavor, infrastructure))
            
        return FlavorCollection(flavors)
    
    def serialize(self, mimetype):
        return ParseableModel.serialize(self, mimetype)
    
    def extend(self, flavor_collection):
        self.flavors.extend(flavor_collection.flavors)
    
    def to_dict(self):
        flavors = []
        for flavor in self.flavors:
            flavor_dict = flavor._to_content_dict()
            flavors.append(flavor_dict)
        
        return {"flavors" : flavors}