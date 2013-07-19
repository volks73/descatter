import os
import unittest
import tempfile
import shutil

import descatter

TEST_FOLDER_NAME = 'tests'
TEST_DATA_FOLDER_NAME = 'data'
TEST_SCHEMA_FILE_PATH = os.path.join(os.getcwd(), TEST_FOLDER_NAME)
TEST_SCHEMA_FILE_PATH = os.path.join(TEST_SCHEMA_FILE_PATH, TEST_DATA_FOLDER_NAME)
TEST_SCHEMA_FILE_PATH = os.path.join(TEST_SCHEMA_FILE_PATH, "test_content_type_schema.xml")

class TestFiler(unittest.TestCase):
    
    def setUp(self):
        self.test_base_folder_path = tempfile.mkdtemp(suffix='', prefix='test_descatter_', dir=None)
        test_file_handle, self.test_source_file_path = tempfile.mkstemp(suffix='.txt', prefix='test_descatter_', dir=None, text=False)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.close()
        
    def tearDown(self):
        os.remove(self.test_source_file_path)
        shutil.rmtree(self.test_base_folder_path)
        
    def test_file(self):
        filer = descatter.Filer(self.test_base_folder_path, TEST_SCHEMA_FILE_PATH)
        filer.file(self.test_source_file_path)
        
        # TODO: Add check for file copied to appropriate destination
    
    def test_batch_file(self):
        pass
    
    def test_recursive_file(self):
        pass