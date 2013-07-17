import os
import unittest
import tempfile

import schema

TEST_FOLDER_NAME = 'tests'
TEST_DATA_FOLDER_NAME = 'data'
TEST_SCHEMA_FILE_PATH = os.path.join(os.getcwd(), TEST_FOLDER_NAME)
TEST_SCHEMA_FILE_PATH = os.path.join(TEST_SCHEMA_FILE_PATH, TEST_DATA_FOLDER_NAME)
TEST_SCHEMA_FILE_PATH = os.path.join(TEST_SCHEMA_FILE_PATH, "test_content_type_schema.xml")

class TestTextFile(unittest.TestCase): 
    
    def setUp(self):
        test_file_handle, self.test_source_file_path = tempfile.mkstemp(suffix='.txt', prefix='test_descatter_', dir=None, text=True)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.write("A temporary test file for the descatter application unit testing\n")
        test_file.close()
    
    def tearDown(self):
        os.remove(self.test_source_file_path)
    
    def test_text_file_find_path(self):
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        
        test_file_path, test_file_extension = os.path.splitext(self.test_source_file_path)
        test_file_name = os.path.basename(test_file_path)
        test_file_name = test_file_name.title() + test_file_extension
        
        expected_value = os.path.join('Text', 'plain')
        expected_value = os.path.join(expected_value, schema.RANDOM_FOLDER_PLACEHOLDER)
        expected_value = os.path.join(expected_value, test_file_name)
        output_value = test_path_finder.find_path(self.test_source_file_path)
        
        self.assertEqual(output_value, expected_value)

class TestWordFile(unittest.TestCase): 
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_doc_file_find_path(self):
        test_file_handle, self.test_source_file_path = tempfile.mkstemp(suffix='.doc', prefix='test_descatter_', dir=None, text=False)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.close()
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        
        test_file_path, test_file_extension = os.path.splitext(self.test_source_file_path)
        test_file_name = os.path.basename(test_file_path)
        test_file_name = test_file_name.title() + test_file_extension
        
        expected_value = os.path.join('Application', 'msword')
        expected_value = os.path.join(expected_value, schema.RANDOM_FOLDER_PLACEHOLDER)
        expected_value = os.path.join(expected_value, test_file_name)
        output_value = test_path_finder.find_path(self.test_source_file_path)
        
        self.assertEqual(output_value, expected_value)
        
        os.remove(self.test_source_file_path)
    
    def test_docx_file_find_path(self):
        test_file_handle, self.test_source_file_path = tempfile.mkstemp(suffix='.docx', prefix='test_descatter_', dir=None, text=False)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.close()
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        
        test_file_path, test_file_extension = os.path.splitext(self.test_source_file_path)
        test_file_name = os.path.basename(test_file_path)
        test_file_name = test_file_name.title() + test_file_extension
        
        expected_value = os.path.join('Application', 'msword')
        expected_value = os.path.join(expected_value, schema.RANDOM_FOLDER_PLACEHOLDER)
        expected_value = os.path.join(expected_value, test_file_name)
        output_value = test_path_finder.find_path(self.test_source_file_path)
        
        self.assertEqual(output_value, expected_value)
        
        os.remove(self.test_source_file_path)