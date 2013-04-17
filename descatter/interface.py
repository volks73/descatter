import argparse
import cmd
import os 
import constants
import catalog

class CommandLine(object):
    
    def __init__(self):
        self.catalog = None
        self.file = None
        
                
        self.parser = argparse.ArgumentParser(description='A cross-platform desktop application for cataloging, organizing, and tagging files', 
                                              prog=constants.APPLICATION_NAME)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CATALOG_ARGUMENT_SHORT_NAME, 
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.CATALOG_ARGUMENT_LONG_NAME, 
                                 nargs='?',
                                 default=os.getcwd(),  
                                 help="Specify the current working catalog")
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.FILE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.FILE_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help="Specify the current working file")
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.ESTABLISH_ARGUMENT_SHORT_NAME, 
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.ESTABLISH_ARGUMENT_LONG_NAME, 
                                 help="Establish or create a catalog",
                                 action='store_true')

        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CHECKIN_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.CHECKIN_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help="Check in the specified file into the specified catalog")
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.INTERACTIVE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.INTERACTIVE_ARGUMENT_LONG_NAME,
                                 action='store_true',
                                 help="Start a console or interactive mode to execute a series of commands within the descatter application")
        
    def parse(self, param_args=None):
        args = vars(self.parser.parse_args(param_args))
    
        self.catalog = catalog.Catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])    
        print("Current working catalog set to: '%s'" % self.catalog.name)
            
        if args[constants.ESTABLISH_ARGUMENT_LONG_NAME]:
            self.establish_catalog()
        
        if args[constants.FILE_ARGUMENT_LONG_NAME]:
            self.file = args[constants.FILE_ARGUMENT_LONG_NAME]
            print("Current working file set to: '%s'" % self.file)
                      
        if args[constants.INTERACTIVE_ARGUMENT_LONG_NAME]:
            Console(self.catalog).cmdloop()
            
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

class Console(cmd.Cmd):
    
    prompt = constants.APPLICATION_NAME + ': '
    
    def __init__(self, cwc, cwf=None):
        self.cwc = cwc # Current Working Catalog
        self.cwf = cwf # Current Working File
        super(Console, self).__init__()
    
    def do_cwc(self, line):
        """Display the current working catalog"""
        # TODO: Add optional -a argument to display absolute path of cwc
        print("Current working catalog: '%s'" % self.cwc.name)
        
    def do_cwf(self, line):
        """Display the current working file"""
        # TODO: Add optional -a argument to display absolute path of cwf
        print("Current working file: '%s'" % self.cwf)
    
    def do_cwd(self, line):
        """Display the current working directory"""
        print("Current working director: %s" % os.getcwd())
    
    def do_catalog(self, catalog_path):
        """Sets the current working catalog"""
        self.cwc = catalog.Catalog(catalog_path)
        print("The current working catalog set to: '%s'" % self.cwc.name)
    
    def do_file(self, file_path):
        """Sets the current working file"""
        self.cwf = file_path
        print("The current working file set to: '%s'" % self.cwf)
    
    def do_establish(self, catalog_path):
        """Establishes or creates a new catalog at the current working catalog"""
        if catalog_path:
            self.cwc = catalog.Catalog(catalog_path)
        
        self.cwc.establish()
        print("The '%s' catalog established at: %s" % (self.cwc.name, self.cwc.path))
    
    def do_exit(self, line):
        """Exits the console or interactive mode"""
        return True