from interface import Console

import os
import unittest

import constants

class TestPromptYesOrNo(unittest.TestCase):
    
    def test_yes_input(self):
        console = Console()
        
        output = console.prompt_yes_or_no(lambda input: "yes")
        self.assertTrue(output)
        
        output = console.prompt_yes_or_no(lambda input: "y")
        self.assertTrue(output)
    
    def test_padded_yes_input(self):
        console = Console()
    
        output = console.prompt_yes_or_no(lambda input: "yes ")
        self.assertTrue(output)
    
        output = console.prompt_yes_or_no(lambda input: " yes")
        self.assertTrue(output)
    
        output = console.prompt_yes_or_no(lambda input: " yes ")
        self.assertTrue(output)
        
        output = console.prompt_yes_or_no(lambda input: " y")
        self.assertTrue(output)
        
        output = console.prompt_yes_or_no(lambda input: "y ")
        self.assertTrue(output)
        
        output = console.prompt_yes_or_no(lambda input: " y ")
        self.assertTrue(output)
        
    def test_case_sensitive_yes_input(self):
        console = Console()
        
        output = console.prompt_yes_or_no(lambda input: "Yes")
        self.assertTrue(output)
        
        output = console.prompt_yes_or_no(lambda input: "YEs")
        self.assertTrue(output)
        
        output = console.prompt_yes_or_no(lambda input: "YES")
        self.assertTrue(output)
        
        output = console.prompt_yes_or_no(lambda input: "Y")
        self.assertTrue(output)
        
    def test_no_input(self):
        console = Console()
        
        output = console.prompt_yes_or_no(lambda input: "no")
        self.assertFalse(output)
        
        output = console.prompt_yes_or_no(lambda input: "n")
        self.assertFalse(output)
    
    def test_padded_no_input(self):
        console = Console()
    
        output = console.prompt_yes_or_no(lambda input: "no ")
        self.assertFalse(output)
    
        output = console.prompt_yes_or_no(lambda input: " no")
        self.assertFalse(output)
    
        output = console.prompt_yes_or_no(lambda input: " no ")
        self.assertFalse(output)
        
        output = console.prompt_yes_or_no(lambda input: " n")
        self.assertFalse(output)
        
        output = console.prompt_yes_or_no(lambda input: "n ")
        self.assertFalse(output)
        
        output = console.prompt_yes_or_no(lambda input: " n ")
        self.assertFalse(output)
    
    def test_case_sensitive_no_input(self):
        console = Console()
        
        output = console.prompt_yes_or_no(lambda input: "No")
        self.assertFalse(output)
        
        output = console.prompt_yes_or_no(lambda input: "NO")
        self.assertFalse(output)
        
        output = console.prompt_yes_or_no(lambda input: "N")
        self.assertFalse(output)
    
    def test_unacceptable_input(self):
        console = Console()
        
        self.assertRaises(ValueError, console.prompt_yes_or_no, lambda input: "maybe")

class TestPromptCatalogPath(unittest.TestCase):
    
    def test_relative_path_input(self):
        console = Console()
        
        test_catalog_path = os.path.join(os.getcwd(), "tests")
        output = console.prompt_catalog_path(lambda input: "tests")
        self.assertEqual(output, test_catalog_path)
    
    def test_padded_relative_path_input(self):
        console = Console()
        
        test_catalog_path = os.path.join(os.getcwd(), "tests")
        
        output = console.prompt_catalog_path(lambda input: " tests")
        self.assertEqual(output, test_catalog_path)
        
        output = console.prompt_catalog_path(lambda input: "tests ")
        self.assertEqual(output, test_catalog_path)
        
        output = console.prompt_catalog_path(lambda input: " tests ")
        self.assertEqual(output, test_catalog_path)
    
    def test_absolute_path_input(self):
        console = Console()
        
        test_catalog_path = os.path.join(os.getcwd(), "tests")
        input_catalog_path = os.path.join(os.getcwd(), "tests")
        output = console.prompt_catalog_path(lambda input: input_catalog_path)
        self.assertEqual(output, test_catalog_path)
    
    def test_not_folder_path(self):
        console = Console()
        
        self.assertRaises(ValueError, console.prompt_catalog_path, lambda input: "Tests_Catalog")
    
    def test_not_catalog_path(self):
        console = Console()
        
        self.assertRaises(ValueError, console.prompt_catalog_path, lambda input: "tests")

