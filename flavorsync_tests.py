import os
import flavorsync
import unittest
import tempfile

from flavorsync.test import parser_unit_tests


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
    
    def test_xml_error_from_model_parser(self):
        parser_unit_tests.xml_error_from_model_parser_test()
    
    def test_json_infrastructure_from_model_parser(self):
        parser_unit_tests.json_infrastructure_from_model_parser_test()
    
    def test_json_flavor_from_model_parser(self):
        parser_unit_tests.json_flavor_from_model_parser_test()
    
    def test_json_flavor_collection_from_model_parser(self):
        parser_unit_tests.json_flavor_collection_from_model_parser_test()
    
    def test_json_error_from_model_parser(self):
        parser_unit_tests.json_error_from_model_parser_test()

if __name__ == '__main__':
    unittest.main()