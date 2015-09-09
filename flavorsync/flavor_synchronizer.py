from flavorsync.openstack.openstack_manager import OpenStackManager
from flavorsync.database_manager import DatabaseManager
from flavorsync.model import FlavorCollection, Flavor
from flavorsync.exceptions import FlavorNotFoundExceptionError,\
    PromotedNotPublicFlavorBadRequestError, UnpublishUnpromotedFlavorError

class FlavorSynchronizer():
    def __init__(self):
        self.database_manager = DatabaseManager()
    
    def register_infrastructure(self, infrastructure):
        self.database_manager.register_infrastructure(infrastructure)

    def unregister_infrastructure(self, name):
        self.database_manager.unregister_infrastructure(name)
    
    def get_flavors(self, public, promoted):
        flavors = self._get_public_flavors(public, promoted)
        flavor_collection = FlavorCollection(flavors)
        
        if not public and not promoted:
            private_flavors = self._get_private_flavors()
            self._remove_duplicated_flavors(flavors, private_flavors)
            flavor_collection.extend(private_flavors)
        
        return flavor_collection
    
    def create_flavor(self, flavor):
        f = self._create_private_flavor(flavor)
        return f
    
    def get_flavor(self, flavor_id):
        try:
            flavor = self._get_public_flavor(flavor_id)
        except FlavorNotFoundExceptionError:
            flavor = self._get_private_flavor(flavor_id)
        
        return flavor
    
    def publish_or_promote_flavor(self, flavor_id, modified_flavor):
        self._check_well_formed_publishing_conditions(modified_flavor)
        
        current_flavor = self.get_flavor(flavor_id)
        
        self._check_publishing_conditions(current_flavor, modified_flavor)
        self._publish_or_promote_flavor(current_flavor, modified_flavor)
        
        return current_flavor
    
    def add_node_to_flavor(self, flavor_id, modified_flavor):
        current_flavor = self.get_flavor(flavor_id)
        
        self._create_private_flavor(current_flavor)
        self.database_manager.add_node_to_flavor(current_flavor,
                                                modified_flavor.nodes)
        
        return current_flavor
        
    
    def delete_flavor(self, flavor_id):
        flavor = self.get_flavor(flavor_id)
        self._delete_private_flavor(flavor.id)
        
        if flavor.public:
            self._delete_node_in_flavor(flavor)
    
    def _get_public_flavors(self, public, promoted):
        return self.database_manager.get_flavors(public, promoted)
        
    def _get_private_flavors(self):
        infrastructure = self.database_manager.get_infrastructure('Mordor')
        openstack_manager = OpenStackManager(infrastructure)
        openstack_flavors = openstack_manager.get_flavors()
        return FlavorCollection.from_openstack_flavor_list(openstack_flavors, infrastructure)
    
    def _create_private_flavor(self, flavor):
        infrastructure = self.database_manager.get_infrastructure('Mordor')
        openstack_manager = OpenStackManager(infrastructure)
        created_flavor = openstack_manager.create_flavor(flavor)
        return Flavor.from_openstack_flavor(created_flavor, infrastructure)
    
    def _publish_flavor(self, flavor):
        f = self.database_manager.create_flavor(flavor)
        return f
    
    def _get_private_flavor(self, flavor_id):
        infrastructure = self.database_manager.get_infrastructure('Mordor')
        openstack_manager = OpenStackManager(infrastructure)
        openstack_flavor = openstack_manager.get_flavor(flavor_id)
        return Flavor.from_openstack_flavor(openstack_flavor, infrastructure)
        
    def _get_public_flavor(self, flavor_id):
        return self.database_manager.get_flavor(flavor_id)
    
    def _delete_private_flavor(self, flavor_id):
        infrastructure = self.database_manager.get_infrastructure('Mordor')
        openstack_manager = OpenStackManager(infrastructure)
        openstack_manager.delete_flavor(flavor_id)
    
    def _delete_node_in_flavor(self, flavor):
        infrastructure = self.database_manager.get_infrastructure('Mordor')
        self.database_manager.delete_node_in_flavor(flavor, infrastructure)
    
    def _check_well_formed_publishing_conditions(self, flavor):
        if flavor.promoted and flavor.public is not None and not flavor.public:
            raise PromotedNotPublicFlavorBadRequestError()
    
    def _check_publishing_conditions(self, current_flavor, modified_flavor):
        if (modified_flavor.public is not None 
                and current_flavor.public
                and not modified_flavor.public
            or current_flavor.promoted and not modified_flavor.promoted):
            raise UnpublishUnpromotedFlavorError()
    
    def _publish_or_promote_flavor(self, current_flavor, modified_flavor):
        if modified_flavor.public:
            current_flavor.public = modified_flavor.public
            if modified_flavor.promoted is not None:
                current_flavor.promoted = modified_flavor.promoted
            current_flavor = self._publish_flavor(current_flavor)
        elif modified_flavor.promoted:
            current_flavor = self.database_manager.promote_flavor(current_flavor)
        
        return current_flavor
    
    def _is_openstack_flavor(self, flavor):
        return flavor is None
    
    def _remove_duplicated_flavors(self, public_flavors, private_flavors):
        for public_flavor in public_flavors:
            for private_flavor in private_flavors.flavors:
                if private_flavor.id in public_flavor.id:
                    private_flavors.flavors.remove(private_flavor)