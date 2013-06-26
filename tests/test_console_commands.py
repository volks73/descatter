from interface import Console
from interface import InputError
from catalog import CatalogError

import unittest
import tempfile
import shutil
import os

import constants
import catalog

class TestCatalogCommand(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_temp_folder = tempfile.mkdtemp()
        cls.test_catalog_path = os.path.join(cls.test_temp_folder, "Catalog_Test_Catalog")
        cls.test_catalog = catalog.create(cls.test_catalog_path)
    
    @classmethod
    def tearDownClass(cls):             
        cls.test_catalog.session.close_all()
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

class TestEstablishCommand(unittest.TestCase):
    
    def setUp(self):
        self.test_temp_folder = tempfile.mkdtemp()
        self.test_catalog_path = os.path.join(self.test_temp_folder, "Establish_Test_Catalog")
    
    def tearDown(self):
        shutil.rmtree(self.test_temp_folder)
    
    def test_no_arguments(self):
        console = Console()
        
        input_value = ''
        
        console.do_establish(input_value, lambda path_input: self.test_catalog_path)
        self.assertEqual(console.current_working_catalog.path, self.test_catalog_path)
        
    def test_path_argument(self):
        console = Console()
        
        input_value = self.test_catalog_path
        
        console.do_establish(input_value, input)
        self.assertEqual(console.current_working_catalog.path, self.test_catalog_path)
    
    def test_schema_argument(self):
        console = Console()
        
        data_folder_path = os.path.join(constants.APPLICATION_NAME, constants.DATA_FOLDER_NAME)
        schema_file_path = os.path.join(os.getcwd(), data_folder_path)
        schema_file_path = os.path.join(schema_file_path, 'content_type_schema.xml')
        
        input_value = self.test_catalog_path + ' ' + constants.SCHEMA_ARGUMENT_SHORT_NAME + ' ' + schema_file_path
        
        console.do_establish(input_value, input)
        self.assertEqual(console.current_working_catalog.path, self.test_catalog_path)

class TestDestroyCommand(unittest.TestCase):
    
    def setUp(self):
        self.test_temp_folder = tempfile.mkdtemp()
        self.test_catalog_path = os.path.join(self.test_temp_folder, "Destroy_Test_Catalog")
        self.test_catalog = catalog.create(self.test_catalog_path)
    
    def tearDown(self):
        self.test_catalog.session.close_all()
        shutil.rmtree(self.test_temp_folder)
    
    def test_no_arguments(self):
        console = Console()
        
        input_value = ''
        catalog_path_input = lambda catalog_path_input: self.test_catalog_path
        yes_or_no_input = lambda yes_or_not_input: 'y'
        
        console.do_destroy(input_value, catalog_path_input, yes_or_no_input)
        self.assertFalse(os.path.exists(self.test_catalog_path))
    
    def test_path_arguments(self):
        console = Console()
        
        input_value = self.test_catalog_path
        catalog_path_input = input
        yes_or_no_input = lambda yes_or_not_input: 'y'
        
        console.do_destroy(input_value, catalog_path_input, yes_or_no_input)
        self.assertFalse(os.path.exists(self.test_catalog_path))

class TestCheckinCommand(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_temp_folder = tempfile.mkdtemp()
        cls.test_catalog_path = os.path.join(cls.test_temp_folder, "Checkin_Test_Catalog")
        cls.test_catalog = catalog.create(cls.test_catalog_path)
    
    @classmethod
    def tearDownClass(cls):
        cls.test_catalog.session.close_all()
        shutil.rmtree(cls.test_temp_folder)
    
    def setUp(self):
        test_temp_file1, self.test_temp_file1_path = tempfile.mkstemp(suffix='.txt', text=True)
        test_temp_file2, self.test_temp_file2_path = tempfile.mkstemp(suffix='.txt', text=True)
        test_temp_file3, self.test_temp_file3_path = tempfile.mkstemp(suffix='.txt', text=True)
        
        os.close(test_temp_file1)
        os.close(test_temp_file2)
        os.close(test_temp_file3)
    
    def tearDown(self):
        os.remove(self.test_temp_file1_path)
        os.remove(self.test_temp_file2_path)
        os.remove(self.test_temp_file3_path)
        
    def test_preset_catalog(self):
        console = Console()
           
        console.do_catalog(self.test_catalog_path)
           
        input_value = ('%s') % self.test_temp_file1_path
        catalog_input = input
        file_paths_input = input
        title_input = lambda title_input: "Test Temp File1"
        expected_original_path = os.path.dirname(self.test_temp_file1_path)
        expected_original_name = os.path.basename(self.test_temp_file1_path)
        expected_title = "Test Temp File1"
           
        console.do_checkin(input_value, catalog_input, file_paths_input, title_input)
        output_catalog_file = console.current_working_file
          
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)
         
    def test_catalog_argument(self):
        console = Console()
          
        input_value = ('%s ' + 
                       constants.COMMAND_SHORT_PREFIX + 
                       constants.CATALOG_ARGUMENT_SHORT_NAME + 
                       ' %s') % (self.test_temp_file1_path, self.test_catalog_path)
        catalog_input = input
        file_paths_input = input
        title_input = lambda title_input: "Test Temp File1"
        expected_original_path = os.path.dirname(self.test_temp_file1_path)
        expected_original_name = os.path.basename(self.test_temp_file1_path)
        expected_title = "Test Temp File1"
          
        console.do_checkin(input_value, catalog_input, file_paths_input, title_input)
        output_catalog_file = console.current_working_file
         
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)
     
    def test_no_file(self):
        console = Console()
         
        console.do_catalog(self.test_catalog_path) 
          
        input_value = ''
        catalog_input = input
        file_paths_input = lambda file_path_input: self.test_temp_file1_path
        title_input = lambda title_input: "Test Temp File1"
        expected_original_path = os.path.dirname(self.test_temp_file1_path)
        expected_original_name = os.path.basename(self.test_temp_file1_path)
        expected_title = "Test Temp File1"
          
        console.do_checkin(input_value, catalog_input, file_paths_input, title_input)
        output_catalog_file = console.current_working_file
         
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)
    
    def test_file_list(self):
        console = Console()
        
        console.do_catalog(self.test_catalog_path)
        
        input_value = ('%s' + 
                       constants.LIST_SEPARATOR + 
                       '%s' + 
                       constants.LIST_SEPARATOR + 
                       '%s') % (
                                self.test_temp_file1_path, 
                                self.test_temp_file2_path, 
                                self.test_temp_file3_path)
        catalog_input = input
        file_paths_input = lambda file_path_input: self.test_temp_file1_path
        title_input = lambda title_input: "Test Title"
        expected_original_path = os.path.dirname(self.test_temp_file3_path)
        expected_original_name = os.path.basename(self.test_temp_file3_path)
        expected_title = "Test Title"
         
        console.do_checkin(input_value, catalog_input, file_paths_input, title_input)
        output_catalog_file = console.current_working_file
        
        self.assertEqual(output_catalog_file.original_path, expected_original_path)
        self.assertEqual(output_catalog_file.original_name, expected_original_name)
        self.assertEqual(output_catalog_file.title, expected_title)
        self.assertIsNotNone(output_catalog_file.id)
        self.assertIsNotNone(output_catalog_file.content_name)
        self.assertIsNotNone(output_catalog_file.content_path)
        self.assertTrue(output_catalog_file.content_name)
        self.assertTrue(output_catalog_file.content_path)

