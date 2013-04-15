import argparse
import os 
import constants
import catalog

class CommandLine(object):
    
    def __init__(self):
        self.cwc = catalog.Catalog(os.getcwd()) # Current Working Catalog
        self.cwf = None                         # Current Working File
        
        self.parser = argparse.ArgumentParser(description='A cross-platform desktop application for cataloging, organizing, and tagging files', 
                                              prog=constants.APPLICATION_NAME)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CATALOG_ARGUMENT_SHORT_NAME, 
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.CATALOG_ARGUMENT_LONG_NAME, 
                                 nargs='?',  
                                 help="Specify the current working catalog")
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.ESTABLISH_ARGUMENT_SHORT_NAME, 
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.ESTABLISH_ARGUMENT_LONG_NAME, 
                                 help="Establish or create a catalog",
                                 action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CWC_ARGUMENT_SHORT_NAME,
                                help="Display the current working catalog",
                                action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CWF_ARGUMENT_SHORT_NAME,
                                help="Display the current working file",
                                action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.FILE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.FILE_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help="Specify the current working file")

        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CHECKIN_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.CHECKIN_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help="Check in the specified file or current working file into the specified catalog or current working catalog")
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.INTERACTIVE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.INTERACTIVE_ARGUMENT_LONG_NAME,
                                 action='store_true',
                                 help="Start interactive mode to execute a series of commands within the descatter application")
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.EXIT_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.EXIT_ARGUMENT_LONG_NAME,
                                 action='store_true',
                                 help="Exit interactive mode")
        
    def parse(self, param_args=None):
        args = vars(self.parser.parse_args(param_args))
    
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.cwc = catalog.Catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])    
            print("Current working catalog set to: '%s'" % self.cwc.name)
            
        if args[constants.CWC_ARGUMENT_SHORT_NAME]:
            print("Catalog: '%s'" % self.cwc.name)
            
        if args[constants.CWF_ARGUMENT_SHORT_NAME]:
            print("File: '%s'" % self.cwf)
            
        if args[constants.ESTABLISH_ARGUMENT_LONG_NAME]:
            self.establish_catalog()
        
        if args[constants.FILE_ARGUMENT_LONG_NAME]:
            self.cwf = args[constants.FILE_ARGUMENT_LONG_NAME]
            print("Current working file set to: '%s'" % self.cwf)
            
        if args[constants.CHECKIN_ARGUMENT_LONG_NAME]:
            self.checkin_file(self.cwf)
            
        if args[constants.INTERACTIVE_ARGUMENT_LONG_NAME]:
            self.run_interactive_mode()
            
        if args[constants.EXIT_ARGUMENT_LONG_NAME]:
            exit(0)
    
    def run_interactive_mode(self):
        # TODO: Add better interactive mode
        while True:
            response = input(constants.INTERACTIVE_MODE_PROMPT)
            self.parse(response.split())
            
    def establish_catalog(self):
        if os.path.isdir(self.cwc.path):
            proceed = False
            response = None                    
            
            if os.listdir(self.cwc.path):
                while not response:
                    print("The folder for establishing the catalog is not empty")
                    response = input("Would you like to proceed? (Y/Yes or N/No): ")
                    
                    if response == 'Y' or response == 'Yes':      
                        proceed = True
                    elif response == 'N' or response == 'No':
                        proceed = False
                    else:
                        print("Response not recognized, try again")
                        response = None
            else:
                proceed = True
                
            if proceed:
                self.cwc.establish()
                    
                print("The catalog established at '%s'" % self.cwc.path)
            else:
                print("Failed to establish the catalog at '%s'" % self.cwc.path)
        else:
            print("The path to establish the catalog is not a folder. Path: '%s'" % self.cwc.path)
        
    def destroy_catalog(self, path):
        pass
    
    def checkin_file(self, path):
        pass