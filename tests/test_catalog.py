from nose.tools import *
from descatter.catalog import *

import os
import shutil

class TestCatalog(object):
    
    def __init__(self):
        self.test_catalog_name = 'Test_Catalog'
        self.test_path = os.path.join(os.getcwd(), 'tests')
        self.test_catalog_path = os.path.join(self.test_path, self.test_catalog_name)
        self.test_content_path = os.path.join(self.test_catalog_path, 'content')
        self.test_templates_path = os.path.join(self.test_catalog_path, 'templates')
        self.test_hooks_path = os.path.join(self.test_catalog_path, 'hooks')
        self.test_log_path = os.path.join(self.test_catalog_path, 'log')
        self.test_database_file = os.path.join(self.test_catalog_path, self.test_catalog_name + SQLITE_EXTENSION)        
    
    def setup(self):
        os.mkdir(self.test_catalog_path)
    
    def teardown(self):
        shutil.rmtree(self.test_catalog_path)    
    
    def test_create(self):
        test_catalog = Catalog()
        test_catalog.create(self.test_catalog_path)
        
        assert os.path.isdir(self.test_content_path), "Content folder not created"
        assert os.path.isdir(self.test_templates_path), "Templates folder not created"
        assert os.path.isdir(self.test_hooks_path), "Hooks folder not created"
        assert os.path.isdir(self.test_log_path), "Log folder not created"
        assert os.path.isfile(self.test_database_file), "Database file not created"
    