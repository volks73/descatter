import os
import unittest
import tempfile
import shutil

import filer

TEST_FOLDER_NAME = 'tests'
TEST_DATA_FOLDER_NAME = 'data'
TEST_DIRECTIVE_FILE_PATH = os.path.join(os.getcwd(), TEST_FOLDER_NAME)
TEST_DIRECTIVE_FILE_PATH = os.path.join(TEST_DIRECTIVE_FILE_PATH, TEST_DATA_FOLDER_NAME)
TEST_DIRECTIVE_FILE_PATH = os.path.join(TEST_DIRECTIVE_FILE_PATH, "test_content_type_directive.xml")

class TestFiler(unittest.TestCase):
    
    def setUp(self):
        self.test_base_folder_path = tempfile.mkdtemp(suffix='', prefix='test_filer_', dir=None)
        test_file_handle, self.test_source_file_path = tempfile.mkstemp(suffix='.txt', prefix='test_filer_', dir=None, text=False)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.close()
        
    def tearDown(self):
        os.remove(self.test_source_file_path)
        shutil.rmtree(self.test_base_folder_path)
        
    def test_file_single(self):
        processor = filer.Processor(self.test_base_folder_path, TEST_DIRECTIVE_FILE_PATH)
        processor.file(self.test_source_file_path)
        
        # TODO: Change to using string of XML instead of file
        # TODO: Add check for file copied to appropriate destination