from interface import Console
from catalog import establish
from catalog import destroy

import os
import tempfile
import shutil
import unittest

import constants

class TestSanitizeUserInput(unittest.TestCase):
    
    def test_input(self):
        console = Console()
        
        expected_value = "test input"
        
        output = console.sanitize_user_input("test input")
        self.assertEqual(output, expected_value)
        
    def test_left_padded_input(self):
        console = Console()
        
        expected_value = "test input"
        
        output = console.sanitize_user_input(" test input")
        self.assertEqual(output, expected_value)
        
    def test_right_padded_input(self):
        console = Console()
        
        expected_value = "test input"
        
        output = console.sanitize_user_input("test input ")
        self.assertEqual(output, expected_value)
        
    def test_padded_input(self):
        console = Console()
        
        expected_value = "test input"
        
        output = console.sanitize_user_input(" test input ")
        self.assertEqual(output, expected_value)
    
    def test_case_sensitive_input(self):
        console = Console()
        
        expected_value = "Test INPUT"
        
        output = console.sanitize_user_input("Test INPUT")
        self.assertEqual(output, expected_value)
    
    def test_none(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_user_input, None)
        
    def test_empty(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_user_input, '')

class TestSanitizeYesOrNoInput(unittest.TestCase):
    
    def test_yes(self):
        console = Console()
        
        output = console.sanitize_yes_or_no_input("yes")
        self.assertTrue(output)
        
        output = console.sanitize_yes_or_no_input("y")
        self.assertTrue(output)
    
    def test_padded_yes(self):
        console = Console()
    
        output = console.sanitize_yes_or_no_input("yes ")
        self.assertTrue(output)
    
        output = console.sanitize_yes_or_no_input(" yes")
        self.assertTrue(output)
    
        output = console.sanitize_yes_or_no_input(" yes ")
        self.assertTrue(output)
        
        output = console.sanitize_yes_or_no_input("y ")
        self.assertTrue(output)
        
        output = console.sanitize_yes_or_no_input(" y")
        self.assertTrue(output)
        
        output = console.sanitize_yes_or_no_input(" y ")
        self.assertTrue(output)
        
    def test_case_sensitive_yes(self):
        console = Console()
        
        output = console.sanitize_yes_or_no_input("Yes")
        self.assertTrue(output)
        
        output = console.sanitize_yes_or_no_input("YEs")
        self.assertTrue(output)
        
        output = console.sanitize_yes_or_no_input("YES")
        self.assertTrue(output)
        
        output = console.sanitize_yes_or_no_input("Y")
        self.assertTrue(output)
        
    def test_no(self):
        console = Console()
        
        output = console.sanitize_yes_or_no_input("no")
        self.assertFalse(output)
        
        output = console.sanitize_yes_or_no_input("n")
        self.assertFalse(output)
    
    def test_padded_no(self):
        console = Console()
    
        output = console.sanitize_yes_or_no_input("no ")
        self.assertFalse(output)
    
        output = console.sanitize_yes_or_no_input(" no")
        self.assertFalse(output)
    
        output = console.sanitize_yes_or_no_input(" no ")
        self.assertFalse(output)
        
        output = console.sanitize_yes_or_no_input("n ")
        self.assertFalse(output)
        
        output = console.sanitize_yes_or_no_input(" n")
        self.assertFalse(output)
        
        output = console.sanitize_yes_or_no_input(" n ")
        self.assertFalse(output)
    
    def test_case_sensitive_no(self):
        console = Console()
        
        output = console.sanitize_yes_or_no_input("No")
        self.assertFalse(output)
        
        output = console.sanitize_yes_or_no_input("NO")
        self.assertFalse(output)
        
        output = console.sanitize_yes_or_no_input("N")
        self.assertFalse(output)
    
    def test_unacceptable(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_yes_or_no_input, "maybe")
        
    def test_empty(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_yes_or_no_input, '')
        
    def test_none(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_yes_or_no_input, None)

