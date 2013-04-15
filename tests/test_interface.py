from nose.tools import *

import os
import shutil
import interface
import constants

class TestCommandLine(object):
    
    def __init__(self):
        self.test_path = os.path.join(os.getcwd(), constants.TESTS_FOLDER_NAME)
        self.test_catalog_path = os.path.join(self.test_path, constants.TEST_CATALOG_NAME)
        self.command_line_interface = interface.CommandLine()
    
    def setup(self):
        os.mkdir(self.test_catalog_path)
    
    def teardown(self):
        shutil.rmtree(os.path.join(self.command_line_interface.cwc.path, constants.CONTENT_FOLDER_NAME))
        shutil.rmtree(os.path.join(self.command_line_interface.cwc.path, constants.HOOKS_FOLDER_NAME))
        shutil.rmtree(os.path.join(self.command_line_interface.cwc.path, constants.LOG_FOLDER_NAME))
        shutil.rmtree(os.path.join(self.command_line_interface.cwc.path, constants.TEMPLATES_FOLDER_NAME))
        os.remove(os.path.join(self.command_line_interface.cwc.path, self.command_line_interface.cwc.name + constants.SQLITE_EXTENSION))
        shutil.rmtree(self.test_catalog_path)
    
    def test_establish_without_path(self):
        test_args = '-e'
        self.command_line_interface.parse(test_args.split())
        
        cwd = os.getcwd()
        
        assert(self.command_line_interface.cwc.path == cwd, "The established catalog path is not the current working directory by default") 
        assert(self.command_line_interface.cwc.name == constants.APPLICATION_NAME, "The catalog name is not 'descatter'")
    
    def test_establish_with_path(self):
        test_args = '-c ' + self.test_catalog_path + ' -e' 
        self.command_line_interface.parse(test_args.split())
        
        assert(self.command_line_interface.cwc.path == self.test_catalog_path, "The established catalog path is not the 'Test_Catalog' directory in the 'tests' folder") 
        assert(self.command_line_interface.cwc.name == constants.TEST_CATALOG_NAME, "The catalog name is not 'Test_Catalog'")