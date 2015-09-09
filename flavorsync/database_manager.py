from flavorsync.database import db
from flavorsync.model import Flavor, Infrastructure
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from flavorsync.exceptions import InfrastructureAlreadyExistsError,\
	InfrastructureNotFoundError, FlavorAlreadyExistsError,\
	FlavorNotFoundExceptionError
from sqlalchemy.orm.exc import UnmappedInstanceError

class DatabaseManager():
	def get_infrastructure(self, name):
		return Infrastructure.query.get(name)
	
	def register_infrastructure(self, infrastructure):
		db.session.add(infrastructure)
		
		try:
			db.session.commit()
		except IntegrityError:
			raise InfrastructureAlreadyExistsError(infrastructure.name)

	def unregister_infrastructure(self, name):
		infrastructure = Infrastructure.query.get(name)
		
		try:
			db.session.delete(infrastructure)
			db.session.commit()
		except UnmappedInstanceError:
			raise InfrastructureNotFoundError(name)
	
	def get_flavors(self, public_, promoted_):
		if not public_ and not promoted_:
			flavors = Flavor.query.all()
		elif public_ and promoted_:
			flavors = Flavor.query.filter_by(public=public_, promoted=promoted_).all()
		elif public_:
			flavors = Flavor.query.filter_by(public=public_).all()
		elif promoted_:
			flavors = Flavor.query.filter_by(promoted=promoted_).all()
		return flavors
	
	def create_flavor(self, flavor):
		db.session.add(flavor)
		
		try:
			db.session.commit()
		except InvalidRequestError:
			raise FlavorAlreadyExistsError(flavor.name)
	
	def get_flavor(self, flavor_id):
		flavor = Flavor.query.get(flavor_id)
		if flavor is None:
			raise FlavorNotFoundExceptionError(flavor_id)
		return flavor
	
	def promote_flavor(self, flavor):
		flavor.promoted = True
		db.session.commit()
	
	def add_flavor_to_infrastructure(self, flavor, node):
		flavor.nodes.extend(node)
		db.session.commit()
	
	def delete_flavor(self, flavor_id):
		flavor = Flavor.query.get(flavor_id)
		db.session.delete(flavor)
		
		try:
			db.session.commit()
		except InvalidRequestError:
			raise FlavorNotFoundExceptionError(flavor_id)
	
	def delete_node_in_flavor(self, flavor, infrastructure):
		flavor.nodes.remove(infrastructure)
		
		try:
			db.session.commit()
		except InvalidRequestError:
			raise FlavorNotFoundExceptionError(flavor.id)