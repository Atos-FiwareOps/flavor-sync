from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client

from uuid import uuid4
from flavorsync.exceptions import FlavorAlreadyExistsError,\
    OpenStackConnectionError, FlavorNotFoundExceptionError
from keystoneclient.openstack.common.apiclient.exceptions import ConnectionRefused
from novaclient.exceptions import Conflict, NotFound

class OpenStackManager():
    def __init__(self, infrastructure):
        self.infrastructure = infrastructure
    
    def get_flavors(self):
        nova_client = self._create_nova_client()
        flavors = self._create_detailed_flavor_list(nova_client)
        return flavors
    
    def create_flavor(self, flavor):
        flavor_id = uuid4()
        nova_client = self._create_nova_client()
        
        try:
            created_flavor = nova_client.flavors.create(
                                        flavorid=flavor_id, name=flavor.name,
                                        ram=flavor.ram, vcpus=flavor.vcpus,
                                        disk=flavor.disk, swap=flavor.swap
                                        )
        except ConnectionRefused:
            raise OpenStackConnectionError()
        except Conflict:
            raise FlavorAlreadyExistsError(flavor.name)
            
        return created_flavor
    
    def get_flavor(self, flavor_id):
        nova_client = self._create_nova_client()
        
        try:
            flavor = nova_client.flavors.get(flavor_id)
        except ConnectionRefused:
            raise OpenStackConnectionError()
        except NotFound:
            raise FlavorNotFoundExceptionError(flavor_id)
        
        return flavor
    
    def delete_flavor(self, flavor_id):
        nova_client = self._create_nova_client()
        
        try:
            nova_client.flavors.delete(flavor_id)
        except ConnectionRefused:
            raise OpenStackConnectionError()
    
    def _create_nova_client(self):
        nova_api_version = 2
        keystone_url = self.infrastructure.keystone_url + '/v3/'
        a = v3.Password(
                    auth_url=keystone_url,
                    username=self.infrastructure.username,
                    password=self.infrastructure.password,
                    user_domain_name="default",
                    project_name=self.infrastructure.tenant,
                    project_domain_name='default')
        sess = session.Session(auth=a)
        
        try:
            nova_client = client.Client(nova_api_version, session=sess)
        except:
            raise OpenStackConnectionError()
            
        return nova_client
    
    def _create_detailed_flavor_list(self, nova_client):
        flavors = []
        
        try:
            for flavor in nova_client.flavors.list():
                flavors.append(nova_client.flavors.get(flavor))
        except ConnectionRefused:
            raise OpenStackConnectionError()
            
        return flavors