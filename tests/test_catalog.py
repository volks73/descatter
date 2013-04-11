from nose.tools import *

import os
import shutil
import catalog
import constants

class TestCatalog(object):
    
    def __init__(self):
        self.test_path = os.path.join(os.getcwd(), constants.TESTS_FOLDER_NAME)
        self.test_catalog_path = os.path.join(self.test_path, constants.TEST_CATALOG_NAME)
        self.test_content_path = os.path.join(self.test_catalog_path, constants.CONTENT_FOLDER_NAME)
        self.test_templates_path = os.path.join(self.test_catalog_path, constants.TEMPLATES_FOLDER_NAME)
        self.test_hooks_path = os.path.join(self.test_catalog_path, constants.HOOKS_FOLDER_NAME)
        self.test_log_path = os.path.join(self.test_catalog_path, constants.LOG_FOLDER_NAME)
        self.test_database_file = os.path.join(self.test_catalog_path, self.test_catalog_name + constants.SQLITE_EXTENSION)        
    
    def setup(self):
        os.mkdir(self.test_catalog_path)
    
    def teardown(self):
        shutil.rmtree(self.test_catalog_path)    
    
    def test_create(self):
        test_catalog = catalog.Catalog()
        test_catalog.create(self.test_catalog_path)
        
        assert(os.path.isdir(self.test_content_path), "Content folder not created")
        assert(os.path.isdir(self.test_templates_path), "Templates folder not created")
        assert(os.path.isdir(self.test_hooks_path), "Hooks folder not created")
        assert(os.path.isdir(self.test_log_path), "Log folder not created")
        assert(os.path.isfile(self.test_database_file), "Database file not created")
    