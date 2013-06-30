from interface import Console
from interface import InputError

import os
import tempfile
import shutil
import unittest

import constants
import catalog

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
        
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_user_input, '')
        
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_user_input, None)

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
        self.assertRaises(InputError, console.sanitize_yes_or_no_input, "maybe")
        
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_yes_or_no_input, '')
        
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_yes_or_no_input, None)

class TestSanitizeFolderPathInput(unittest.TestCase):
    
    def setUp(self):
        self.test_temp_folder_path = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.test_temp_folder_path)
    
    def test_absolute_path(self):
        console = Console()
        
        expected_value = self.test_temp_folder_path
        input_value = '%s' % os.path.abspath(self.test_temp_folder_path)
        output = console.sanitize_folder_path_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_relative_path(self):
        console = Console()
        
        expected_value = self.test_temp_folder_path
        input_value = '%s' % os.path.relpath(self.test_temp_folder_path)
        output = console.sanitize_folder_path_input(expected_value)
        self.assertEqual(output, expected_value)
    
    def test_invalid_path(self):
        console = Console()
        
        input_value = 'test!@#$%^&*()+=[]{}|?<>.tmp'
        self.assertRaises(InputError, console.sanitize_folder_path_input, input_value)
    
    def test_trailing_forward_slash(self):
        console = Console()
        
        expected_value = self.test_temp_folder_path 
        input_value = '%s' % os.path.abspath(self.test_temp_folder_path) + '\\'
        output = console.sanitize_folder_path_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_trailing_back_slash(self):
        console = Console()
        
        expected_value = self.test_temp_folder_path
        input_value = '%s' % os.path.abspath(self.test_temp_folder_path) + '/'
        output = console.sanitize_folder_path_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded_path(self):
        console = Console()
        
        expected_value = self.test_temp_folder_path
        
        input_value = ' %s' % os.path.abspath(self.test_temp_folder_path)
        output = console.sanitize_folder_path_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = '%s ' % os.path.abspath(self.test_temp_folder_path)
        output = console.sanitize_folder_path_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' %s ' % os.path.abspath(self.test_temp_folder_path)
        output = console.sanitize_folder_path_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_folder_path_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_folder_path_input, None)

class TestSanitizeCatalogPathInput(unittest.TestCase):
    
    def setUp(self):
        self.test_temp_folder = tempfile.mkdtemp()
        self.test_catalog_path = os.path.join(self.test_temp_folder, "Sanitize_Catalog_Path_Input_Test_Catalog")
        self.test_catalog = catalog.create(self.test_catalog_path)
    
    def tearDown(self):
        self.test_catalog.session.close_all()
        shutil.rmtree(self.test_temp_folder)
    
    def test_input(self):
        console = Console()
        
        input_value = '%s' % self.test_catalog_path
        expected_value = self.test_catalog_path
        output = console.sanitize_catalog_path_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_padded_input(self):
        console = Console()
        
        expected_value = self.test_catalog_path
        
        input_value = ' %s' % expected_value
        output = console.sanitize_catalog_path_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = '%s ' % expected_value
        output = console.sanitize_catalog_path_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' %s ' % expected_value
        output = console.sanitize_catalog_path_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_not_folder_path(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_catalog_path_input, "test_not_catalog_path")
        
    def test_not_catalog_path(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_catalog_path_input, "test_not_catalog_path")
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_catalog_path_input, '')
        
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_catalog_path_input, None)

class TestSanitizeFilePathInput(unittest.TestCase):
    
    def setUp(self):
        test_temp_file, self.test_temp_file_path = tempfile.mkstemp(suffix='.txt', text=True)
        os.close(test_temp_file)
    
    def tearDown(self):
        os.remove(self.test_temp_file_path)
    
    def test_absolute_path(self):
        console = Console()
        
        expected_value = self.test_temp_file_path
        input_value = '%s' % os.path.abspath(self.test_temp_file_path)
        output = console.sanitize_file_path_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_relative_path(self):
        console = Console()
        
        expected_value = self.test_temp_file_path
        input_value = '%s' % os.path.relpath(self.test_temp_file_path)
        output = console.sanitize_file_path_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded_path(self):
        console = Console()
        
        expected_value = self.test_temp_file_path
        
        input_value = ' %s' % os.path.abspath(self.test_temp_file_path)
        output = console.sanitize_file_path_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = '%s ' % os.path.abspath(self.test_temp_file_path)
        output = console.sanitize_file_path_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' %s ' % os.path.abspath(self.test_temp_file_path)
        output = console.sanitize_file_path_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_file_path_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_file_path_input, None)

