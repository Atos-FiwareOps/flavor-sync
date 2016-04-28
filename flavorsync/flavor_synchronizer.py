from flavorsync.openstack.openstack_manager import OpenStackManager
from flavorsync.database_manager import DatabaseManager
from flavorsync.model import FlavorCollection, Flavor, InfrastructureCollection
from flavorsync.exceptions import FlavorNotFoundExceptionError,\
    PromotedNotPublicFlavorBadRequestError, UnpublishUnpromotedFlavorError
from uuid import uuid4
from flask import session



class FlavorSynchronizer():
    def __init__(self):
        self.database_manager = DatabaseManager()
    
    
    ##############
    #Management of the completed lifecycle of the flavors, including private, public and promoted flavors
    #That should be only possible if all the management is done using this API, if the different regions don't use it, 
    #it will be complicated to maintain the coherence.
    #Hence, this part is not finished and tested, since we have not centralized this management.
    #########

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
 
    def get_flavors_region(self, region):
        private_flavors = self._get_private_flavors()
      
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

    def is_node_included(self, region):
        return self._exist_node(region)

    def get_nodes(self):
        return self._get_nodes()

    #########
    #########


    ##############
    #Management of the promoted flavors, which are not related with the private flavors.
    #This part has been integrated with the DashFI.
    #########
    def get_public_flavor(self, flavor_id):
        try:
            flavor = self._get_public_flavor(flavor_id)
        except FlavorNotFoundExceptionError:
            flavor = None
        return flavor

    def create_promoted_flavor(self, flavor):
        #this method only manage the promoted flavors. Hence, it is responsible to force the promoted attribute.
        flavor.promoted = True
        flavor.public = True
        if not flavor.id:
            flavor.id = str(uuid4())
            print (flavor)
        print (flavor.id)
        f = self._publish_flavor(flavor)
        return f
    
    def delete_promoted_flavor(self, flavor_id):
        #If the promoted flavor has nodes associated an error raised, since it is not allowed to remove promote flavors with nodes.
        #If you only manage promoted flavors, it shouldn't happen, 
        #nevertheless if you are managing the complete life cycle, the flavor cannot be deleted if it has nodes associated.
        self.database_manager.delete_flavor(flavor_id)

    #########
    #########

    #########
    #Manage only the private flavors for the different regions.
    #This part has been integrated with the DashFI.
    #########
    def get_region_flavors(self, region):
        private_flavors = self._get_private_region_flavors(region)
        return private_flavors

    def get_region_flavor(self, region, flavor_id):
        try:
            flavor = self._get_private_region_flavor(region, flavor_id)
        except FlavorNotFoundExceptionError:
            flavor = None
        return flavor

    def create_region_flavor(self, region, flavor):
        f = self._create_private_region_flavor(region, flavor)
        return f


    def delete_region_flavor(self, region, flavor_id):
        self._delete_private_region_flavor(region, flavor_id)
        


    ########
    ########
    

    ########
    ##Common and private methods
    ########
    def _get_public_flavors(self, public, promoted):
        return self.database_manager.get_flavors(public, promoted)

    def _exist_node(self, region):
        infrastructure = self.database_manager.get_infrastructure(region)
        if infrastructure is None:
            return False
        else:
            return True

    def _get_nodes(self):
        infrastructures = self.database_manager.get_infrastructures()
        infrastructure_collection = InfrastructureCollection(infrastructures)
        return infrastructure_collection
        
    #with token of KeyStone
    def _get_private_region_flavors(self, region):
        token = session['token_keystone']
        infrastructure = self.database_manager.get_infrastructure(region)
        openstack_manager = OpenStackManager(region, token)
        openstack_flavors = openstack_manager.get_flavors()
        #TODO review how to manage the infrastructure to be aligned with the data base definition.
        return FlavorCollection.from_openstack_flavor_list(openstack_flavors, infrastructure)

    def _get_private_region_flavor(self, region, flavor_id):
        token = session['token_keystone']
        infrastructure = self.database_manager.get_infrastructure(region)
        openstack_manager = OpenStackManager(region, token)
        openstack_flavor = openstack_manager.get_flavor(flavor_id)
        return Flavor.from_openstack_flavor(openstack_flavor, infrastructure)

    def _create_private_region_flavor(self, region, flavor):
        token = session['token_keystone']
        infrastructure = self.database_manager.get_infrastructure(region)
        openstack_manager = OpenStackManager(region, token)
        created_flavor = openstack_manager.create_flavor(flavor)
        return Flavor.from_openstack_flavor(created_flavor, infrastructure)

    def _delete_private_region_flavor(self, region, flavor_id):
        token = session['token_keystone']
        infrastructure = self.database_manager.get_infrastructure(region)
        openstack_manager = OpenStackManager(region, token)
        openstack_manager.delete_flavor(flavor_id)

    #without Keystone token
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