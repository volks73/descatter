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
        self.test_database_file = os.path.join(self.test_catalog_path, constants.TEST_CATALOG_NAME + constants.SQLITE_EXTENSION)        
    
    def setup(self):
        os.mkdir(self.test_catalog_path)
    
    def teardown(self):
        shutil.rmtree(self.test_catalog_path)    
    
    def test_create(self):
        test_catalog = catalog.Catalog()
        test_catalog.create(self.test_catalog_path)
    
        for media_type_name in constants.MEDIA_TYPE_NAMES:
            media_type_path = os.path.join(self.test_content_path, media_type_name)
            assert(os.path.isdir(media_type_path), "'%s' media type folder not created" % media_type_name)
        
        for media_subtype_name, media_type_name in constants.DEFAULT_CONTENT_TYPES.items():
            media_subtype_path = os.path.join(self.test_content_path, media_type_name)
            media_subtype_path = os.path.join(media_subtype_path, media_subtype_name)
            assert(os.path.isdir(media_subtype_path), "%s media subtype folder not created" % media_subtype_name)
            
            number_folder_path = os.path.join(media_subtype_path, '1')
            assert(os.path.isdir(number_folder_path), "Number folder not created for '%s' media subtype" % media_subtype_name)
        
        assert(os.path.isdir(self.test_content_path), "'content' folder not created")
        assert(os.path.isdir(self.test_templates_path), "'templates' folder not created")
        assert(os.path.isdir(self.test_hooks_path), "'hooks' folder not created")
        assert(os.path.isdir(self.test_log_path), "'log' folder not created")
        assert(os.path.isfile(self.test_database_file), "'%s' database file not created" % self.test_database_file)

class TestDatabase(object):
    
    def __init__(self):
        pass
    
    def setup(self):
        # TODO: Add create Test_Catalog folder
        pass
    
    def teardown(self):
        # TODO: Add removal of Test_Catalog folder
        pass
    
    def test_create(self):
        # TOOD: Add assertion of creation of database file
        # TODO: Add assertion of tables created in database file
        # TODO: Add assertion of tables populated with default data
        pass
    
    