class TestPromptFilePaths(unittest.TestCase):
    
    def test_relative_path_input(self):
        console = Console()
        
        test_file_path = (os.path.join(os.getcwd(), "CHANGES.txt"),)
        
        output = console.prompt_file_paths(lambda input: "CHANGES.txt")
        self.assertEqual(output, test_file_path)
    
    def test_padded_relative_path_input(self):
        console = Console()
        
        test_file_path = (os.path.join(os.getcwd(), "CHANGES.txt"),)
        
        output = console.prompt_file_paths(lambda input: " CHANGES.txt")
        self.assertEqual(output, test_file_path)
        
        output = console.prompt_file_paths(lambda input: "CHANGES.txt ")
        self.assertEqual(output, test_file_path)
        
        output = console.prompt_file_paths(lambda input: " CHANGES.txt ")
        self.assertEqual(output, test_file_path)
    
    def test_relative_path_lists_input(self):
        console = Console()
        
        test_file_paths = (os.path.join(os.getcwd(), "CHANGES.txt"),
                           os.path.join(os.getcwd(), "LICENSE.txt"),
                           os.path.join(os.getcwd(), "README.md"))
        
        input_file_paths = ("CHANGES.txt" + 
                      constants.LIST_SEPARATOR + 
                      " LICENSE.txt" +
                      constants.LIST_SEPARATOR +
                      " README.md")
                
        output = console.prompt_file_paths(lambda input: input_file_paths)
        self.assertEqual(output, test_file_paths)
    
    def test_padded_relative_path_list_input(self):
        console = Console()
        
        test_file_paths = (os.path.join(os.getcwd(), "CHANGES.txt"),
                           os.path.join(os.getcwd(), "LICENSE.txt"),
                           os.path.join(os.getcwd(), "README.md"))
        
        input_file_paths = (" CHANGES.txt" + 
                            constants.LIST_SEPARATOR + 
                            " LICENSE.txt" +
                            constants.LIST_SEPARATOR +
                            " README.md")
                
        output = console.prompt_file_paths(lambda input: input_file_paths)
        self.assertEqual(output, test_file_paths)
        
        input_file_paths = ("CHANGES.txt " + 
                            constants.LIST_SEPARATOR + 
                            "LICENSE.txt " +
                            constants.LIST_SEPARATOR +
                            "README.md ")
                
        output = console.prompt_file_paths(lambda input: input_file_paths)
        self.assertEqual(output, test_file_paths)

        input_file_paths = (" CHANGES.txt " + 
                            constants.LIST_SEPARATOR + 
                            " LICENSE.txt " +
                            constants.LIST_SEPARATOR +
                            " README.md ")
                
        output = console.prompt_file_paths(lambda input: input_file_paths)
        self.assertEqual(output, test_file_paths)

    def test_absolute_path_input(self):
        console = Console()
        
        test_file_path = (os.path.join(os.getcwd(), "CHANGES.txt"), )
        
        file_path_input = os.path.join(os.getcwd(), "CHANGES.txt")
        output = console.prompt_file_paths(lambda input: file_path_input)
        self.assertEqual(output, test_file_path)
    
    def test_absolute_path_list_input(self):
        console = Console()
        
        test_file_paths = (os.path.join(os.getcwd(), "CHANGES.txt"),
                           os.path.join(os.getcwd(), "LICENSE.txt"),
                           os.path.join(os.getcwd(), "README.md"))
        
        input_file_paths = (os.path.join(os.getcwd(), "CHANGES.txt") + 
                            constants.LIST_SEPARATOR +
                            os.path.join(os.getcwd(), "LICENSE.txt") + 
                            constants.LIST_SEPARATOR +
                            os.path.join(os.getcwd(), "README.md"))
        
        output = console.prompt_file_paths(lambda input: input_file_paths)
        self.assertEqual(output, test_file_paths)
    
    def test_not_file_path(self):
        console = Console()
        
        self.assertRaises(ValueError, console.prompt_file_paths, lambda input: "NotAFile.txt")
    
    def test_not_file_path_list(self):
        console = Console()
        
        self.assertRaises(ValueError, console.prompt_file_paths, lambda input: "NotAFile1.txt,NotAFile2.,txt,NotAFile3.txt")