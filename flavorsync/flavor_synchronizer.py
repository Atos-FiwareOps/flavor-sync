from flavorsync.openstack.openstack_manager import OpenStackManager
from flavorsync.database_manager import DatabaseManager
from flavorsync.model import FlavorCollection, Flavor
from flavorsync.exceptions import FlavorNotFoundExceptionError,\
	PromotedNotPublicFlavorBadRequestError, UnpublishUnpromotedFlavorError

#TODO: is it really necessary to keep track of public and private attributes
#      in the database?

class FlavorSynchronizer():
	def __init__(self):
		self.database_manager = DatabaseManager()
	
	def register_infrastructure(self, infrastructure):
		self.database_manager.register_infrastructure(infrastructure)

	def unregister_infrastructure(self, infrastructure_name):
		self.database_manager.unregister_infrastructure(infrastructure_name)
	
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
	
	def publish_or_promote_flavor(self, flavor_id, flavor):
		self._check_well_formed_publishing_conditions(flavor)
		
		f = self.get_flavor(flavor_id)
		
		self._check_publishing_conditions(f, flavor)
		self._publish_or_promote_flavor(f, flavor)
		
		return f
	
	def add_flavor_to_infrastructure(self, id_, flavor):
		#TODO check permissions
		f = self.get_flavor(id_)
		
		self._create_private_flavor(f)
		self.database_manager.add_flavor_to_infrastructure(f, flavor.nodes)
		
		return f
		
	
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
	
	def _get_private_flavor(self, id_):
		infrastructure = self.database_manager.get_infrastructure('Mordor')
		openstack_manager = OpenStackManager(infrastructure)
		openstack_flavor = openstack_manager.get_flavor(id_)
		return Flavor.from_openstack_flavor(openstack_flavor, infrastructure)
		
	def _get_public_flavor(self, id_):
		return self.database_manager.get_flavor(id_)
	
	def _delete_private_flavor(self, id_):
		infrastructure = self.database_manager.get_infrastructure('Mordor')
		openstack_manager = OpenStackManager(infrastructure)
		openstack_manager.delete_flavor(id_)
	
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
	
	def _publish_or_promote_flavor(self, flavor, new_conditions):
		if new_conditions.public:
			flavor.public = new_conditions.public
			if new_conditions.promoted is not None:
				flavor.promoted = new_conditions.promoted
			flavor = self._publish_flavor(flavor)
		elif new_conditions.promoted:
			flavor = self.database_manager.promote_flavor(flavor)
		
		return flavor
	
	def _is_openstack_flavor(self, flavor):
		return flavor is None
	
	def _remove_duplicated_flavors(self, public_flavors, private_flavors):
		for public_flavor in public_flavors:
			for private_flavor in private_flavors.flavors:
				if private_flavor.id in public_flavor.id:
					private_flavors.flavors.remove(private_flavor)
	