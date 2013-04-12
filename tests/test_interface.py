from nose.tools import *

import sys
import os
import shutil
import interface
import constants

class TestCommandLine(object):
    
    def __init__(self):
        self.test_path = os.path.join(os.getcwd(), constants.TESTS_FOLDER_NAME)
        self.test_catalog_path = os.path.join(self.test_path, constants.TEST_CATALOG_NAME)
        self.calling_args = sys.argv
    
    def setup(self):
        os.mkdir(self.test_catalog_path)
        remove_args = sys.argv[:1]
        sys.argv = remove_args
    
    def teardown(self):
        shutil.rmtree(self.test_catalog_path)
        sys.argv = self.calling_args
    
    def test_create(self):
        sys.argv.append(constants.CREATE_SUBCOMMAND_NAME)
        sys.argv.append(self.test_catalog_path)
        
        command_line_interface = interface.CommandLine()
        command_line_interface.parse()
        
        