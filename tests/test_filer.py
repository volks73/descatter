import os
import unittest
import tempfile
import shutil

import organize

TESTS_FOLDER_NAME = 'tests'
TESTS_DATA_FOLDER_NAME = 'data'
TESTS_DATA_FOLDER_PATH = os.path.join(os.path.join(os.getcwd(), TESTS_FOLDER_NAME), TESTS_DATA_FOLDER_NAME)

class TestFileFile(unittest.TestCase):
    
    def setUp(self):
        self.test_source_folder_path = tempfile.mkdtemp(suffix='', prefix="descatter_TestFileFile_src_", dir=None)
        self.test_destination_folder_path = tempfile.mkdtemp(suffix='', prefix='descatter_TestFileFile_dst_', dir=None)
        directive_path_TestFileFile = os.path.join(TESTS_DATA_FOLDER_PATH, "test_directive_TestFileFile.xml")
        self.test_filer = organize.Filer(self.test_destination_folder_path, organize.Directive(directive_path_TestFileFile))

    def tearDown(self):
        shutil.rmtree(self.test_source_folder_path)
        shutil.rmtree(self.test_destination_folder_path)
        
    def test_without_extension(self):
        test_file_handle, test_source_file_path = tempfile.mkstemp(suffix='', prefix='descatter_TestFileFile_', dir=self.test_source_folder_path, text=False)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.close()
        
        expected_filed_path = os.path.join(self.test_destination_folder_path, os.path.basename(test_source_file_path))
        
        output_value = self.test_filer.file_file(test_source_file_path)
        
        self.assertEquals(output_value, expected_filed_path)
        self.assertTrue(os.path.exists(expected_filed_path))

    def test_with_extension(self):
        test_file_handle, test_source_file_path = tempfile.mkstemp(suffix='.txt', prefix='descatter_TestFileFile_', dir=self.test_source_folder_path, text=True)
        test_file = os.fdopen(test_file_handle, 'w')
        test_file.close()
        
        expected_filed_path = os.path.join(self.test_destination_folder_path, os.path.basename(test_source_file_path))
        
        output_value = self.test_filer.file_file(test_source_file_path)
        
        self.assertEquals(output_value, expected_filed_path)
        self.assertTrue(os.path.exists(expected_filed_path))

class TestFileList(unittest.TestCase):
    
    def setUp(self):
        self.test_source_folder_path = tempfile.mkdtemp(suffix='', prefix="descatter_TestFileFile_src_", dir=None)
        self.test_destination_folder_path = tempfile.mkdtemp(suffix='', prefix='descatter_TestFileFile_dst_', dir=None)
        directive_path_TestFileFile = os.path.join(TESTS_DATA_FOLDER_PATH, "test_directive_TestFileFile.xml")
        self.test_filer = organize.Filer(self.test_destination_folder_path, organize.Directive(directive_path_TestFileFile))

    def tearDown(self):
        shutil.rmtree(self.test_source_folder_path)
        shutil.rmtree(self.test_destination_folder_path)
    
    def test_without_extensions(self):
        test_source_file_paths = []        
        for index in range(10):
            prefix = 'descatter_TestFileList_' + str(index) + '_'
            test_file_handle, test_source_file_path = tempfile.mkstemp(suffix='', prefix=prefix, dir=self.test_source_folder_path, text=False)
            test_file = os.fdopen(test_file_handle, 'w')
            test_file.close()
            
            test_source_file_paths.append(test_source_file_path)
            
        expected_filed_paths = []
        for file_path in test_source_file_paths:
            expected_filed_paths.append(os.path.join(self.test_destination_folder_path, os.path.basename(file_path)))
        
        output_value = self.test_filer.file_list(test_source_file_path)
        
        for index, value in enumerate(output_value):
            self.assertEquals(output_value, expected_filed_paths[index])
            self.assertTrue(os.path.exists(expected_filed_paths[index]))
    
    def test_with_extensions(self):
        test_source_file_paths = []        
        for index in range(10):
            prefix = 'descatter_TestFileList_' + str(index) + '_'
            test_file_handle, test_source_file_path = tempfile.mkstemp(suffix='.txt', prefix=prefix, dir=self.test_source_folder_path, text=True)
            test_file = os.fdopen(test_file_handle, 'w')
            test_file.close()
            
            test_source_file_paths.append(test_source_file_path)
            
        expected_filed_paths = []
        for file_path in test_source_file_paths:
            expected_filed_paths.append(os.path.join(self.test_destination_folder_path, os.path.basename(file_path)))
        
        output_value = self.test_filer.file_list(test_source_file_path)
        
        for index, value in enumerate(output_value):
            self.assertEquals(output_value, expected_filed_paths[index])
            self.assertTrue(os.path.exists(expected_filed_paths[index]))

