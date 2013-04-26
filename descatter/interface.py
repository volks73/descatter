from prettytable import PrettyTable

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
        
        # TODO: Add all commands from the console as command line arguments
        
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
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.CATALOG_ARGUMENT_SHORT_NAME, 
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.CATALOG_ARGUMENT_LONG_NAME, 
                                 nargs='?',  
                                 help=constants.CATALOG_ARGUMENT_HELP)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.FILE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.FILE_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help=constants.FILE_ARGUMENT_HELP)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.MAPPINGS_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.MAPPINGS_ARGUMENT_LONG_NAME,
                                 help=constants.MAPPINGS_ARGUMENT_HELP,
                                 action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.EXTENSION_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.EXTENSION_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help=constants.EXTENSION_ARGUMENT_HELP)
                                 
        super(Console, self).__init__()
    
    def do_cwc(self, line):
        """Display the current working catalog"""
                
        args = vars(self.parser.parse_args(line.split()))
        
        if self.cwc:
            if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
                print("Current working catalog: '%s'" % self.cwc.path)
            else:
                print("Current working catalog: '%s'" % self.cwc.name)
        else:
            print("No current working catalog has been set")
        
    def do_cwf(self, line):
        """Display the current working file"""
        
        args = vars(self.parser.parse_args(line.split()))
        
        if self.cwf:        
            if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
                print("Current working file: '%s'" % self.cwf[constants.FILE_PATH_KEY])
            else:
                print("Current working file: '%s'" % self.cwf[constants.FILE_NAME_KEY])
        else:
            print("No current working file has been set")
    
    def do_cwd(self, line):
        """Display the current working directory"""
        
        print("Current working directory: %s" % os.getcwd())
    
    def do_catalog(self, catalog_path):
        """Sets the current working catalog"""
        
        if not os.path.isabs(catalog_path):
            catalog_path = os.path.join(os.getcwd(), catalog_path)
            
        self.cwc = catalog.Catalog(catalog_path)
        print("The current working catalog set to: '%s'" % self.cwc.name)
    
    def do_file(self, file_path):
        """Sets the current working file"""
        
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
        
            file_name = os.path.basename(file_path)
                
            self.cwf = { constants.FILE_NAME_KEY : file_name, constants.FILE_PATH_KEY : file_path }
            print("The current working file set to: '%s'" % self.cwf[constants.FILE_NAME_KEY])
        else:
            print("No current working file was set")
    
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
        else:
            print("Good choice!")
    
    def do_checkin(self, line):
        """Checks in the current working file into the current working catalog"""
    
        args = vars(self.parser.parse_args(line.split()))
    
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.do_catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])
            
        if args[constants.FILE_ARGUMENT_LONG_NAME]:
            self.do_file(args[constants.FILE_ARGUMENT_LONG_NAME])
        
        self.cwc.checkin(self.cwf[constants.FILE_PATH_KEY])
    
    def do_list(self, line):
        """Lists various properties and values for the specified catalog"""
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.do_catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if args[constants.MAPPINGS_ARGUMENT_LONG_NAME]:
            
            file_mappings = self.cwc.get_file_mappings()
            
            mappings_table = PrettyTable([constants.FILE_EXTENSION_HEADER_NAME, constants.CONTENT_FOLDER_HEADER_NAME])
            mappings_table.align[constants.CONTENT_FOLDER_HEADER_NAME] = constants.CONTENT_FOLDER_HEADER_ALIGNMENT
            
            if args[constants.EXTENSION_ARGUMENT_LONG_NAME]:
                ext = args[constants.EXTENSION_ARGUMENT_LONG_NAME]
                
                if ext in file_mappings:
                    row = [ext, file_mappings[ext]]
                    mappings_table.add_row(row)
                    print(mappings_table)
                else:
                    print("No mapping exists for '%s' file extension" % ext)
            else:
                for file_extension in sorted(file_mappings):
                    row = [file_extension, file_mappings[file_extension]]
                    mappings_table.add_row(row)
                
                print(mappings_table)
        # TODO: Add listing tags
        # TODO: Add listing files
        # TODO: Add listing templates
        else:
            print("Nothing to list")
    
    def do_exit(self, line):
        """Exits the console or interactive mode"""
        
        return True
    
    def do_quit(self, line):
        """Exits the console or interactive mode"""
        
        return True