import requests
import flavorsync.test.util as util
import re

from functools import wraps

from flavorsync import app

from flask import request
from flask import json, session

from flavorsync.model import Flavor, Infrastructure
from flavorsync.database import db
from flavorsync.flavor_synchronizer import FlavorSynchronizer
from werkzeug.wrappers import Response
from flavorsync.validator import factory_selector

from flavorsync.exceptions import UnAuthorizedMethodError
from flavorsync import config




# set the secret key.  keep this really secret:
#To generate the new secret Key use this:
#>>> import os
#>>> os.urandom(24)
app.secret_key = '\xbb"}k{y\x89NN\x15\xd9\xe7\x8b\x07\xf2\x88U\xd3\xfd,\x99\'\xe7u'

#authentication and authorization part
def check_auth(token, token_keystone):
    """TODO it is only to test the call of OpenStack. We need to change this validation for the IdM and delegate to the call of Openstack the token validation.
    """
    chech_auth = False
    url_keyrock = config.url_keyrock + token
    responseToken = requests.get(url_keyrock)
    if (responseToken.status_code == 200):
        try:
            user = json.loads(responseToken.content)
            session['user'] = user
            _token_keystone = ""
            if token_keystone:
                _token_keystone = token_keystone
            session['token_keystone'] = _token_keystone
            chech_auth = True
        except Exception as err:
            print ("check_auth(): Error - " + str(err))
            chech_auth = False
    else:
        chech_auth = False
    return chech_auth