class TestFileFolder(unittest.TestCase):
    
    EXTENSIONS = ('.doc', 
              '.docx', 
              '.xls',
              '.xlsx', 
              '.ppt',
              '.pptx', 
              '.pdf',
              '.odt', 
              '.mp3', 
              '.tif', 
              '.tiff', 
              '.jpg',
              '.jpeg', 
              '.png',
              '.svg',
              '.txt', 
              '.md',
              '.csv',
              '.css', 
              '.htm', 
              '.html', 
              '.avi')
    
    def setUp(self):
        self.test_source_folder_path = tempfile.mkdtemp(suffix='', prefix="descatter_TestFileFolder_src_", dir=None)
        self.test_destination_folder_path = tempfile.mkdtemp(suffix='', prefix='descatter_TestFileFolder_dst_', dir=None)
        directive_path_TestFileFile = os.path.join(TESTS_DATA_FOLDER_PATH, "test_directive_TestFileFolder.xml")
        self.test_filer = organize.Filer(self.test_destination_folder_path, organize.Directive(directive_path_TestFileFile))

        self.test_source_file_paths = []

        for extension in self.EXTENSIONS:
            prefix = 'descatter_TestFileFolder_'
            test_file_handle, test_source_file_path = tempfile.mkstemp(suffix=extension, prefix=prefix, dir=self.test_source_folder_path, text=False)
            test_file = os.fdopen(test_file_handle, 'w')
            test_file.close()
            
            self.test_source_file_paths.append(test_source_file_path)
        
        for index in range(10):
            folder_name = "subFolder" + str(index)
            folder_path = os.path.join(self.test_source_folder_path, folder_name)
            os.mkdir(folder_path)
            
            for extension in self.EXTENSIONS:
                prefix = 'descatter_TestFileFolder_' + folder_name + '_'
                test_file_handle, test_source_file_path = tempfile.mkstemp(suffix=extension, prefix=prefix, dir=folder_path, text=False)
                test_file = os.fdopen(test_file_handle, 'w')
                test_file.close()
                
                self.test_source_file_paths.append(test_source_file_path)
                
            level_2_subfolder_path = os.path.join(folder_path, "subFolder")
            os.mkdir(level_2_subfolder_path)
            
            for extension in self.EXTENSIONS:
                prefix = 'descatter_TestFileFolder_' + folder_name + '_2level_'
                test_file_handle, test_source_file_path = tempfile.mkstemp(suffix=extension, prefix=prefix, dir=level_2_subfolder_path, text=False)
                test_file = os.fdopen(test_file_handle, 'w')
                test_file.close()
                
                self.test_source_file_paths.append(test_source_file_path)

    def tearDown(self):
        shutil.rmtree(self.test_source_folder_path)
        shutil.rmtree(self.test_destination_folder_path)

    def test_not_deep(self):
        output_value = self.test_filer.file_folder(self.test_source_folder_path, False)
        
        expected_filed_paths = []
        for file_path in self.test_source_file_paths:
            expected_filed_paths.append(os.path.join(self.test_destination_folder_path, os.path.basename(file_path)))
        
        for index, value in enumerate(output_value):
            self.assertTrue(os.path.exists(expected_filed_paths[index]))
    
        number_filed = len(os.listdir(self.test_destination_folder_path))
        self.assertEquals(len(output_value), number_filed)
    
    def test_deep(self):
        output_value = self.test_filer.file_folder(self.test_source_folder_path, True)
        
        expected_filed_paths = []
        for file_path in self.test_source_file_paths:
            expected_filed_paths.append(os.path.join(self.test_destination_folder_path, os.path.basename(file_path)))
        
        for index, value in enumerate(output_value):
            self.assertTrue(os.path.exists(expected_filed_paths[index]))