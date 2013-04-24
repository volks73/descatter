import argparse
import cmd
import os 
import constants
import catalog

class CommandLine(object):
    
    def __init__(self):
        self.catalog = None
        self.file = None
         
        self.parser = argparse.ArgumentParser(description=constants.APPLICATION_DESCRIPTION, 
                                              prog=constants.APPLICATION_NAME)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CATALOG_ARGUMENT_SHORT_NAME, 
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.CATALOG_ARGUMENT_LONG_NAME, 
                                 nargs='?',
                                 default=os.getcwd(),  
                                 help=constants.CATALOG_ARGUMENT_HELP)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.FILE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.FILE_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help=constants.FILE_ARGUMENT_HELP)
        
        self.parser.add_argument(constants.COMMAND_LONG_PREFIX + 
                                 constants.CREATE_ARGUMENT_LONG_NAME, 
                                 help=constants.CREATE_ARGUMENT_HELP,
                                 action='store_true')

        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CHECKIN_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.CHECKIN_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help=constants.CHECKIN_ARGUMENT_HELP)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.INTERACTIVE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.INTERACTIVE_ARGUMENT_LONG_NAME,
                                 action='store_true',
                                 help=constants.INTERACTIVE_ARGUMENT_HELP)
        
    def parse(self, param_args=None):
        args = vars(self.parser.parse_args(param_args))
    
        self.catalog = catalog.Catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])    
        print("Current working catalog set to: '%s'" % self.catalog.name)
            
        if args[constants.CREATE_ARGUMENT_LONG_NAME]:
            self.create_catalog()
        
        if args[constants.FILE_ARGUMENT_LONG_NAME]:
            self.file = args[constants.FILE_ARGUMENT_LONG_NAME]
            print("Current working file set to: '%s'" % self.file)
                      
        if args[constants.INTERACTIVE_ARGUMENT_LONG_NAME]:
            Console(self.catalog).cmdloop()
            
    def create_catalog(self):
        if os.path.isdir(self.cwc.path):
            proceed = False
            response = None                    
            
            if os.listdir(self.cwc.path):
                while not response:
                    print("The folder for creating the catalog is not empty")
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
                self.cwc.create()
                    
                print("The '%s' catalog created at '%s'" % (self.cwc.name, self.cwc.path))
            else:
                print("Failed to create the catalog at '%s'" % self.cwc.path)
        else:
            print("The path: '%s' is not a folder." % self.cwc.path)

class Console(cmd.Cmd):
    
    prompt = constants.CONSOLE_PROMPT
    
    def __init__(self, cwc, cwf=None):
        self.cwc = cwc # Current Working Catalog
        self.cwf = cwf # Current Working File
        
        self.parser = argparse.ArgumentParser(description=constants.CONSOLE_DESCRIPTION)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.ABSOLUTE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.ABSOLUTE_ARGUMENT_LONG_NAME,
                                 help=constants.ABSOLUTE_ARGUMENT_HELP,
                                 action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.SCHEMA_ARGUMENT_SHORT_NAME, 
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.SCHEMA_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help=constants.SCHEMA_ARGUMENT_HELP)
        
        super(Console, self).__init__()
    
    def do_cwc(self, line):
        """Display the current working catalog"""
                
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
            print("Current working catalog: '%s'" % self.cwc.path)
        else:
            print("Current working catalog: '%s'" % self.cwc.name)
        
    def do_cwf(self, line):
        """Display the current working file"""
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
            print("Current working file: '%s'" % self.cwf) # TODO: Add file path attribute
        else:
            print("Current working file: '%s'" % self.cwf)
    
    def do_cwd(self, line):
        """Display the current working directory"""
        
        print("Current working director: %s" % os.getcwd())
    
    def do_catalog(self, catalog_path):
        """Sets the current working catalog"""
        
        if not catalog_path:
            catalog_path = os.getcwd()
            
        self.cwc = catalog.Catalog(catalog_path)
        print("The current working catalog set to: '%s'" % self.cwc.name)
    
    def do_file(self, file_path):
        """Sets the current working file"""
        
        self.cwf = file_path
        print("The current working file set to: '%s'" % self.cwf)
    
    def do_create(self, line):
        """Creates a new catalog at the current working catalog"""
        
        args = vars(self.parser.parse_args(line.split()))    
        
        self.cwc.create(args[constants.SCHEMA_ARGUMENT_LONG_NAME])
        print("The '%s' catalog established at: %s" % (self.cwc.name, self.cwc.path))
    
    def do_destroy(self, catalog_path):
        """Destroy or delete a catalog. This will delete all of the files as well"""
        
        if catalog_path:
            self.cwc = catalog.Catalog(catalog_path)
        
        print("All files will be lost and this cannot be undone!")
        response = input("Are you sure you want to destroy '%s' catalog? (Y/Yes or N/No): " % self.cwc.name)
        
        if response == 'Y' or response == 'Yes':
            self.cwc.destroy()
            print("The catalog has been destroyed!")
            self.cwc = None
        else:
            print("Good choice!")
    
    def do_exit(self, line):
        """Exits the console or interactive mode"""
        
        return True