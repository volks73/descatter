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
                      
        if args[constants.INTERACTIVE_ARGUMENT_LONG_NAME]:
            Console(self.catalog).cmdloop()

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
        
        if self.cwc is not None:
            if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
                print("Current working catalog: '%s'" % self.cwc.path)
            else:
                print("Current working catalog: '%s'" % self.cwc.name)
        else:
            print("No current working catalog has been set")
        
    def do_cwf(self, line):
        """Display the current working file"""
        
        args = vars(self.parser.parse_args(line.split()))
        
        if self.cwf is not None:        
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
        
        # TODO: Add check if the file_path is to a file
        
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_path)[1][1:].strip().lower()
                
            self.cwf = {constants.FILE_NAME_KEY : file_name,
                        constants.FILE_EXT_KEY : file_ext,
                        constants.FILE_PATH_KEY : file_path}
            print("The current working file set to: '%s'" % self.cwf[constants.FILE_NAME_KEY])
        else:
            print("No current working file was set")
    
    def do_create(self, line):
        """Creates a new catalog at the current working catalog"""
        
        args = vars(self.parser.parse_args(line.split()))    
        
        self.cwc.create(args[constants.SCHEMA_ARGUMENT_LONG_NAME])
        print("The '%s' catalog created at: %s" % (self.cwc.name, self.cwc.path))
    
    def do_destroy(self, catalog_path):
        """Destroy or delete a catalog. This will delete all of the files as well"""
        
        if catalog_path:
            self.cwc = catalog.Catalog(catalog_path)
        
        print("All files will be lost and this cannot be undone!")
        print("Are you sure you want to destroy '%s' catalog?" % self.cwc.name)
        response = input("(Y/Yes or N/No): ")
        
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
        elif not self.cwf:
            print("Nothing to check in. Please specific a file with the '-f' argument or set a current working file with the 'file' command.")
       
        # TODO: Add -a argument to show the absolute check in file path after checking in
       
        while True:
            try: 
                self.cwc.checkin(self.cwf[constants.FILE_PATH_KEY])
                print("'%s' checked in to catalog" % self.cwf[constants.FILE_NAME_KEY])
            except LookupError:
                file_extension = self.cwf[constants.FILE_EXT_KEY]
                print("The '%s' file extension is unknown for the '%s' catalog." % (file_extension, self.cwc.name))
                print("Would you like to add the '%s' file extension to the '%s' catalog?" % (file_extension, self.cwc.name))
                response = input("(Y/Yes or N/No): ")
                
                if response == 'Y' or response == 'Yes':
                    
                    print("Please specify a folder path relative to the content folder for the '%s' file extension." % file_extension)
                    destination = input("(content folder path): ")
                    
                    while os.path.isabs(response):
                        print("The folder path must be relative to the content folder. Please try again.")
                        response = input("(content folder path): ")
                       
                    self.cwc.content_map.add(file_extension, destination)
                    continue
                else:
                    print("The file was not checked in")
            break 
    
    # TODO: Add -t argument for checkin, which does a test checkin and shows the path the file would be checked in to
    
    def do_map(self, line):
        """Adds a file map to the specified catalog"""
        # TODO: Add adding a file map to the catalog
        # TODO: Add -e, --extension argument to specified an extension to add, change, or remove
        # TODO: Add -r, --remove argument to remove a mapping from the catalog
        # TODO: Add -l, --list to list mappings, same as 'list -m' command and option
        pass
    
    def do_list(self, line):
        """Lists various properties and values for the specified catalog"""
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.do_catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if args[constants.MAPPINGS_ARGUMENT_LONG_NAME]:
            mappings_table = PrettyTable([constants.FILE_EXTENSION_HEADER_NAME, constants.CONTENT_FOLDER_HEADER_NAME])
            mappings_table.align[constants.CONTENT_FOLDER_HEADER_NAME] = constants.CONTENT_FOLDER_HEADER_ALIGNMENT
            parent_path = None
            file_map = self.cwc.content_map.map
            
            if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
                parent_path = os.path.join(self.cwc.path, constants.CONTENT_FOLDER_NAME)
            
            if args[constants.EXTENSION_ARGUMENT_LONG_NAME]:
                file_extension = args[constants.EXTENSION_ARGUMENT_LONG_NAME]
            
                if file_extension in self.cwc.content_map.map:
                    row = [file_extension, os.path.join(parent_path, file_map[file_extension])]
                    mappings_table.add_row(row)
                else:
                    print("No mapping exists for '%s' file extension" % file_extension)
            else:
                for file_extension in sorted(file_map):
                    row = [file_extension, os.path.join(parent_path, file_map[file_extension])]
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