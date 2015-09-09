from flavorsync import app

from flask import request

from flavorsync.model import Flavor, Infrastructure
from flavorsync.database import db
from flavorsync.flavor_synchronizer import FlavorSynchronizer
from werkzeug.wrappers import Response
from flavorsync.validator import factory_selector
import re

@app.errorhandler(404)
def not_found(error):
    return "The requested resource does not exist", 404

@app.after_request
def shutdown_session(response):
    db.session.remove()
    return response

@app.route("/v1")
def root():
    return "Hello world"

@app.route("/v1/infrastructures", methods=['POST'])
def register_infrastructure():
    body = _remove_non_usable_characters(_remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.createInfrastructureRequestValidator()
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
    body = _remove_non_usable_characters(_remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.createFlavorRequestValidator()
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
    body = _remove_non_usable_characters(_remove_xml_header(request.data.decode("utf-8")))
    content_type = request.content_type
    
    validator_factory = factory_selector.get_factory(content_type)
    validator = validator_factory.createFlavorModificationRequestValidator()
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

def _remove_xml_header(xml):
    return re.sub("<\?.*\?>", "", xml)
    
def _remove_non_usable_characters(xml):
    parsed_xml = re.sub("\\n", "", xml)
    parsed_xml = re.sub(" +<", "<", parsed_xml)
    return parsed_xml