def authenticate():
    """Sends a 401 response that enables Auth2 authentication"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper token', 401,
    {'X-Auth-Token': 'Auth2 realm="Token Required"'})

def authorization():
    """Sends a 401 response that enables Auth2 authentication"""
    print ("authorization!!!!!!")
    return Response(
    'The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.\n', 405 )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Auth-Token')
        token_keystone = request.headers.get('X-Auth-Token-KeyStone')
        print ("token_keystone" + str(token_keystone))
        if not token or not check_auth(token, token_keystone):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def exists_node_calendar(node):
    listNodes = ast.literal_eval(config.node_list)
    if any(d.get('id', None) == node for d in listNodes):
        return True
    else:
        return False

def authorization():
    ##This method is reponsible to manage the authorization for the flavors
    ##This method validate if the user has the apropiate rol for manage promoted flavors 
    is_authorized = False
    try:
        
        user = session['user']
        print (user)
        #validate if the user has privileges to manage the promoted flavors
        roles = user['roles']
        for role in roles:
            role_name =  role['name']
            if role_name=='InfrastructureManager':
                is_authorized = True
                break
    except Exception as err:
            #any error indicate that the structure is not correct and we don't allow to connect for this user.
            is_authorized = False
            print ('Error authorization for user !!!' )
            print (err)
    if not is_authorized:
        raise UnAuthorizedMethodError()
        

#definition of the different views
@app.errorhandler(404)
def not_found(error):
    return "The requested resource does not exist", 404

@app.errorhandler(UnAuthorizedMethodError)
def not_authorized(error):
    return "The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.", 405



@app.after_request
def shutdown_session(response):
    db.session.remove()
    return response

@app.route("/api/v1")
@requires_auth
def root():
    return "Hello world"

#Definition of the compleate management of the flavors
@app.route("/v1/infrastructures", methods=['POST'])
def register_infrastructure():
    body = util.remove_non_usable_characters(
                        util.remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.create_infrastructure_request_validator()
    validator.validate(body)
    
    infrastructure = Infrastructure.deserialize(content_type, body)
    
    manager = FlavorSynchronizer()
    manager.register_infrastructure(infrastructure)
    
    response_body = infrastructure.serialize(request.accept_mimetypes)
    
    return Response(response_body, status=201, mimetype=request.accept_mimetypes[0][0])

@app.route("/v1/infrastructures/<name>", methods=['DELETE'])
def unregister_infrastructure(name):
    manager = FlavorSynchronizer()
    manager.unregister_infrastructure(name)
    return Response(status=204)

@app.route("/v1/flavors", methods=['GET'])
def get_flavors():
    promoted = request.args.get('promoted', False, type=bool)
    public = request.args.get('public', False, type=bool)
    
    manager = FlavorSynchronizer()
    flavor_collection = manager.get_flavors(public, promoted)
    
    response_body = flavor_collection.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0]) 

@app.route("/v1/flavors", methods=['POST'])
def create_flavor():
    body = util.remove_non_usable_characters(
                        util.remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.create_flavor_request_validator()
    validator.validate(body)
    
    flavor = Flavor.deserialize(content_type, body)
    
    manager = FlavorSynchronizer()
    created_flavor = manager.create_flavor(flavor)
    
    response_body = created_flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, status=201, mimetype=request.accept_mimetypes[0][0])

@app.route("/v1/flavors/<flavor_id>", methods=['GET'])
def get_flavor(flavor_id):
    manager = FlavorSynchronizer()
    flavor = manager.get_flavor(flavor_id)
    
    response_body = flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0])

@app.route("/v1/flavors/<flavor_id>", methods=['PUT'])
def publish_or_promote_flavor(flavor_id):
    body = util.remove_non_usable_characters(
                        util.remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.create_flavor_modification_request_validator()
    validator.validate(body)
    
    modified_flavor = Flavor.deserialize(content_type, request.data)
    manager = FlavorSynchronizer()
    
    if not modified_flavor.nodes:
        modified_flavor = manager.publish_or_promote_flavor(flavor_id, modified_flavor)
    else:
        modified_flavor = manager.add_node_to_flavor(flavor_id, modified_flavor)
    
    response_body = modified_flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0])

@app.route("/v1/flavors/<flavor_id>", methods=['DELETE'])
def delete_flavor(flavor_id):
    manager = FlavorSynchronizer()
    manager.delete_flavor(flavor_id)
    return Response(status=204)

#////////////////
#Management of the promoted flavors
#////////////////
@app.route("/api/v1/promotedflavors", methods=['GET'])
@requires_auth
def get_promotedflavors():
    promoted = True
    public = True
    
    manager = FlavorSynchronizer()
    #we get only the promoted flavors, not the privates
    flavor_collection = manager.get_flavors(public, promoted)
    
    response_body = flavor_collection.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0]) 

@app.route("/api/v1/promotedflavors", methods=['POST'])
@requires_auth
def create_promotedflavor():
    #Only the users with the appropiate roles could manage the promoted flavors.
    authorization()
    #if the user has the correct roles, they can manage the promoted flavors
    body = util.remove_non_usable_characters(
                        util.remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.create_flavor_request_validator()
    validator.validate(body)
    
    flavor = Flavor.deserialize(content_type, body)
    flavor.promoted =  True
    flavor.public = True
    
    manager = FlavorSynchronizer()
    created_flavor = manager.create_promoted_flavor(flavor)
    print ("request.accept_mimetypes")
    print (request.accept_mimetypes)
    
    response_body = created_flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, status=201, mimetype=request.accept_mimetypes[0][0])


@app.route("/api/v1/promotedflavors/<flavor_id>", methods=['GET'])
@requires_auth
def get_promotedflavor(flavor_id):
    manager = FlavorSynchronizer()
    flavor = manager.get_public_flavor(flavor_id)
    if flavor is None:
        return Response('Not Found Flavor', status=404)
    if not flavor.promoted:
        return Response('The requested resource is not promoted', status=404)
    
    response_body = flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0])

@app.route("/api/v1/promotedflavors/<flavor_id>", methods=['PUT'])
@requires_auth
def modify_promotedflavor(flavor_id):
    #TODO To be decided how to update promoted flavors.
    #Only the users with the appropiate roles could manage the promoted flavors.
    authorization()
    body = util.remove_non_usable_characters(
                        util.remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.create_flavor_modification_request_validator()
    validator.validate(body)
    
    modified_flavor = Flavor.deserialize(content_type, request.data)
    manager = FlavorSynchronizer()
    
    if not modified_flavor.nodes:
        modified_flavor = manager.publish_or_promote_flavor(flavor_id, modified_flavor)
    else:
        return Response("The method specified in the Request-Line is not allowed for the node list of infrastructures.", status=405)
    
    response_body = modified_flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0])

@app.route("/api/v1/promotedflavors/<flavor_id>", methods=['DELETE'])
@requires_auth
def delete_promotedflavor(flavor_id):
    #Only the users with the appropiate roles could manage the promoted flavors.
    authorization()
    manager = FlavorSynchronizer()
    flavor = manager.get_public_flavor(flavor_id)
    if flavor is None:
        return Response('Not Found Flavor', status=404)
    #validate if the flavor is promoted
    if flavor.promoted and not flavor.nodes:
        manager.delete_promoted_flavor(flavor_id)
        return Response(status=204)
    else:
        #error
        return Response("The method specified in the Request-Line is not allowed, since the flavor is not promoted or there are nodes associated to the flavor", status=405)
    

#////////////////
#Management of region flavors
#////////////////
@app.route("/api/v1/nodes", methods=['GET'])
@app.route("/api/v1/regions", methods=['GET'])
@requires_auth
def get_regions():
    manager = FlavorSynchronizer()
    region_collection = manager.get_nodes()

    response_body = region_collection.serialize(request.accept_mimetypes)
    #response_body = ""
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0]) 


@app.route("/api/v1/regions/<region_name>/flavors", methods=['GET'])
@requires_auth
def get_region_flavors(region_name):
    manager = FlavorSynchronizer()
    if not manager.is_node_included(region_name):
        return _create_not_found_region_response(region_name)
    flavor_collection = manager.get_region_flavors(region_name)
    
    response_body = flavor_collection.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0]) 

@app.route("/api/v1/regions/<region_name>/flavors/<flavor_id>", methods=['GET'])
@requires_auth
def get_region_flavor(region_name, flavor_id):
    manager = FlavorSynchronizer()
    if not manager.is_node_included(region_name):
        return _create_not_found_region_response(region_name)
    
    flavor = manager.get_region_flavor(region_name, flavor_id)
    if flavor is None:
        return Response('Not Found Flavor for this region', status=404)
        
    response_body = flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, mimetype=request.accept_mimetypes[0][0])

@app.route("/api/v1/regions/<region_name>/flavors", methods=['POST'])
@requires_auth
def create_region_flavor(region_name):

    if not manager.is_node_included(region_name):
        return _create_not_found_region_response(region_name)

    body = util.remove_non_usable_characters(
                        util.remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.create_flavor_request_validator()
    validator.validate(body)
    
    flavor = Flavor.deserialize(content_type, body)
    flavor.promoted =  False
    flavor.public = False
    
    manager = FlavorSynchronizer()
    created_flavor = manager.create_region_flavor(region_name, flavor)
    
    response_body = created_flavor.serialize(request.accept_mimetypes)
    
    return Response(response_body, status=201, mimetype=request.accept_mimetypes[0][0])

##TODO create the method "modify flavor"!!!!!

@app.route("/api/v1/regions/<region_name>/flavors/<flavor_id>", methods=['DELETE'])
@requires_auth
def delete_region_flavor(region_name, flavor_id):
    if not manager.is_node_included(region_name):
        return _create_not_found_region_response(region_name)
    manager = FlavorSynchronizer()
    manager.delete_region_flavor(region_name, flavor_id)
    return Response(status=204)

def _create_not_found_region_response(region_name):
    return Response('Not Found the region ' + region_name, status=404)