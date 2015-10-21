import os
import flavorsync
import unittest
import tempfile
import flavorsync.views
import flavorsync.test.config as config

from flavorsync.test import parser_unit_tests, model_unit_tests, validation_unit_tests,\
    use_case_tests
from flavorsync import database
from flavorsync.openstack.openstack_manager import OpenStackManager
from flavorsync.model import Infrastructure


class flavorsyncTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flavorsync.app.config['DATABASE'] = tempfile.mkstemp()
        flavorsync.app.config['TESTING'] = True
        self.app = flavorsync.app.test_client()
        #flavorsync.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flavorsync.app.config['DATABASE'])
    
    def test_create_xml_infrastructure_parser_factory(self):
        parser_unit_tests.create_xml_infrastructure_parser_factory_test()
    
    def test_create_xml_flavor_parser_factory(self):
        parser_unit_tests.create_xml_flavor_parser_factory_test()
    
    def test_create_xml_flavor_collection_parser_factory(self):
        parser_unit_tests.create_xml_flavor_collection_parser_factory_test()
    
    def test_create_xml_exception_parser_factory(self):
        parser_unit_tests.create_xml_exception_parser_factory_test()
    
    def test_create_json_infrastructure_parser_factory(self):
        parser_unit_tests.create_json_infrastructure_parser_factory_test()
    
    def test_create_json_flavor_parser_factory(self):
        parser_unit_tests.create_json_flavor_parser_factory_test()
    
    def test_create_json_flavor_collection_parser_factory(self):
        parser_unit_tests.create_json_flavor_collection_parser_factory_test()
    
    def test_create_json_exception_parser_factory(self):
        parser_unit_tests.create_json_exception_parser_factory_test()
    
    def test_create_wrong_mimetype_infrastructure_parser_factory(self):
        parser_unit_tests.create_wrong_mimetype_infrastructure_parser_factory_test()
    
    def test_create_wrong_mimetype_flavor_parser_factory(self):
        parser_unit_tests.create_wrong_mimetype_flavor_parser_factory_test()
    
    def test_create_wrong_mimetype_flavor_collection_parser_factory(self):
        parser_unit_tests.create_wrong_mimetype_flavor_collection_parser_factory_test()
    
    def test_create_wrong_mimetype_exception_parser_factory(self):
        parser_unit_tests.create_wrong_mimetype_exception_parser_factory_test()
    
    def test_create_xml_wrong_type_parser_factory(self):
        parser_unit_tests.create_xml_wrong_type_parser_factory_test()
    
    def test_create_json_wrong_type_parser_factory(self):
        parser_unit_tests.create_json_wrong_type_parser_factory_test()
    
    def test_xml_infrastructure_to_dict_parser(self):
        parser_unit_tests.xml_infrastructure_to_dict_parser_test()
    
    def test_xml_flavor_to_dict_parser(self):
        parser_unit_tests.xml_flavor_to_dict_parser_test()
    
    def test_xml_flavor_publication_to_dict_parser(self):
        parser_unit_tests.xml_flavor_publication_to_dict_parser_test()
    
    def test_xml_flavor_promotion_to_dict_parser(self):
        parser_unit_tests.xml_flavor_promotion_to_dict_parser_test()
    
    def test_xml_flavor_installation_to_dict_parser(self):
        parser_unit_tests.xml_flavor_installation_to_dict_parser_test()
    
    def test_json_infrastructure_to_dict_parser(self):
        parser_unit_tests.json_infrastructure_to_dict_parser_test()
    
    def test_json_flavor_to_dict_parser(self):
        parser_unit_tests.json_flavor_to_dict_parser_test()
    
    def test_json_flavor_publication_to_dict_parser(self):
        parser_unit_tests.json_flavor_publication_to_dict_parser_test()
    
    def test_json_flavor_promotion_to_dict_parser(self):
        parser_unit_tests.json_flavor_promotion_to_dict_parser_test()
    
    def test_json_flavor_installation_to_dict_parser(self):
        parser_unit_tests.json_flavor_installation_to_dict_parser_test()
    
    def test_xml_flavor_collection_to_dict_parser(self):
        parser_unit_tests.xml_flavor_collection_to_dict_parser_test()
    
    def test_xml_exception_to_dict_parser(self):
        parser_unit_tests.xml_exception_to_dict_parser_test()
    
    def test_json_flavor_collection_to_dict_parser(self):
        parser_unit_tests.json_flavor_collection_to_dict_parser_test()
    
    def test_json_exception_to_dict_parser(self):
        parser_unit_tests.json_exception_to_dict_parser_test()
    
    def test_xml_infrastructure_from_model_parser(self):
        parser_unit_tests.xml_infrastructure_from_model_parser_test()
    
    def test_xml_flavor_from_model_parser(self):
        parser_unit_tests.xml_flavor_from_model_parser_test()
    
    def test_xml_flavor_collection_from_model_parser(self):
        parser_unit_tests.xml_flavor_collection_from_model_parser_test()
    
    def test_xml_empty_flavor_collection_from_model_parser(self):
        parser_unit_tests.xml_empty_flavor_collection_from_model_parser_test()
    
    def test_xml_error_from_model_parser(self):
        parser_unit_tests.xml_error_from_model_parser_test()
    
    def test_json_infrastructure_from_model_parser(self):
        parser_unit_tests.json_infrastructure_from_model_parser_test()
    
    def test_json_flavor_from_model_parser(self):
        parser_unit_tests.json_flavor_from_model_parser_test()
    
    def test_json_flavor_collection_from_model_parser(self):
        parser_unit_tests.json_flavor_collection_from_model_parser_test()
    
    def test_json_empty_flavor_collection_from_model_parser(self):
        parser_unit_tests.json_empty_flavor_collection_from_model_parser_test()
    
    def test_json_error_from_model_parser(self):
        parser_unit_tests.json_error_from_model_parser_test()
    
    
    
    
    def test_deserialize_xml_infrastructure(self):
        model_unit_tests.deserialize_xml_infrastructure_test()
    
    def test_deserialize_json_infrastructure(self):
        model_unit_tests.deserialize_json_infrastructure_test()
    
    def test_deserialize_wrong_mimetype_infrastructure(self):
        model_unit_tests.deserialize_wrong_mimetype_infrastructure_test()
    
    def test_serialize_xml_infrastructure(self):
        model_unit_tests.serialize_xml_infrastructure_test()
    
    def test_serialize_json_infrastructure(self):
        model_unit_tests.serialize_json_infrastructure_test()
    
    def test_serialize_wrong_mimetype_infrastructure(self):
        model_unit_tests.serialize_wrong_mimetype_infrastructure_test()
    
    def test_infrastructure_to_content_dict(self):
        model_unit_tests.infrastructure_to_content_dict_test()
    
    def test_infrastructure_to_dict(self):
        model_unit_tests.infrastructure_to_dict_test()
    
    def test_deserialize_xml_flavor(self):
        model_unit_tests.deserialize_xml_flavor_test()
    
    def test_deserialize_json_flavor(self):
        model_unit_tests.deserialize_json_flavor_test()
    
    def test_deserialize_wrong_mimetype_flavor(self):
        model_unit_tests.deserialize_wrong_mimetype_flavor_test()
    
    def test_serialize_xml_flavor(self):
        model_unit_tests.serialize_xml_flavor_test()
    
    def test_serialize_json_flavor(self):
        model_unit_tests.serialize_json_flavor_test()
    
    def test_serialize_wrong_mimetype_flavor(self):
        model_unit_tests.serialize_wrong_mimetype_flavor_test()
    
    def test_flavor_to_content_dict(self):
        model_unit_tests.flavor_to_content_dict_test()
    
    def test_flavor_to_dict(self):
        model_unit_tests.flavor_to_dict_test()
    
    def test_from_openstack_flavor(self):
        model_unit_tests.from_openstack_flavor_test()
    
    def test_serialize_xml_flavor_collection(self):
        model_unit_tests.serialize_xml_flavor_collection_test()
    
    def test_serialize_xml_empty_flavor_collection(self):
        model_unit_tests.serialize_xml_empty_flavor_collection_test()
    
    def test_serialize_json_flavor_collection(self):
        model_unit_tests.serialize_json_flavor_collection_test()
    
    def test_serialize_json_empty_flavor_collection(self):
        model_unit_tests.serialize_json_empty_flavor_collection_test()
    
    def test_serialize_wrong_mimetype_flavor_collection(self):
        model_unit_tests.serialize_wrong_mimetype_flavor_collection_test()
    
    def test_flavor_collection_to_dict(self):
        model_unit_tests.flavor_collection_to_dict_test()
    
    def test_empty_flavor_collection_to_dict(self):
        model_unit_tests.emtpy_flavor_collection_to_dict_test()
    
    def test_from_openstack_flavor_list(self):
        model_unit_tests.from_openstack_flavor_list_test()
    
    def test_from_empty_openstack_flavor_list(self):
        model_unit_tests.from_empty_openstack_flavor_list_test()
    
    def test_flavor_collection_extend_list(self):
        model_unit_tests.flavor_collection_extend_list_test()



    def test_create_xml_validator_factory(self):
        validation_unit_tests.create_xml_validator_factory_test()
    
    def test_create_json_validator_factory(self):
        validation_unit_tests.create_json_validator_factory_test()
    
    def test_create_wrong_mimetype_validator_factory(self):
        validation_unit_tests.create_wrong_mimetype_validator_factory_test()
    
    def test_create_xml_ivalidator(self):
        validation_unit_tests.create_xml_ivalidator_test()
    
    def test_create_json_ivalidator(self):
        validation_unit_tests.create_json_ivalidator_test()
    
    def test_create_wrong_mimetype_ivalidator(self):
        validation_unit_tests.create_wrong_mimetype_ivalidator_test()
    
    def test_validate_xml_exception_payload(self):
        validation_unit_tests.validate_xml_exception_payload(self)
    
    def test_validate_xml_flavor_collection_payload(self):
        validation_unit_tests.validate_xml_flavor_collection_payload(self)
    
    def test_validate_empty_xml_flavor_collection_payload(self):
        validation_unit_tests.validate_empty_xml_flavor_collection_payload(self)
    
    def test_validate_xml_flavor_creation_payload(self):
        validation_unit_tests.validate_xml_flavor_creation_payload(self)
    
    def test_validate_xml_flavor_installation_payload(self):
        validation_unit_tests.validate_xml_flavor_installation_payload(self)
    
    def test_validate_xml_flavor_promotion_payload(self):
        validation_unit_tests.validate_xml_flavor_promotion_payload(self)
    
    def test_validate_xml_flavor_publication_payload(self):
        validation_unit_tests.validate_xml_flavor_publication_payload(self)
    
    def test_validate_xml_flavor_payload(self):
        validation_unit_tests.validate_xml_flavor_payload(self)
    
    def test_validate_xml_infrastructure_request_payload(self):
        validation_unit_tests.validate_xml_infrastructure_request_payload(self)
    
    def test_validate_xml_infrastructure_payload(self):
        validation_unit_tests.validate_xml_infrastructure_payload(self)
    
    def test_validate_json_exception_payload(self):
        validation_unit_tests.validate_json_exception_payload(self)
    
    def test_validate_json_flavor_collection_payload(self):
        validation_unit_tests.validate_json_flavor_collection_payload(self)
    
    def test_validate_empty_json_flavor_collection_payload(self):
        validation_unit_tests.validate_empty_json_flavor_collection_payload(self)
    
    def test_validate_json_flavor_creation_payload(self):
        validation_unit_tests.validate_json_flavor_creation_payload(self)
    
    def test_validate_json_flavor_installation_payload(self):
        validation_unit_tests.validate_json_flavor_installation_payload(self)
    
    def test_validate_json_flavor_promotion_payload(self):
        validation_unit_tests.validate_json_flavor_promotion_payload(self)
    
    def test_validate_json_flavor_publication_payload(self):
        validation_unit_tests.validate_json_flavor_publication_payload(self)
    
    def test_validate_json_flavor_payload(self):
        validation_unit_tests.validate_json_flavor_payload(self)
    
    def test_validate_json_infrastructure_request_payload(self):
        validation_unit_tests.validate_json_infrastructure_request_payload(self)
    
    def test_validate_json_infrastructure_payload(self):
        validation_unit_tests.validate_json_infrastructure_payload(self)

