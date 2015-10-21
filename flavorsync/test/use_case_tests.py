import flavorsync.test.util as util
from flavorsync.validator import factory_selector
from flavorsync.test.util import XML_MIMETYPE, JSON_MIMETYPE
from jsonschema.exceptions import ValidationError

from lxml import etree
from lxml import objectify
import json
from flavorsync.model import Infrastructure
from flavorsync.database_manager import DatabaseManager
import flavorsync

def infrastructure_on_line_test(app):
    response = app.get('/v1', follow_redirects=True)
    assert response.status_code == 200
    assert 'Hello world' in response.data.decode("utf-8")

def register_new_infrastucture_xml_test(app):
    content_type=XML_MIMETYPE
    accept=XML_MIMETYPE
    
    request_body = util.load_xml_example_as_string('infrastructure_bad_request.xml')
    response = app.post('/v1/infrastructures', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_xml_example_as_string('infrastructure_request.xml')
    response = app.post('/v1/infrastructures', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 201
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_infrastructure_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    response = app.post('/v1/infrastructures', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    assert response.status_code == 409

def register_new_infrastucture_json_test(app):
    content_type=JSON_MIMETYPE
    accept=JSON_MIMETYPE
    
    
    request_body = util.load_json_example_as_string('infrastructure_bad_request.json')
    response = app.post('/v1/infrastructures', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_json_example_as_string('infrastructure_request.json')
    response = app.post('/v1/infrastructures', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 201
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_infrastructure_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    response = app.post('/v1/infrastructures', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    assert response.status_code == 409

def list_all_flavors_xml_test(app, flavor_id=None):
    accept=XML_MIMETYPE
    response = app.get('/v1/flavors', headers={'accept': accept}, follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_collection_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    if flavor_id:
        flavors = objectify.fromstring(response_body)
        n_ocurrences = len(flavors.xpath("flavor[@id='{0}']".format(flavor_id)))
        assert n_ocurrences == 1
        assert flavors.xpath("flavor[@id='{0}']/node='Mordor'".format(flavor_id))

def list_all_flavors_json_test(app, flavor_id=None):
    accept=JSON_MIMETYPE
    response = app.get('/v1/flavors', headers={'accept': accept}, follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_collection_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    if flavor_id:
        exists = False
        flavors = json.loads(response_body)
        for flavor in flavors['flavors']:
            if flavor_id in flavor['id']:
                exists = True
                isinstalled = 'Mordor' in flavor['nodes']
                break
        assert exists
        assert isinstalled

def create_new_flavor_xml_test(app):
    content_type=XML_MIMETYPE
    accept=XML_MIMETYPE
    
    request_body = util.load_xml_example_as_string('flavor_creation_bad_request.xml')
    response = app.post('/v1/flavors', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_xml_example_as_string('flavor_creation_request.xml')
    response = app.post('/v1/flavors', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 201
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
        
    response = app.post('/v1/flavors', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 409
    
    xml = objectify.fromstring(response_body)
    return xml.values()[0]

def create_new_flavor_json_test(app):
    content_type=JSON_MIMETYPE
    accept=JSON_MIMETYPE
    
    request_body = util.load_json_example_as_string('flavor_creation_bad_request.json')
    response = app.post('/v1/flavors', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_json_example_as_string('flavor_creation_request.json')
    response = app.post('/v1/flavors', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 201
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
        
    response = app.post('/v1/flavors', data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 409
    
    flavor = json.loads(response_body)
    return flavor['flavor']['id']

def get_flavor_info_xml_test(app, flavor_id):
    accept=XML_MIMETYPE
    
    response = app.get('/v1/flavors/idontexist', headers={'accept': accept}, follow_redirects=True)
    
    assert response.status_code == 404
    
    response = app.get('/v1/flavors/{0}'.format(flavor_id), headers={'accept': accept}, follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False

def get_flavor_info_json_test(app, flavor_id):
    accept=JSON_MIMETYPE
    
    response = app.get('/v1/flavors/idontexist', headers={'accept': accept}, follow_redirects=True)
    
    assert response.status_code == 404
    
    response = app.get('/v1/flavors/{0}'.format(flavor_id), headers={'accept': accept}, follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False

def install_flavor_xml_test(app):
    content_type=XML_MIMETYPE
    accept=XML_MIMETYPE
    
    fake_flavor_id = _create_fake_infrastructure_and_flavor()
    
    request_body = util.load_xml_example_as_string('flavor_installation_request.xml')
    response = app.put('/v1/flavors/{0}'.format(fake_flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    return fake_flavor_id

def install_flavor_json_test(app):
    content_type=JSON_MIMETYPE
    accept=JSON_MIMETYPE
    
    fake_flavor_id = _create_fake_infrastructure_and_flavor()
    
    request_body = util.load_json_example_as_string('flavor_installation_request.json')
    response = app.put('/v1/flavors/{0}'.format(fake_flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    return fake_flavor_id

def publish_flavor_xml_test(app, flavor_id):
    content_type=XML_MIMETYPE
    accept=XML_MIMETYPE
    
    request_body = util.load_xml_example_as_string('flavor_publication_bad_request.xml')
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_xml_example_as_string('flavor_publication_request.xml')
    response = app.put('/v1/flavors/idontexist'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 404
    
    
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    request_body = util.load_xml_example_as_string('flavor_unpublication_request.xml')
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 409

def publish_flavor_json_test(app, flavor_id):
    content_type=JSON_MIMETYPE
    accept=JSON_MIMETYPE
    
    request_body = util.load_json_example_as_string('flavor_publication_bad_request.json')
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_json_example_as_string('flavor_publication_request.json')
    response = app.put('/v1/flavors/idontexist'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 404
    
    
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    request_body = util.load_json_example_as_string('flavor_unpublication_request.json')
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 409


def promote_flavor_xml_test(app, flavor_id):
    content_type=XML_MIMETYPE
    accept=XML_MIMETYPE
    
    request_body = util.load_xml_example_as_string('flavor_promotion_bad_request.xml')
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_xml_example_as_string('flavor_promotion_request.xml')
    response = app.put('/v1/flavors/idontexist'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 404
    
    
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False

def promote_flavor_json_test(app, flavor_id):
    content_type=JSON_MIMETYPE
    accept=JSON_MIMETYPE
    
    request_body = util.load_json_example_as_string('flavor_promotion_bad_request.json')
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 400
    
    request_body = util.load_json_example_as_string('flavor_promotion_request.json')
    response = app.put('/v1/flavors/idontexist'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 404
    
    response = app.put('/v1/flavors/{0}'.format(flavor_id), data=request_body, content_type=content_type, headers={'accept': accept},  follow_redirects=True)
    
    assert response.status_code == 200
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_flavor_validator()
    
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False

def delete_flavor_test(app, flavor_id):
    accept=XML_MIMETYPE
    
    response = app.delete('/v1/flavors/{0}'.format(flavor_id), headers={'accept': accept}, follow_redirects=True)
    assert response.status_code == 204
    
    response = app.delete('/v1/flavors/{0}'.format(flavor_id), headers={'accept': accept}, follow_redirects=True)
    assert response.status_code == 404
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_exception_validator()
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    accept=JSON_MIMETYPE
    
    response = app.delete('/v1/flavors/{0}'.format(flavor_id), headers={'accept': accept}, follow_redirects=True)
    assert response.status_code == 404
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_exception_validator()
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False

def unregister_infrastucture_test(app):
    accept=XML_MIMETYPE
    
    response = app.delete('/v1/infrastructures/Isengard', headers={'accept': accept}, follow_redirects=True)
    assert response.status_code == 404
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_exception_validator()
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    accept=JSON_MIMETYPE
    
    response = app.delete('/v1/infrastructures/Isengard', headers={'accept': accept}, follow_redirects=True)
    assert response.status_code == 404
    
    response_body = response.data.decode("utf-8")
    
    validator_factory = factory_selector.get_factory(accept)
    validator = validator_factory.create_exception_validator()
    try:
        validator.validate(response_body)
        assert True
    except ValidationError:
        assert False
    
    response = app.delete('/v1/infrastructures/Mordor', headers={'accept': accept}, follow_redirects=True)
    assert response.status_code == 204

def _create_fake_infrastructure_and_flavor():
    with flavorsync.app.app_context():
        manager = DatabaseManager()
        
        flavor = util.create_secondary_example_flavor()
        
        manager.register_infrastructure(flavor.nodes[0])
        manager.create_flavor(flavor)
        
        return flavor.id