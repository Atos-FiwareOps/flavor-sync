from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client

from uuid import uuid4
from flavorsync.exceptions import FlavorAlreadyExistsError,\
    OpenStackConnectionError, FlavorNotFoundExceptionError, OpenStackEndPointNotFound, OpenStackUnauthorizedError,\
    OpenStackForbidden
from keystoneclient.openstack.common.apiclient.exceptions import ConnectionRefused, Unauthorized, EndpointNotFound
from novaclient.exceptions import Conflict, NotFound, Forbidden
from flavorsync import config


class OpenStackManager():
    _prelogString = "OpenStackManager()--"
    def __init__(self, infrastructure, token):
        self.infrastructure = infrastructure
        self.token = token
    
    def get_flavors(self):
        print (self._prelogString + "get_flavors(): started the get flavors")
        nova_client = self._create_nova_client()
        print (self._prelogString + "get_flavors(): created the nova client")
        try:

            flavors = self._create_detailed_flavor_list(nova_client)
            print (self._prelogString + "get_flavors(): get the flavors for the region "+ self.infrastructure)
            print (flavors)
        except Unauthorized:
            print (self._prelogString + "get_flavors(): Unauthorized OpenStack error for "+ self.infrastructure)
            raise OpenStackUnauthorizedError()
        except EndpointNotFound:
            print (self._prelogString + "get_flavors(): publicURL endpoint for compute service in "+ self.infrastructure +" region not found")
            raise OpenStackEndPointNotFound(self.infrastructure)

        return flavors
    
    def create_flavor(self, flavor):
        try:
            flavor_id = flavor.id
        except AttributeError:
            flavor_id = uuid4()
        nova_client = self._create_nova_client()
        
        try:
            created_flavor = nova_client.flavors.create(
                                        flavorid=flavor_id, name=flavor.name,
                                        ram=flavor.ram, vcpus=flavor.vcpus,
                                        disk=flavor.disk, swap=flavor.swap
                                        )
            print (self._prelogString + "create_flavor: created the flavor")
        except ConnectionRefused:
            raise OpenStackConnectionError()
        except Conflict:
            raise FlavorAlreadyExistsError(flavor.name)
        except Forbidden:
            print (self._prelogString + "create_flavor(): error creating Flavors in a region. Your credentials don’t give you access to this resource.")
            raise OpenStackForbidden(self.infrastructure)
        except Unauthorized:
            print (self._prelogString + "create_flavor(): Unauthorized OpenStack error for "+ self.infrastructure)
            raise OpenStackUnauthorizedError()
        except EndpointNotFound:
            print (self._prelogString + "create_flavor(): publicURL endpoint for compute service in "+ self.infrastructure +" region not found")
            raise OpenStackEndPointNotFound(self.infrastructure)
            
        return created_flavor
    
    def get_flavor(self, flavor_id):
        nova_client = self._create_nova_client()
        
        try:
            flavor = nova_client.flavors.get(flavor_id)
        except ConnectionRefused:
            raise OpenStackConnectionError()
        except NotFound:
            raise FlavorNotFoundExceptionError(flavor_id)
        except Unauthorized:
            print (self._prelogString + "get_flavor(): Unauthorized OpenStack error for "+ self.infrastructure)
            raise OpenStackUnauthorizedError()
        except EndpointNotFound:
            print (self._prelogString + "get_flavor(): publicURL endpoint for compute service in "+ self.infrastructure +" region not found")
            raise OpenStackEndPointNotFound(self.infrastructure)
        
        return flavor
    
    def delete_flavor(self, flavor_id):
        nova_client = self._create_nova_client()
        
        try:
            nova_client.flavors.delete(flavor_id)
            print (self._prelogString + "delete_flavor: deleted the flavor")
        except ConnectionRefused:
            raise OpenStackConnectionError()
        except NotFound:
            raise FlavorNotFoundExceptionError(flavor_id)
        except Forbidden:
            print (self._prelogString + "create_flavor(): error creating Flavors in a region. Your credentials don’t give you access to this resource.")
            raise OpenStackForbidden(self.infrastructure)
        except Unauthorized:
            print (self._prelogString + "create_flavor(): Unauthorized OpenStack error for "+ self.infrastructure)
            raise OpenStackUnauthorizedError()
        except EndpointNotFound:
            print (self._prelogString + "create_flavor(): publicURL endpoint for compute service in "+ self.infrastructure +" region not found")
            raise OpenStackEndPointNotFound(self.infrastructure)
    
    def _create_nova_client(self):

        print (self._prelogString + "_create_nova_client(): Start the creation of nova client")
        
        #if we have received the token, this indicates that we are into the federation of FIWARELab
        if self.token:
            print (self._prelogString + "_create_nova_client(): identification of active token " + self.token)
            #it is delegated to the centralized Keystone to identify the endpoints of the different nova services
            nova_api_version = 2
            keystone_url = config.url_keystone
            #keystone_url = 'http://cloud.lab.fiware.org:4730/v3/'
            a = v3.Token(
                            auth_url=keystone_url,
                            token = self.token)
            print ("after token")

            sess = session.Session(auth=a)
            print (self._prelogString + "_create_nova_client(): created the token in session")
                    
            try:
                print (self._prelogString + "_create_nova_client(): start the clien of nova for the region " + self.infrastructure)
                nova_client = client.Client(nova_api_version, session=sess, region_name=self.infrastructure)
                print (self._prelogString + "_create_nova_client(): Nova Clien created!!!!!")
                
            except:
                raise OpenStackConnectionError()
            return nova_client

        else:
            #we mantain the first version of the component to cover the compleate lifecycle
            #It is only integrated with login and password for local Openstack infratructure (Mordor),
            #, it should be modified to manage the federated nodes.
            print (self._prelogString + "_create_nova_client(): Started the old version to create the nova client!!!!")
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