class flavorsyncTestCase2(unittest.TestCase):

    def setUp(self):
        self.db_fd, flavorsync.app.config['DB_TEST_URI'] = tempfile.mkstemp()
        flavorsync.app.config['TESTING'] = True
        self.app = flavorsync.app.test_client()
        
        with flavorsync.app.app_context():
             database.init_db(flavorsync.app)

    def tearDown(self):
        try:
            flavor_id = self.flavor_id
            infrastructure = Infrastructure(
                                    'Mordor',
                                    config.OPENSTACK_TEST_KEYSTONE_URL,
                                    config.OPENSTACK_TEST_USERNAME,
                                    config.OPENSTACK_TEST_PASSWORD,
                                    config.OPENSTACK_TEST_TENANT)
            openstackmanager = OpenStackManager(infrastructure)
            openstackmanager.delete_flavor(flavor_id)
        except AttributeError:
        	pass
        
        os.close(self.db_fd)
        os.unlink(flavorsync.app.config['DB_TEST_URI'])
    
    def test_register_and_unregister_infrastucture(self):
        use_case_tests.infrastructure_on_line_test(self.app)
        use_case_tests.register_new_infrastucture_xml_test(self.app)
        use_case_tests.unregister_infrastucture_test(self.app)
        use_case_tests.register_new_infrastucture_json_test(self.app)
        use_case_tests.unregister_infrastucture_test(self.app)
    
    def test_list_flavors(self):
        use_case_tests.infrastructure_on_line_test(self.app)
        use_case_tests.register_new_infrastucture_xml_test(self.app)
        use_case_tests.unregister_infrastucture_test(self.app)
        use_case_tests.register_new_infrastucture_json_test(self.app)
        use_case_tests.list_all_flavors_xml_test(self.app)
        use_case_tests.list_all_flavors_json_test(self.app)
    
    def test_create_and_delete_flavors(self):
        use_case_tests.infrastructure_on_line_test(self.app)
        use_case_tests.register_new_infrastucture_xml_test(self.app)
        use_case_tests.unregister_infrastucture_test(self.app)
        use_case_tests.register_new_infrastucture_json_test(self.app)
        flavor_id = use_case_tests.create_new_flavor_xml_test(self.app)
        use_case_tests.list_all_flavors_xml_test(self.app,flavor_id)
        use_case_tests.list_all_flavors_json_test(self.app,flavor_id)
        use_case_tests.delete_flavor_test(self.app, flavor_id)
        flavor_id = use_case_tests.create_new_flavor_json_test(self.app)
        use_case_tests.list_all_flavors_xml_test(self.app,flavor_id)
        use_case_tests.list_all_flavors_json_test(self.app,flavor_id)
        use_case_tests.get_flavor_info_xml_test(self.app, flavor_id)
        use_case_tests.get_flavor_info_json_test(self.app, flavor_id)
        use_case_tests.delete_flavor_test(self.app, flavor_id)
        use_case_tests.unregister_infrastucture_test(self.app)
    
    def test_publish_and_promote_flavor_xml(self):
        use_case_tests.infrastructure_on_line_test(self.app)
        use_case_tests.register_new_infrastucture_xml_test(self.app)
        self.flavor_id = use_case_tests.create_new_flavor_xml_test(self.app)
        use_case_tests.publish_flavor_xml_test(self.app, self.flavor_id)
        use_case_tests.promote_flavor_xml_test(self.app, self.flavor_id)
    
    def test_publish_and_promote_flavor_json(self):
        use_case_tests.infrastructure_on_line_test(self.app)
        use_case_tests.register_new_infrastucture_json_test(self.app)
        self.flavor_id = use_case_tests.create_new_flavor_json_test(self.app)
        use_case_tests.publish_flavor_json_test(self.app, self.flavor_id)
        use_case_tests.promote_flavor_json_test(self.app, self.flavor_id)
    
    def test_install_flavor_xml(self):
        use_case_tests.infrastructure_on_line_test(self.app)
        use_case_tests.register_new_infrastucture_xml_test(self.app)
        self.flavor_id = use_case_tests.install_flavor_xml_test(self.app)
        use_case_tests.list_all_flavors_xml_test(self.app, self.flavor_id)
        use_case_tests.list_all_flavors_json_test(self.app, self.flavor_id)
    
    def test_install_flavor_json(self):
        use_case_tests.infrastructure_on_line_test(self.app)
        use_case_tests.register_new_infrastucture_json_test(self.app)
        self.flavor_id = use_case_tests.install_flavor_json_test(self.app)
        use_case_tests.list_all_flavors_xml_test(self.app, self.flavor_id)
        use_case_tests.list_all_flavors_json_test(self.app, self.flavor_id)

if __name__ == '__main__':
    unittest.main()