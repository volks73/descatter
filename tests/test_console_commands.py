from interface import Console
from catalog import establish
from catalog import destroy

import unittest
import tempfile
import shutil
import os

import constants

class TestCatalogCommand(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_temp_folder = tempfile.mkdtemp()
        cls.test_catalog_path = os.path.join(cls.test_temp_folder, "Catalog_Test_Catalog")
        cls.test_catalog = establish(cls.test_catalog_path)
    
    @classmethod
    def tearDownClass(cls):             
        destroy(cls.test_catalog_path, True)
        shutil.rmtree(cls.test_temp_folder)
    
    def test_input(self):
        console = Console()
        
        input_value = ('%s') % self.test_catalog_path
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)
        
    def test_input_verbose(self):
        console = Console()
        
        input_value = ('%s ' + constants.COMMAND_SHORT_PREFIX + constants.VERBOSE_ARGUMENT_SHORT_NAME) % self.test_catalog_path
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)
        
    def test_argument_long_name_input(self):
        console = Console()
        
        input_value = (constants.COMMAND_LONG_PREFIX + constants.CATALOG_ARGUMENT_LONG_NAME + ' %s') % self.test_catalog_path
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)

    def test_argument_short_name_input(self):
        console = Console()
        
        input_value = (constants.COMMAND_SHORT_PREFIX + constants.CATALOG_ARGUMENT_SHORT_NAME + ' %s') % self.test_catalog_path
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)
    
    def test_no_input(self):
        console = Console()
        
        input_value = '%s' % self.test_catalog_path
        console.do_catalog('', lambda input: input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)

class TestCheckinCommand(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_temp_folder = tempfile.mkdtemp()
        cls.test_catalog_path = os.path.join(cls.test_temp_folder, "Checkin_Test_Catalog")
        cls.test_catalog = establish(cls.test_catalog_path)
    
    @classmethod
    def tearDownClass(cls):
        destroy(cls.test_catalog_path, True)
        
        try:
            shutil.rmtree(cls.test_temp_folder)
        except IOError:
            pass
        except PermissionError:
            pass
    
    def setUp(self):
        self.test_temp_file1 = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        self.test_temp_file2 = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        self.test_temp_file3 = tempfile.NamedTemporaryFile(suffix='.txt', delete=False)
        
        self.test_temp_file1.close()
        self.test_temp_file2.close()
        self.test_temp_file3.close()
    
    def tearDown(self):
        os.remove(self.test_temp_file1.name)
        os.remove(self.test_temp_file2.name)
        os.remove(self.test_temp_file3.name)
        
    def test_checkin_file_preset_catalog(self):
        console = Console()
           
        console.do_catalog(self.test_catalog_path)
           
        input_value = ('%s') % self.test_temp_file1.name
        expected_original_path = os.path.dirname(self.test_temp_file1.name)
        expected_original_name = os.path.basename(self.test_temp_file1.name)
        expected_title = "Test Temp File1"
           
        console.do_checkin(input_value, (input, lambda title_input: "Test Temp File1"))
        output_catalog_file = console.current_working_file
          
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)
         
    def test_checkin_file_catalog_short_argument(self):
        console = Console()
          
        input_value = ('%s ' + constants.COMMAND_SHORT_PREFIX + constants.CATALOG_ARGUMENT_SHORT_NAME + ' %s') % (self.test_temp_file1.name, self.test_catalog_path)
        expected_original_path = os.path.dirname(self.test_temp_file1.name)
        expected_original_name = os.path.basename(self.test_temp_file1.name)
        expected_title = "Test Temp File1"
          
        console.do_checkin(input_value, (input, lambda title_input: "Test Temp File1"))
        output_catalog_file = console.current_working_file
         
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)
         
    def test_checkin_file_catalog_long_argument(self):
        console = Console()
          
        input_value = ('%s ' + constants.COMMAND_LONG_PREFIX + constants.CATALOG_ARGUMENT_LONG_NAME + ' %s') % (self.test_temp_file1.name, self.test_catalog_path)
        expected_original_path = os.path.dirname(self.test_temp_file1.name)
        expected_original_name = os.path.basename(self.test_temp_file1.name)
        expected_title = "Test Temp File1"
          
        console.do_checkin(input_value, (input, lambda title_input: "Test Temp File1"))
        output_catalog_file = console.current_working_file
         
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)
     
    def test_checkin_no_file(self):
        console = Console()
         
        console.do_catalog(self.test_catalog_path) 
          
        input_value = ''
        expected_original_path = os.path.dirname(self.test_temp_file1.name)
        expected_original_name = os.path.basename(self.test_temp_file1.name)
        expected_title = "Test Temp File1"
          
        console.do_checkin(input_value, (lambda file_path_input: self.test_temp_file1.name, lambda title_input: "Test Temp File1"))
        output_catalog_file = console.current_working_file
         
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)
    
    def test_checkin_file_list(self):
        console = Console()
        
        console.do_catalog(self.test_catalog_path)
        
        input_value = ('%s' + constants.LIST_SEPARATOR + '%s' + constants.LIST_SEPARATOR + '%s') % (self.test_temp_file1.name, self.test_temp_file2.name, self.test_temp_file3.name)
        expected_original_path = os.path.dirname(self.test_temp_file3.name)
        expected_original_name = os.path.basename(self.test_temp_file3.name)
        expected_title = "Test Title"
         
        console.do_checkin(input_value, (input, lambda title_input: "Test Title"))
        output_catalog_file = console.current_working_file
        
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)

class TestEstablishCommand(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_temp_folder = tempfile.mkdtemp()
        cls.test_catalog_path = os.path.join(cls.test_temp_folder, "Establish_Test_Catalog")
    
    @classmethod
    def tearDownClass(cls):
        try:
            shutil.rmtree(cls.test_temp_folder)
        except IOError:
            pass
        except PermissionError:
            pass
    
    def test_establish_no_arguments(self):
        pass
    
    def test_establish_path_argument(self):
        pass
    
    def test_establish_path_argument_with_forward_slashes(self):
        pass
    
    def test_establish_path_argument_with_back_slashes(self):
        pass
    
    def test_establish_with_schema_argument(self):
        pass