class TestSanitizeCatalogPathInput(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.test_temp_folder = tempfile.mkdtemp()
        cls.test_catalog_path = os.path.join(cls.test_temp_folder, "Test_Catalog")
        cls.test_catalog = establish(cls.test_catalog_path)
    
    @classmethod
    def tearDownClass(cls):             
        destroy(cls.test_catalog_path, True)
        shutil.rmtree(cls.test_temp_folder)
    
    def test_input_catalog_path(self):
        console = Console()
        
        output = console.sanitize_catalog_path_input(self.test_catalog_path)
        self.assertEqual(output, self.test_catalog_path)
        
    def test_input_not_catalog_path(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_catalog_path_input, "test_not_catalog_path")
    
    def test_empty(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_catalog_path_input, '')
        
    def test_none(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_catalog_path_input, None)

class TestSanitizeFilePathsInput(unittest.TestCase):
        
    def test_relative_path(self):
        console = Console()
        
        expected_value = (os.path.join(os.getcwd(), "CHANGES.txt"),)
        
        output = console.sanitize_file_paths_input("CHANGES.txt")
        self.assertEqual(output, expected_value)
    
    def test_padded_relative_path(self):
        console = Console()
        
        expected_value = (os.path.join(os.getcwd(), "CHANGES.txt"),)
        
        output = console.sanitize_file_paths_input(" CHANGES.txt")
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_file_paths_input("CHANGES.txt ")
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_file_paths_input(" CHANGES.txt ")
        self.assertEqual(output, expected_value)
    
    def test_relative_path_lists(self):
        console = Console()
        
        expected_value = (os.path.join(os.getcwd(), "CHANGES.txt"),
                           os.path.join(os.getcwd(), "LICENSE.txt"),
                           os.path.join(os.getcwd(), "README.md"))
        
        input_value = ("CHANGES.txt" + 
                            constants.LIST_SEPARATOR + 
                            " LICENSE.txt" +
                            constants.LIST_SEPARATOR +
                            " README.md")
                
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded_relative_path_list(self):
        console = Console()
        
        expected_value = (os.path.join(os.getcwd(), "CHANGES.txt"),
                           os.path.join(os.getcwd(), "LICENSE.txt"),
                           os.path.join(os.getcwd(), "README.md"))
        
        input_value = (" CHANGES.txt" + 
                            constants.LIST_SEPARATOR + 
                            " LICENSE.txt" +
                            constants.LIST_SEPARATOR +
                            " README.md")
                
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ("CHANGES.txt " + 
                            constants.LIST_SEPARATOR + 
                            "LICENSE.txt " +
                            constants.LIST_SEPARATOR +
                            "README.md ")
                
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)

        input_value = (" CHANGES.txt " + 
                            constants.LIST_SEPARATOR + 
                            " LICENSE.txt " +
                            constants.LIST_SEPARATOR +
                            " README.md ")
                
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)

    def test_absolute_path(self):
        console = Console()
        
        expected_value = (os.path.join(os.getcwd(), "CHANGES.txt"), )
        input_value = os.path.join(os.getcwd(), "CHANGES.txt")
        
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_absolute_path_list(self):
        console = Console()
        
        expected_value = (os.path.join(os.getcwd(), "CHANGES.txt"),
                           os.path.join(os.getcwd(), "LICENSE.txt"),
                           os.path.join(os.getcwd(), "README.md"))
        
        input_value = (os.path.join(os.getcwd(), "CHANGES.txt") + 
                            constants.LIST_SEPARATOR +
                            os.path.join(os.getcwd(), "LICENSE.txt") + 
                            constants.LIST_SEPARATOR +
                            os.path.join(os.getcwd(), "README.md"))
        
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_not_file_path(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_file_paths_input, "NotAFile.txt")
    
    def test_not_file_path_list(self):
        console = Console()
        
        input_values = ("NotAFile1.txt" +
                            constants.LIST_SEPARATOR +
                            "NotAFile2.txt" +
                            constants.LIST_SEPARATOR +
                            "NotAFile3.txt")
        
        self.assertRaises(ValueError, console.sanitize_file_paths_input, input_values)
    
    def test_empty(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_file_paths_input, '')
        
    def test_none(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_file_paths_input, None)