class TestCheckoutCommand(unittest.TestCase):             
    
    def setUp(self):
        self.test_temp_folder = tempfile.mkdtemp()
        self.test_catalog_path = os.path.join(self.test_temp_folder, "Checkout_Test_Catalog")
        self.test_catalog = catalog.create(self.test_catalog_path)
        
        test_temp_file1, self.test_temp_file1_path = tempfile.mkstemp(suffix='.txt', text=True)
        test_temp_file2, self.test_temp_file2_path = tempfile.mkstemp(suffix='.txt', text=True)
        test_temp_file3, self.test_temp_file3_path = tempfile.mkstemp(suffix='.txt', text=True)
        
        os.close(test_temp_file1)
        os.close(test_temp_file2)
        os.close(test_temp_file3)
        
        self.test_temp_file1 = self.test_catalog.checkin(self.test_temp_file1_path)
        self.test_temp_file2 = self.test_catalog.checkin(self.test_temp_file2_path)
        self.test_temp_file3 = self.test_catalog.checkin(self.test_temp_file3_path)
        
        os.remove(self.test_temp_file1_path)
        os.remove(self.test_temp_file2_path)
        os.remove(self.test_temp_file3_path)
    
    def tearDown(self):
        self.test_catalog.session.close_all()
        shutil.rmtree(self.test_temp_folder)
        
    def test_preset_catalog(self):
        console = Console()
           
        console.do_catalog(self.test_catalog_path)
           
        input_value = '1'
        catalog_input = input
        file_ids_input = input
           
        console.do_checkout(input_value, catalog_input, file_ids_input)
        self.assertTrue(os.path.exists(self.test_temp_file1_path))
         
    def test_catalog_argument(self):
        console = Console()
          
        input_value = ('1 ' + 
                       constants.COMMAND_SHORT_PREFIX + 
                       constants.CATALOG_ARGUMENT_SHORT_NAME + 
                       ' %s') % self.test_catalog_path
        catalog_input = input
        file_ids_input = input
          
        console.do_checkout(input_value, catalog_input, file_ids_input)
        self.assertTrue(os.path.exists(self.test_temp_file1_path))
    
    def test_file_id(self):
        console = Console()
         
        console.do_catalog(self.test_catalog_path) 
          
        input_value = '1'
        catalog_input = input
        file_ids_input = lambda file_path_input: self.test_temp_file1_path
          
        console.do_checkout(input_value, catalog_input, file_ids_input)
        self.assertTrue(os.path.exists(self.test_temp_file1_path))
        
    def test_padded_file_id(self):
        console = Console()
         
        console.do_catalog(self.test_catalog_path) 
          
        input_value = ' 1 '
        catalog_input = input
        file_ids_input = lambda file_path_input: self.test_temp_file1_path
          
        console.do_checkout(input_value, catalog_input, file_ids_input)
        self.assertTrue(os.path.exists(self.test_temp_file1_path))        
        
    def test_empty(self):
        console = Console()
         
        console.do_catalog(self.test_catalog_path) 
          
        input_value = ''
        catalog_input = input
        file_ids_input = lambda file_path_input: self.test_temp_file1_path
          
        console.do_checkout(input_value, catalog_input, file_ids_input)
        self.assertTrue(os.path.exists(self.test_temp_file1_path))
    
    def test_no_file_found(self):
        console = Console()
        
        console.do_catalog(self.test_catalog_path) 
          
        input_value = '123456789'
        catalog_input = input
        file_ids_input = input
        self.assertRaises(CatalogError, console.do_checkout, input_value)
    
    def test_file_id_list(self):
        console = Console()
        
        console.do_catalog(self.test_catalog_path)
        
        input_value = '1' + constants.LIST_SEPARATOR + '2' + constants.LIST_SEPARATOR + '3'
        catalog_input = input
        file_ids_input = input
        
        console.do_checkout(input_value, catalog_input, file_ids_input)
        self.assertTrue(os.path.exists(self.test_temp_file1_path))
        self.assertTrue(os.path.exists(self.test_temp_file2_path))
        self.assertTrue(os.path.exists(self.test_temp_file3_path))
        
    def test_padded_file_id_list(self):
        console = Console()
        
        console.do_catalog(self.test_catalog_path)
        
        input_value = ' 1 ' + constants.LIST_SEPARATOR + ' 2 ' + constants.LIST_SEPARATOR + ' 3 '
        catalog_input = input
        file_ids_input = input
        
        console.do_checkout(input_value, catalog_input, file_ids_input)
        self.assertTrue(os.path.exists(self.test_temp_file1_path))
        self.assertTrue(os.path.exists(self.test_temp_file2_path))
        self.assertTrue(os.path.exists(self.test_temp_file3_path))