class TestSanitizeFilePathsInput(unittest.TestCase):
    
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
    
    def test_absolute_paths(self):
        console = Console()
        
        expected_value = (self.test_temp_file1_path,
                          self.test_temp_file2_path,
                          self.test_temp_file3_path)
        
        input_value = ('%s' % os.path.abspath(self.test_temp_file1_path) + 
                       constants.LIST_SEPARATOR + 
                       '%s' % os.path.abspath(self.test_temp_file2_path) + 
                       constants.LIST_SEPARATOR + 
                       '%s' % os.path.abspath(self.test_temp_file3_path))
        
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_relative_paths(self):
        console = Console()
        
        expected_value = (self.test_temp_file1_path,
                          self.test_temp_file2_path,
                          self.test_temp_file3_path)
        
        input_value = ('%s' % os.path.relpath(self.test_temp_file1_path) + 
                       constants.LIST_SEPARATOR + 
                       '%s' % os.path.relpath(self.test_temp_file2_path) + 
                       constants.LIST_SEPARATOR + 
                       '%s' % os.path.relpath(self.test_temp_file3_path))
        
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded_paths(self):
        console = Console()
        
        expected_value = (self.test_temp_file1_path,
                          self.test_temp_file2_path,
                          self.test_temp_file3_path)
        
        input_value = (' %s' % os.path.abspath(self.test_temp_file1_path) + 
                       constants.LIST_SEPARATOR + 
                       ' %s' % os.path.abspath(self.test_temp_file2_path) + 
                       constants.LIST_SEPARATOR + 
                       ' %s' % os.path.abspath(self.test_temp_file3_path))
        
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ('%s ' % os.path.abspath(self.test_temp_file1_path) + 
                       constants.LIST_SEPARATOR + 
                       '%s ' % os.path.abspath(self.test_temp_file2_path) + 
                       constants.LIST_SEPARATOR + 
                       '%s ' % os.path.abspath(self.test_temp_file3_path))
        
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = (' %s ' % os.path.abspath(self.test_temp_file1_path) + 
                       constants.LIST_SEPARATOR + 
                       ' %s ' % os.path.abspath(self.test_temp_file2_path) + 
                       constants.LIST_SEPARATOR + 
                       ' %s ' % os.path.abspath(self.test_temp_file3_path))
        
        output = console.sanitize_file_paths_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_not_file_path_list(self):
        console = Console()
        
        input_values = ("NotAFile1.txt" +
                        constants.LIST_SEPARATOR +
                        "NotAFile2.txt" +
                        constants.LIST_SEPARATOR +
                        "NotAFile3.txt")
        
        self.assertRaises(InputError, console.sanitize_file_paths_input, input_values)
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_file_paths_input, '')
        
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_file_paths_input, None)

class TestSanitizeCatalogFileIdInput(unittest.TestCase):
    
    def test_catalog_file_id(self):
        console = Console()
        
        expected_value = '1'
        input_value = '1'
        output = console.sanitize_catalog_file_id_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded(self):
        console = Console()
        
        expected_value = '1'
        
        input_value = '1 '
        output = console.sanitize_catalog_file_id_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' 1'
        output = console.sanitize_catalog_file_id_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' 1 '
        output = console.sanitize_catalog_file_id_input(input_value)
        self.assertEqual(output, expected_value)

    def test_non_integer(self):
        console = Console()
        
        input_value = "test value"
        self.assertRaises(InputError, console.sanitize_catalog_file_id_input, input_value)

    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_catalog_file_id_input, '')
        
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_catalog_file_id_input, None)

class TestSanitizeCatalogFileIdsInput(unittest.TestCase):
    
    def test_catalog_file_ids(self):
        console = Console()
        
        expected_value = ('1', '2', '3')
        input_value = '1' + constants.LIST_SEPARATOR + '2' + constants.LIST_SEPARATOR + '3'
        output = console.sanitize_catalog_file_ids_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_padded(self):
        console = Console()
        
        expected_value = ('1', '2', '3')
        
        input_value = ' 1' + constants.LIST_SEPARATOR + ' 2' + constants.LIST_SEPARATOR + ' 3'
        output = console.sanitize_catalog_file_ids_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = '1 ' + constants.LIST_SEPARATOR + '2 ' + constants.LIST_SEPARATOR + '3 '
        output = console.sanitize_catalog_file_ids_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' 1 ' + constants.LIST_SEPARATOR + ' 2 ' + constants.LIST_SEPARATOR + ' 3 '
        output = console.sanitize_catalog_file_ids_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_catalog_file_ids_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_catalog_file_ids_input, None)

