import os
import unittest

import catalog
import constants

class TestContentSchema(unittest.TestCase):
    
    def setUp(self):
        self.test_schema_file_path = os.path.join(os.getcwd(), constants.APPLICATION_NAME)
        self.test_schema_file_path = os.path.join(self.test_schema_file_path, constants.DATA_FOLDER_NAME)
        self.test_schema_file_path = os.path.join(self.test_schema_file_path, "prototype_schema.xml")
    
        test_checkin_file_path = os.path.join(os.getcwd(), "CHANGES.txt")
    
        self.test_checkin_file = catalog.create_checkin_file(test_checkin_file_path)
    
    def tearDown(self):
        pass
    
    def test_get_destination(self):
        test_content_schema = catalog.ContentSchema(self.test_schema_file_path)
        test_content_schema.get_destination(self.test_checkin_file)