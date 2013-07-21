import os
import unittest
import tempfile
import shutil

import organize

TEST_FOLDER_NAME = 'tests'
TEST_DATA_FOLDER_NAME = 'data'
TEST_DIRECTIVE_FILE_PATH = os.path.join(os.getcwd(), TEST_FOLDER_NAME)
TEST_DIRECTIVE_FILE_PATH = os.path.join(TEST_DIRECTIVE_FILE_PATH, TEST_DATA_FOLDER_NAME)
TEST_DIRECTIVE_FILE_PATH = os.path.join(TEST_DIRECTIVE_FILE_PATH, "test_content_type_directive.xml")

EXTENSIONS = ('.doc',
              '.DOC', 
              '.docx',
              '.DOCX', 
              '.xls',
              '.XLS', 
              '.xlsx',
              '.XLSX', 
              '.ppt',
              '.PPT', 
              '.pptx',
              '.PPTX', 
              '.pdf',
              '.PDF',
              '.odt',
              '.ODT', 
              '.mp3',
              '.MP3', 
              '.tif',
              '.TIF', 
              '.tiff',
              '.TIFF', 
              '.jpg',
              '.JPG', 
              '.jpeg',
              '.JPEG', 
              '.png',
              '.PNG', 
              '.txt',
              '.TXT', 
              '.md',
              '.MD', 
              '.csv',
              '.CSV',
              '.css',
              '.CSS', 
              '.htm',
              '.HTM', 
              '.html',
              '.HTML', 
              '.avi',
              '.AVI')

class TestFiler(unittest.TestCase):
    
    def setUp(self):
        self.test_source_folder_path = tempfile.mkdtemp(suffix='', prefix="descatter_test_src_", dir=None)
        self.test_destination_folder_path = tempfile.mkdtemp(suffix='', prefix='descatter_test_dst_', dir=None)
        self.test_filer = organize.Filer(self.test_destination_folder_path, organize.Directive(TEST_DIRECTIVE_FILE_PATH))
        self.test_source_file_paths = []

        for extension in EXTENSIONS:
            test_file_handle, test_source_file_path = tempfile.mkstemp(suffix=extension, prefix='descatter_test_file_', dir=self.test_source_folder_path, text=False)
            test_file = os.fdopen(test_file_handle, 'w')
            test_file.close()
            
            self.test_source_file_paths.append(test_source_file_path)
            
        # TODO: Create subfolder structure to test deep filing function.
        
#     def tearDown(self):
#         shutil.rmtree(self.test_source_folder_path)
#         shutil.rmtree(self.test_destination_folder_path)
        
#     def test_file_file(self):
#         self.test_filer.file_file(self.test_source_file_paths[0])
        
        # TODO: Change to using string of XML instead of file
        # TODO: Add check for file copied to appropriate destination
        
#     def test_file_list(self):
#         self.test_filer.file_list(self.test_source_file_paths)
    
#     def test_file_folder(self):
#         self.test_filer.file_folder(self.test_source_folder_path, deep=False)

    def test_filer_folder_deep(self):
        self.test_filer.file_folder(self.test_source_folder_path, True)