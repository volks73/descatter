from interface import Console

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
        
    def test_preset_catalog(self):
        console = Console()
           
        console.do_catalog(self.test_catalog_path)
           
        input_value = ('%s') % self.test_temp_file1.name
        catalog_input = input
        file_paths_input = input
        title_input = lambda title_input: "Test Temp File1"
        expected_original_path = os.path.dirname(self.test_temp_file1.name)
        expected_original_name = os.path.basename(self.test_temp_file1.name)
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
          
        input_value = ('%s ' + constants.COMMAND_SHORT_PREFIX + constants.CATALOG_ARGUMENT_SHORT_NAME + ' %s') % (self.test_temp_file1.name, self.test_catalog_path)
        catalog_input = input
        file_paths_input = input
        title_input = lambda title_input: "Test Temp File1"
        expected_original_path = os.path.dirname(self.test_temp_file1.name)
        expected_original_name = os.path.basename(self.test_temp_file1.name)
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
        file_paths_input = lambda file_path_input: self.test_temp_file1.name
        title_input = lambda title_input: "Test Temp File1"
        expected_original_path = os.path.dirname(self.test_temp_file1.name)
        expected_original_name = os.path.basename(self.test_temp_file1.name)
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
        
        input_value = ('%s' + constants.LIST_SEPARATOR + '%s' + constants.LIST_SEPARATOR + '%s') % (self.test_temp_file1.name, self.test_temp_file2.name, self.test_temp_file3.name)
        catalog_input = input
        file_paths_input = lambda file_path_input: self.test_temp_file1.name
        title_input = lambda title_input: "Test Title"
        expected_original_path = os.path.dirname(self.test_temp_file3.name)
        expected_original_name = os.path.basename(self.test_temp_file3.name)
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