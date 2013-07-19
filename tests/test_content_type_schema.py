from datetime import datetime

import os
import unittest
import tempfile

import schema

TEST_FOLDER_NAME = 'tests'
TEST_DATA_FOLDER_NAME = 'data'
TEST_SCHEMA_FILE_PATH = os.path.join(os.getcwd(), TEST_FOLDER_NAME)
TEST_SCHEMA_FILE_PATH = os.path.join(TEST_SCHEMA_FILE_PATH, TEST_DATA_FOLDER_NAME)
TEST_SCHEMA_FILE_PATH = os.path.join(TEST_SCHEMA_FILE_PATH, "test_content_type_schema.xml")

class TestContentTypeSchema(unittest.TestCase): 
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def configure(self, temp_file_suffix, type_folder_name, subtype_folder_name):
    
        test_file_handle, test_source_file_path = tempfile.mkstemp(suffix=temp_file_suffix, prefix='test_descatter_', dir=None, text=False)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.close()
            
        test_file_path, test_file_extension = os.path.splitext(test_source_file_path)
        test_file_name = os.path.basename(test_file_path)
        expected_file_name = test_file_name.title() + test_file_extension
        
        schema_variables = schema.create_variables(test_source_file_path, 1, 1)
            
        expected_value = os.path.join(type_folder_name, subtype_folder_name)
        expected_value = os.path.join(expected_value, schema.RANDOM_FOLDER_PLACEHOLDER)
        expected_value = os.path.join(expected_value, expected_file_name)
        
        return (test_source_file_path, schema_variables, expected_value)
    
    def test_txt_file(self):
        test_source_file_path, schema_variables, expected_value = self.configure('.txt', 'Text', 'plain')
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        output_value = test_path_finder.find_path(test_source_file_path, schema_variables)
                
        self.assertEqual(output_value, expected_value)
        
        os.remove(test_source_file_path)

    def test_doc_file(self):
        test_source_file_path, schema_variables, expected_value = self.configure('.doc', 'Application', 'msword')
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        output_value = test_path_finder.find_path(test_source_file_path, schema_variables)
                
        self.assertEqual(output_value, expected_value)
        
        os.remove(test_source_file_path)
    
    def test_docx_file(self):
        test_source_file_path, schema_variables, expected_value = self.configure('.docx', 'Application', 'msword')
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        output_value = test_path_finder.find_path(test_source_file_path, schema_variables)
                
        self.assertEqual(output_value, expected_value)
        
        os.remove(test_source_file_path)
    
    def test_tif_file(self):
        test_source_file_path, schema_variables, expected_value = self.configure('.tif', 'Image', 'tiff')
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        output_value = test_path_finder.find_path(test_source_file_path, schema_variables)
                
        self.assertEqual(output_value, expected_value)
        
        os.remove(test_source_file_path)
    
    def test_tiff_file(self):
        test_source_file_path, schema_variables, expected_value = self.configure('.tiff', 'Image', 'tiff')
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        output_value = test_path_finder.find_path(test_source_file_path, schema_variables)
                
        self.assertEqual(output_value, expected_value)
        
        os.remove(test_source_file_path)
    
    def test_mp3_file(self):
        test_source_file_path, schema_variables, expected_value = self.configure('.mp3', 'Audio', 'mp3')
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        output_value = test_path_finder.find_path(test_source_file_path, schema_variables)
                
        self.assertEqual(output_value, expected_value)
        
        os.remove(test_source_file_path)
    
    def test_avi_file(self):
        test_source_file_path, schema_variables, expected_value = self.configure('.avi', 'Video', 'avi')
        
        test_path_finder = schema.PathFinder(TEST_SCHEMA_FILE_PATH)
        output_value = test_path_finder.find_path(test_source_file_path, schema_variables)
                
        self.assertEqual(output_value, expected_value)
        
        os.remove(test_source_file_path)