class TestSanitizeCatalogFileIdsInput(unittest.TestCase):
    
    def test_catalog_file_id(self):
        console = Console()
        
        expected_value = ('1',)
        
        output = console.sanitize_catalog_file_ids_input('1')
        self.assertEqual(output, expected_value)
    
    def test_padded_catalog_file_id(self):
        console = Console()
        
        expected_value = ('1',)
        
        output = console.sanitize_catalog_file_ids_input('1 ')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_catalog_file_ids_input(' 1')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_catalog_file_ids_input(' 1 ')
        self.assertEqual(output, expected_value)
    
    def test_catalog_file_id_list(self):
        console = Console()
        
        expected_value = ('1', '2', '3')
        
        output = console.sanitize_catalog_file_ids_input('1,2,3')
        self.assertEqual(output, expected_value)
        
    def test_padded_catalog_file_id_list(self):
        console = Console()
        
        expected_value = ('1', '2', '3')
        
        output = console.sanitize_catalog_file_ids_input(' 1, 2, 3')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_catalog_file_ids_input('1 ,2 ,3 ')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_catalog_file_ids_input(' 1 , 2 , 3 ')
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_catalog_file_ids_input, '')
    
    def test_none(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_catalog_file_ids_input, None)

class TestSanitizeTagsInput(unittest.TestCase):
    
    def test_tag(self):
        console = Console()
        
        expected_value = ('test',)
        
        output = console.sanitize_tags_input('test')
        self.assertEqual(output, expected_value)
    
    def test_padded_tag(self):
        console = Console()
        
        expected_value = ('test',)
        
        output = console.sanitize_tags_input('test ')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_tags_input(' test')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_tags_input(' test ')
        self.assertEqual(output, expected_value)
    
    def test_tag_list(self):
        console = Console()
        
        expected_value = ('test1', 'test2', 'test3')
        
        output = console.sanitize_tags_input('test1,test2,test3')
        self.assertEqual(output, expected_value)
        
    def test_padded_tag_list(self):
        console = Console()
        
        expected_value = ('test1', 'test2', 'test3')
        
        output = console.sanitize_tags_input(' test1, test2, test3')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_tags_input('test1 ,test2 ,test3 ')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_tags_input(' test1 , test2 , test3 ')
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_tags_input, '')
    
    def test_none(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_tags_input, None)
        
class TestSanitizeFileExtensionsInput(unittest.TestCase):
    
    def test_file_extension(self):
        console = Console()
        
        expected_value = ('ext',)
        
        output = console.sanitize_file_extensions_input('ext')
        self.assertEqual(output, expected_value)
    
    def test_file_extension_leading_period(self):
        console = Console()
        
        expected_value = ('ext',)
        
        output = console.sanitize_file_extensions_input('.ext')
        self.assertEqual(output, expected_value)
    
    def test_padded_file_extension(self):
        console = Console()
        
        expected_value = ('ext',)
        
        output = console.sanitize_file_extensions_input('ext ')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_file_extensions_input(' ext')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_file_extensions_input(' ext ')
        self.assertEqual(output, expected_value)
    
    def test_file_extension_list(self):
        console = Console()
        
        expected_value = ('ext1', 'ext2', 'ext3')
        
        output = console.sanitize_file_extensions_input('ext1,ext2,ext3')
        self.assertEqual(output, expected_value)
        
    def test_file_extension_list_leading_period(self):
        console = Console()
        
        expected_value = ('ext1', 'ext2', 'ext3')
        
        output = console.sanitize_file_extensions_input('.ext1,.ext2,.ext3')
        self.assertEqual(output, expected_value)
        
    def test_padded_file_extension_list(self):
        console = Console()
        
        expected_value = ('ext1', 'ext2', 'ext3')
        
        output = console.sanitize_file_extensions_input(' ext1, ext2, ext3')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_file_extensions_input('ext1 ,ext2 ,ext3 ')
        self.assertEqual(output, expected_value)
        
        output = console.sanitize_file_extensions_input(' ext1 , ext2 , ext3 ')
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_file_extensions_input, '')
    
    def test_none(self):
        console = Console()
        
        self.assertRaises(ValueError, console.sanitize_file_extensions_input, None)