class TestSanitizeTagInput(unittest.TestCase):
    
    def test_tag(self):
        console = Console()
        
        expected_value = 'test'
        input_value = 'test'
        output = console.sanitize_tag_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_tag_with_spaces(self):
        console = Console()
        
        expected_value = 'test 1'
        input_value = 'test 1'
        output = console.sanitize_tag_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded_tag(self):
        console = Console()
        
        expected_value = 'test'
        
        input_value = 'test '
        output = console.sanitize_tag_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' test'
        output = console.sanitize_tag_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' test '
        output = console.sanitize_tag_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_tag_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_tag_input, None)

class TestSanitizeTagsInput(unittest.TestCase):
    
    def test_tags(self):
        console = Console()
        
        expected_value = ('test_tag1','test_tag2','test_tag3')
        input_value = ('test_tag1' +
                       constants.LIST_SEPARATOR +
                       'test_tag2' +
                       constants.LIST_SEPARATOR +
                       'test_tag3')
        output = console.sanitize_tags_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded_tag(self):
        console = Console()
        
        expected_value = ('test_tag1','test_tag2','test_tag3')
        
        input_value = (' test_tag1' +
                       constants.LIST_SEPARATOR +
                       ' test_tag2' +
                       constants.LIST_SEPARATOR +
                       ' test_tag3')
        
        output = console.sanitize_tags_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ('test_tag1 ' +
                       constants.LIST_SEPARATOR +
                       'test_tag2 ' +
                       constants.LIST_SEPARATOR +
                       'test_tag3 ')
        
        output = console.sanitize_tags_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = (' test_tag1 ' +
                       constants.LIST_SEPARATOR +
                       ' test_tag2 ' +
                       constants.LIST_SEPARATOR +
                       ' test_tag3 ')
        
        output = console.sanitize_tags_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_tags_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_tags_input, None)

class TestSanitizeFileExtensionInput(unittest.TestCase):
    
    def test_file_extension(self):
        console = Console()
        
        expected_value = 'ext'
        input_value = 'ext'
        output = console.sanitize_file_extension_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_leading_period(self):
        console = Console()
        
        expected_value = 'ext'
        input_value = '.ext'
        output = console.sanitize_file_extension_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded(self):
        console = Console()
        
        expected_value = 'ext'
        
        input_value = 'ext '
        output = console.sanitize_file_extension_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' ext'
        output = console.sanitize_file_extension_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' ext '
        output = console.sanitize_file_extension_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_file_extension_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_file_extension_input, None)
        
class TestSanitizeFileExtensionsInput(unittest.TestCase):
    
    def test_file_extension_list(self):
        console = Console()
        
        expected_value = ('ext1', 'ext2', 'ext3')
        input_value = 'ext1' + constants.LIST_SEPARATOR + 'ext2' + constants.LIST_SEPARATOR + 'ext3'
        output = console.sanitize_file_extensions_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_file_extension_list_leading_period(self):
        console = Console()
        
        expected_value = ('ext1', 'ext2', 'ext3')
        input_value = '.ext1' + constants.LIST_SEPARATOR + '.ext2' + constants.LIST_SEPARATOR + '.ext3'
        output = console.sanitize_file_extensions_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_padded_file_extension_list(self):
        console = Console()
        
        expected_value = ('ext1', 'ext2', 'ext3')
        
        input_value = ' ext1' + constants.LIST_SEPARATOR + ' ext2' + constants.LIST_SEPARATOR + ' ext3'
        output = console.sanitize_file_extensions_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = 'ext1 ' + constants.LIST_SEPARATOR + 'ext2 ' + constants.LIST_SEPARATOR + 'ext3 '
        output = console.sanitize_file_extensions_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' ext1 ' + constants.LIST_SEPARATOR + ' ext2 ' + constants.LIST_SEPARATOR + ' ext3 '
        output = console.sanitize_file_extensions_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_file_extensions_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_file_extensions_input, None)

class TestSanitizeTitleInput(unittest.TestCase):
    
    def test_title(self):
        console = Console()
        
        expected_value = 'Title'
        input_value = 'Title'
        
        output = console.sanitize_title_input(input_value)
        self.assertEqual(output, expected_value)
    
    def test_padded(self):
        console = Console()
        
        expected_value = 'Title'
        
        input_value = ' Title'
        output = console.sanitize_title_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = 'Title '
        output = console.sanitize_title_input(input_value)
        self.assertEqual(output, expected_value)
        
        input_value = ' Title '
        output = console.sanitize_title_input(input_value)
        self.assertEqual(output, expected_value)
        
    def test_empty(self):
        console = Console()
        self.assertRaises(InputError, console.sanitize_title_input, '')
    
    def test_none(self):
        console = Console()
        self.assertRaises(ValueError, console.sanitize_title_input, None)