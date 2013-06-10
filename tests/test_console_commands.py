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
        cls.test_catalog_path = os.path.join(cls.test_temp_folder, "Test_Catalog")
        cls.test_catalog = establish(cls.test_catalog_path)
    
    @classmethod
    def tearDownClass(cls):             
        destroy(cls.test_catalog_path, True)
        shutil.rmtree(cls.test_temp_folder)
    
    def test_input(self):
        console = Console()
        
        input_value = self.test_catalog_path
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)
        
    def test_input_verbose(self):
        console = Console()
        
        input_value = self.test_catalog_path + ' ' + constants.COMMAND_SHORT_PREFIX + constants.VERBOSE_ARGUMENT_SHORT_NAME
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)
        
    def test_argument_long_name_input(self):
        console = Console()
        
        input_value = constants.COMMAND_LONG_PREFIX + constants.CATALOG_ARGUMENT_LONG_NAME + ' ' + self.test_catalog_path
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)

    def test_argument_short_name_input(self):
        console = Console()
        
        input_value = constants.COMMAND_SHORT_PREFIX + constants.CATALOG_ARGUMENT_SHORT_NAME + ' ' + self.test_catalog_path
        console.do_catalog(input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)
    
    def test_no_input(self):
        console = Console()
        
        input_value = self.test_catalog_path
        console.do_catalog('', lambda input: input_value)
        output = console.current_working_catalog.path
        self.assertEqual(output, self.test_catalog_path)