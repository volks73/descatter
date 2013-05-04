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
    
    def __init__(self, cwc=None, cwf=None):
        """ Initializes the console. """
        
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
                                 constants.MAP_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.MAP_ARGUMENT_LONG_NAME,
                                 help=constants.MAP_ARGUMENT_HELP,
                                 action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX + 
                                 constants.EXTENSION_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX + 
                                 constants.EXTENSION_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help=constants.EXTENSION_ARGUMENT_HELP)
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.DESTINATION_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.DESTINATION_ARGUMENT_LONG_NAME,
                                 nargs='?',
                                 help=constants.DESTINATION_ARGUMENT_HELP)
                                 
        super(Console, self).__init__()
    
    def print_specify_catalog(self):
        """ Prints a message to the console to specify a catalog for the command. """
        
        print("No catalog specified. Please specify a catalog with the '" + constants.COMMAND_SHORT_PREFIX + constants.CATALOG_ARGUMENT_SHORT_NAME + "' argument or set a current working catalog with the '" + constants.CATALOG_ARGUMENT_LONG_NAME + "' command")
    
    def print_specify_file(self):
        """ Prints a message to the console to specify a file for the command. """
        
        print("Please specific a file with the '" + constants.COMMAND_SHORT_PREFIX + constants.FILE_ARGUMENT_SHORT_NAME + "' argument or set a current working file with the '" + constants.FILE_ARGUMENT_LONG_NAME + "' command.")
    
    def do_cwc(self, line):
        """ Display the current working catalog. """
                
        args = vars(self.parser.parse_args(line.split()))
        
        if self.cwc is None:
            print("No current working catalog has been set")
        else:
            if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
                print("Current working catalog: '%s'" % self.cwc.path)
            else:
                print("Current working catalog: '%s'" % self.cwc.name)
        
    def do_cwf(self, line):
        """ Display the current working file. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if self.cwf is None:
            print("No current working file has been set")
        else:        
            if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
                print("Current working file: '%s'" % self.cwf[constants.FILE_PATH_KEY])
            else:
                print("Current working file: '%s'" % self.cwf[constants.FILE_NAME_KEY])          
    
    def do_cwd(self, line):
        """ Display the current working directory. """
        
        print("Current working directory: %s" % os.getcwd())
    
    def do_catalog(self, catalog_path):
        """ Sets the current working catalog. """
        
        if not os.path.isabs(catalog_path):
            catalog_path = os.path.join(os.getcwd(), catalog_path)    
        
        if catalog.is_catalog(catalog_path):
            self.cwc = catalog.Catalog(catalog_path)
            print("The current working catalog set to: '%s'" % self.cwc.name)
        else:
            print("The path is not to a " + constants.APPLICATION_NAME + " catalog")
            self.cwc = None
    
    def do_file(self, file_path):
        """ Sets the current working file. """
        
        if os.path.isfile(file_path):       
            file_path = os.path.join(os.getcwd(), file_path)
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_path)[1][1:].strip().lower()
                    
            self.cwf = {constants.FILE_NAME_KEY : file_name,
                        constants.FILE_EXT_KEY : file_ext,
                        constants.FILE_PATH_KEY : file_path}
            print("The current working file set to: '%s'" % self.cwf[constants.FILE_NAME_KEY])
        else:
            print("Path is not a file!")
    
    def do_create(self, line):
        """ Sub-command to create file extension maps, templates, and tags at the specified catalog. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.MAP_ARGUMENT_LONG_NAME]:
            self.create_map(args)    
        elif args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.create_catalog(args)
        else:
            print("Nothing to create")

    def create_map(self, args):
        """ Creates a file extension map for the specified catalog. """
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.do_catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])
            
        if self.cwc is None:
            self.print_specify_catalog()
        else:        
            file_extension = None
            
            if args[constants.EXTENSION_ARGUMENT_LONG_NAME]:
                file_extension = args[constants.EXTENSION_ARGUMENT_LONG_NAME]
            else:
                print("Please specify a file extension")
                file_extension = input("(file extension): ")
            
            if file_extension[0] == '.':
                file_extension = file_extension[1:]
                
            destination = None
            
            if args[constants.DESTINATION_ARGUMENT_LONG_NAME]:
                destination = args[constants.DESTINATION_ARGUMENT_LONG_NAME]
            else:
                print("Please specify a folder path relative to the content folder for the '%s' file extension." % file_extension)
                destination = input("(content folder path): ")
                
            self.cwc.content_map.add(file_extension, destination)
            
            catalog_destination = self.cwc.content_map.get_destination(file_extension)
            print("The '%s' file extension mapped to the '%s' content folder" % (file_extension, catalog_destination))

    def do_remove(self, line):
        """ Removes a file extension mapping from the specified catalog. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.do_catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if self.cwc is None:
            self.print_specify_catalog()
        elif args[constants.MAP_ARGUMENT_LONG_NAME]:
            self.remove_map(args)
        else:
            print("Nothing to remove!")    
        
    def remove_map(self, args):
        """ Removes a file extension map from the current working catalog. """
        
        file_extension = None
            
        if args[constants.EXTENSION_ARGUMENT_LONG_NAME]:
            file_extension = args[constants.EXTENSION_ARGUMENT_LONG_NAME]
        else:
            print("Please specify a file extension")
            file_extension = input("(file extension): ")
        
        if file_extension[0] == '.':
            file_extension = file_extension[1:]
            
        try:
            self.cwc.content_map.remove(file_extension)
            print("The '%s' file extension map removed from the '%s' catalog" % (file_extension, self.cwc.name))
        except KeyError:
            print("The '%s' file extension not mapped in the '%s' catalog" % (file_extension, self.cwc.name))

    def do_establish(self, line):
        """ Establishes a new catalog at the specified path. """
        
        split_line = line.split()
        catalog_path = split_line[0]
        args = vars(self.parser.parse_args(split_line[1:]))
        
        if not os.path.isabs(catalog_path):
            catalog_path = os.path.join(os.getcwd(), catalog_path)    
         
        self.cwc = catalog.establish(catalog_path, args[constants.SCHEMA_ARGUMENT_LONG_NAME])
        print("The '%s' catalog established at: '%s'" % (self.cwc.name, self.cwc.path))
        print("The current working catalog set to: '%s'" % self.cwc.name)

    def do_destroy(self, line):
        """ Destroys or deletes a catalog at the specified path. This will delete all of the files as well. """
        
        if line:
            split_line = line.split()
            catalog_path = split_line[0]
        
            self.do_catalog(catalog_path)
            
            if self.cwc is not None:
                print("All files will be lost and this cannot be undone!")
                print("Are you sure you want to destroy the '%s' catalog?" % self.cwc.name)
                response = input("(Y/Yes or N/No): ")
            
                if response == 'Y' or response == 'Yes':
                    catalog.destroy(catalog_path)
                    print("The catalog has been destroyed!")
                    
                    self.cwc = None
                else:
                    print("Good choice!")
        else:
            print("Please specify an absolute path to the catalog to be destroyed")
    
    def do_checkin(self, line):
        """Checks in the current working file into the current working catalog"""
    
        args = vars(self.parser.parse_args(line.split()))
    
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.do_catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])
            
        if args[constants.FILE_ARGUMENT_LONG_NAME]:
            self.do_file(args[constants.FILE_ARGUMENT_LONG_NAME])
        
        if self.cwc is None:
            self.print_specify_catalog()
        elif self.cwf is None:
            self.print_specity_file()
        else:
            while True:
                try: 
                    destination = self.cwc.checkin(self.cwf[constants.FILE_PATH_KEY])
                    
                    if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
                        checkin_absolute_path = os.path.join(self.cwc.path, constants.CONTENT_FOLDER_NAME)
                        checkin_absolute_path = os.path.join(checkin_absolute_path, destination)
                        print("'%s' checked in to '%s' at '%s'" % (self.cwf[constants.FILE_PATH_KEY], self.cwc.path, checkin_absolute_path))   
                    else:
                        print("'%s' checked in to '%s' at '%s'" % (self.cwf[constants.FILE_NAME_KEY], self.cwc.name, destination))
                        
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
    
    def do_show(self, line):
        """ Shows various properties and values for the specified catalog """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.do_catalog(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if self.cwc is None:
            self.print_specify_catalog()
        else:
            if args[constants.MAP_ARGUMENT_LONG_NAME]:
                self.show_map(args)
            else:
                print("Nothing to show!")
    
    def show_map(self, args):
        """ Shows the file extension maps in a ASCII table sorted in descending alphabetical order """
        
        map_table = PrettyTable([constants.FILE_EXTENSION_HEADER_NAME, constants.CONTENT_FOLDER_HEADER_NAME])
        map_table.align[constants.CONTENT_FOLDER_HEADER_NAME] = constants.CONTENT_FOLDER_HEADER_ALIGNMENT
        parent_path = None
        file_map = self.cwc.content_map.map
                
        if args[constants.ABSOLUTE_ARGUMENT_LONG_NAME]:
            parent_path = os.path.join(self.cwc.path, constants.CONTENT_FOLDER_NAME)
                
        if args[constants.EXTENSION_ARGUMENT_LONG_NAME]:
            file_extension = args[constants.EXTENSION_ARGUMENT_LONG_NAME]
                
            if file_extension in file_map:
                row = [file_extension, os.path.join(parent_path, file_map[file_extension])]
                map_table.add_row(row)
            else:
                print("No map exists for the '%s' file extension" % file_extension)
        else:
            for file_extension in sorted(file_map):
                row = [file_extension, os.path.join(parent_path, file_map[file_extension])]
                map_table.add_row(row)        
                    
        print(map_table)
    
    def do_exit(self, line):
        """ Safely exits the console or interactive mode. """
        
        return True
    
    def do_quit(self, line):
        """ Safely exits the console or interactive mode. """
        
        return True