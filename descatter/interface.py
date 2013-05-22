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
        
        self.parser.add_argument(constants.PATH_ARGUMENT_LONG_NAME,  
                                 nargs='*',  
                                 default=None)
        
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
                                 help=constants.FILE_ARGUMENT_HELP,
                                 action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.MAP_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.MAP_ARGUMENT_LONG_NAME,
                                 help=constants.MAP_ARGUMENT_HELP,
                                 action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.TAG_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.TAG_ARGUMENT_LONG_NAME,
                                 help=constants.TAG_ARGUMENT_HELP,
                                 action='store_true')
        
        self.parser.add_argument(constants.COMMAND_SHORT_PREFIX +
                                 constants.VERBOSE_ARGUMENT_SHORT_NAME,
                                 constants.COMMAND_LONG_PREFIX +
                                 constants.VERBOSE_ARGUMENT_LONG_NAME,
                                 help=constants.VERBOSE_ARGUMENT_HELP,
                                 action='store_true')
                                 
        super(Console, self).__init__()
    
    def print_specify_catalog(self):
        """ Prints a message to the console to specify a catalog for the command. """
        
        print("No catalog specified!")
        
        text = ("Please specify a catalog with the '" + 
                constants.COMMAND_SHORT_PREFIX + 
                constants.CATALOG_ARGUMENT_SHORT_NAME + 
                "' argument or set a current working catalog with the '" + 
                constants.CATALOG_ARGUMENT_LONG_NAME + 
                "' command")
        
        print(text)
    
    def print_catalog_files_table(self, catalog_files, verbose=False):
        
        table_headers = [constants.TITLE_HEADER_NAME,
                         constants.CONTENT_PATH_HEADER_NAME,
                         constants.CONTENT_NAME_HEADER_NAME]
        
        if verbose:
            table_headers.append(constants.ORIGINAL_PATH_HEADER_NAME)
            table_headers.append(constants.ORIGINAL_NAME_HEADER_NAME) 
        
        files_table = PrettyTable(table_headers)
        files_table.align[constants.TITLE_HEADER_NAME] = constants.TITLE_HEADER_ALIGNMENT
        files_table.align[constants.CONTENT_PATH_HEADER_NAME] = constants.CONTENT_PATH_HEADER_ALIGNMENT
        
        for catalog_file in catalog_files:
            
            row = [catalog_file.get_title(),
                   catalog_file.get_content_path(),
                   catalog_file.get_content_name()]
            
            if verbose:
                row.append(catalog_file.get_original_path())
                row.append(catalog_file.get_original_name())
            
            files_table.add_row(row)
        
        print(files_table)
    
    def input_prompt(self, value):
        """ Display prompt to input a value after displaying a question """
        
        prompt = (constants.CONSOLE_PROMPT_PREFIX + 
                  value + 
                  constants.CONSOLE_PROMPT_SUFFIX + 
                  constants.CONSOLE_PROMPT_TERMINATOR)
        
        # TODO: Add a cancel option
        
        return input(prompt)
    
    def set_cwc(self, catalog_path, verbose=False):
        """ Sets the current working catalog """
    
        if catalog.is_catalog(catalog_path):           
            if self.cwc is not None:
                self.cwc.db.disconnect()
            
            self.cwc = catalog.Catalog(catalog_path)
            
            if verbose:
                print("The current working catalog set to: '%s'" % self.cwc.path)
            else:
                print("The current working catalog set to: '%s'" % self.cwc.name)
        else:
            print("The path is not to a " + constants.APPLICATION_NAME + " catalog")
    
    def set_cwf(self, content_path, verbose=False):
        """ Sets the current working file """
        
        possible_file = self.cwc.get_file(content_path)
        
        if possible_file is not None:
            self.cwf = possible_file
            
            if verbose:
                print("Current working file set to:")
                self.do_cwf()
            else:
                print("Current working file set!")
        else:
            print("File could not be found!")
    
    def do_cwc(self, line=None):
        """ Display the current working catalog. """
                
        args = vars(self.parser.parse_args(line.split()))
        
        if self.cwc is None:
            print("No current working catalog has been set!")
        else:
            if args[constants.VERBOSE_ARGUMENT_LONG_NAME]:
                print("Current working catalog: '%s'" % self.cwc.path)
            else:
                print("Current working catalog: '%s'" % self.cwc.name)
        
    def do_cwf(self, line=None):
        """ Display the current working file. """
        
        if self.cwf is None:
            print("No current working file has been set!")
        else:
            self.print_catalog_files_table([self.cwf])         
    
    def do_cwd(self, line):
        """ Display the current working directory. """
        
        print("Current working directory: %s" % os.getcwd())
    
    def do_catalog(self, line):
        """ Sets the current working catalog. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        catalog_path = args[constants.PATH_ARGUMENT_LONG_NAME]
        
        if catalog_path:
            catalog_path = catalog_path[0]
        else:
            print("Please specify a catalog by its path")
            catalog_path = self.input_prompt('catalog path')    
        
        self.set_cwc(catalog_path, args[constants.VERBOSE_ARGUMENT_LONG_NAME])
            
        # TODO: Add saving a history of catalogs used in User home directory installation of descatter
    
    def do_file(self, line):
        """ Sets the current working file. """
        
        args = vars(self.parser.parse_args(line.split()))
                
        content_path = args[constants.PATH_ARGUMENT_LONG_NAME]
        
        if content_path:
            content_path = content_path[0]
        else:
            print("Please specify a catalog file by its content path")
            content_path = self.input_prompt('content path')
        
        self.set_cwf(content_path, args[constants.VERBOSE_ARGUMENT_LONG_NAME])
        
        # TODO: Add history of recently used files

    def do_tag(self, line):
        """ Tags a file """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.set_cwc(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if self.cwc is None:
            self.print_specify_catalog()
        else:
            content_path = args[constants.PATH_ARGUMENT_LONG_NAME]
            
            if content_path:
                content_path = content_path[0]
            else:
                print("Please specify a catalog file by its content path")
                content_path = self.input_prompt('content path')

            tag_file = self.cwc.get_file(content_path)

            if tag_file is not None:                        
                print("Please specify a tag")
                tag_name = self.input_prompt('tag')
        
                # TODO: Add comma separated listing for batch tagging of file
        
                self.cwc.tag(tag_file, catalog.Tag(tag_name))
                print("File successfully tagged!")
                self.set_cwf(tag_file.content_path)
    
    def do_find(self, line):
        """ Find all files tagged with the specified tag """
        
        pass
    
    def do_create(self, line):
        """ Sub-command to create file extension maps, templates, and tags at the specified catalog. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.set_cwc(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if self.cwc is None:
            self.print_specify_catalog()
        elif args[constants.MAP_ARGUMENT_LONG_NAME]:
            self.create_map(args)
        elif args[constants.TAG_ARGUMENT_LONG_NAME]:
            self.create_tag(args)
        else:
            print("Nothing to create")

    def create_map(self, args):
        """ Creates a file extension map for the specified catalog. """
        
        print("Please specify a file extension")
        file_extension = self.input_prompt('file extension')
            
        if file_extension[0] == '.':
            file_extension = file_extension[1:]
        
        print("Please specify a content path for the '%s' file extension." % file_extension)
        destination = self.input_prompt("content folder path")
                
        self.cwc.content_map.add(file_extension, destination)
            
        catalog_destination = self.cwc.content_map.get_destination(file_extension)
        print("The '%s' file extension is mapped to the '%s' content folder" % (file_extension, catalog_destination))
    
    def create_tag(self, args):
        """ Creates a tag to attach to files checked into the specified catalog. """
               
        print("Please specify a tag")
        tag_name = self.input_prompt('tag')
        
        self.cwc.db.add_tag(catalog.Tag(tag_name))
        print("The '%s' tag created" % tag_name)

    def do_remove(self, line):
        """ Removes a file extension mapping from the specified catalog. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.set_cwc(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if self.cwc is None:
            self.print_specify_catalog()
        elif args[constants.MAP_ARGUMENT_LONG_NAME]:
            self.remove_map(args)
        elif args[constants.TAG_ARGUMENT_LONG_NAME]:
            self.remove_tag(args)
        elif args[constants.FILE_ARGUMENT_LONG_NAME]:
            self.remove_file(args)
        else:
            print("Nothing to remove!")    
        
    def remove_map(self, args):
        """ Removes a file extension map from the current working catalog. """
        
        print("Please specify a file extension")
        file_extension = self.input_prompt('file extension')
        
        if file_extension[0] == '.':
            file_extension = file_extension[1:]
            
        try:
            self.cwc.content_map.remove(file_extension)
            print("File extension map successfully removed!")
        except KeyError:
            print("The '%s' file extension not mapped in the '%s' catalog" % (file_extension, self.cwc.name))

    def remove_tag(self, args):
        """ Removes a tag """
        
        print("Please specify a tag")
        tag_name = self.input_prompt('tag')
        
        self.cwc.db.remove_tag(catalog.Tag(tag_name))
        print("Tag successfully removed!")

    def remove_file(self, args):
        """ Removes a file """

        print("Please specify the content path for the file")
        content_path = self.input_prompt('content path')
                    
        self.cwc.remove_file(content_path)
        print("File successfully removed!")

    def do_establish(self, line):
        """ Establishes a new catalog at the specified path. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        catalog_path = args[constants.PATH_ARGUMENT_LONG_NAME]
        
        if catalog_path:
            catalog_path = catalog_path[0]
        
        while not os.path.isabs(catalog_path):
            print("Please specify an absolute OS path for the catalog")
            catalog_path = self.input_prompt('catalog')    
         
        self.cwc = catalog.establish(catalog_path, args[constants.SCHEMA_ARGUMENT_LONG_NAME])
        print("The '%s' catalog established at: '%s'" % (self.cwc.name, self.cwc.path))
        print("The current working catalog set to: '%s'" % self.cwc.name)

    def do_destroy(self, line):
        """ Destroys or deletes a catalog at the specified path. This will delete all of the files as well. """
        
        args = vars(self.parser.parse_args(line.split()))
        
        catalog_path = args[constants.PATH_ARGUMENT_LONG_NAME]
        
        if catalog_path:
            catalog_path = catalog_path[0]
        else:
            print("Please specify an absolute OS path for the catalog")
            catalog_path = self.input_prompt('catalog')
        
        if catalog.is_catalog(catalog_path):
            destroy_catalog = catalog.Catalog(catalog_path)
            
            print("All files will be lost and this cannot be undone!")
            print("Are you sure you want to destroy the '%s' catalog?" % destroy_catalog.name)
            
            acceptable_answer = False
            while not acceptable_answer:
                response = self.input_prompt('Yes or No').lower()
            
                if response == 'yes':
                    catalog.destroy(destroy_catalog)
                    
                    if self.cwc:
                        if self.cwc.path == destroy_catalog.path:
                            self.cwc = None
                    
                    print("The catalog has been destroyed!")
                    acceptable_answer = True                    
                elif response == 'no':
                    print("Good choice!")
                    acceptable_answer = True                    
                else:
                    acceptable_answer = False
        else:
            print("The path is not to a " + constants.APPLICATION_NAME + " catalog")
    
    def do_checkin(self, line):
        """ Checks in the current working file into the current working catalog """
    
        args = vars(self.parser.parse_args(line.split()))    
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.set_cwc(args[constants.CATALOG_ARGUMENT_LONG_NAME])
                            
        if self.cwc is None:
            self.print_specify_catalog()
        else:            
            file_path = args[constants.PATH_ARGUMENT_LONG_NAME]
            
            if file_path:
                file_path = file_path[0]
            else:
                print("Please specify a file by its OS path")
                file_path = self.input_prompt('file')
                
            print("Please enter a title for the file")
            title = self.input_prompt('title')
            
            while True:
                try: 
                    self.cwf = self.cwc.checkin(file_path, title)
                      
                    if args[constants.VERBOSE_ARGUMENT_LONG_NAME]:
                        print("File successfully checked in as:")
                        self.print_catalog_files_table([self.cwf])
                    else:
                        print("File successfully checked in!")
                        
                except LookupError:
                    print("The '%s' file extension is unknown for the '%s' catalog." % (self.cwf.extension, self.cwc.name))
                    print("Would you like to add the '%s' file extension to the '%s' catalog?" % (self.cwf.extension, self.cwc.name))
                    response = self.input_prompt('Y/Yes or N/No')
                    
                    if response == 'Y' or response == 'Yes':
                        
                        print("Please specify a folder path relative to the content folder for the '%s' file extension." % self.cwf.extension)
                        destination = self.input_prompt('content path')
                        
                        while os.path.isabs(response):
                            print("The path must be relative to the content folder. Please try again.")
                            response = input('content path')
                           
                        self.cwc.content_map.add(self.cwf.extension, destination)
                        continue
                    else:
                        print("The file was not checked in")
                break
    
    def do_list(self, line):
        """ Lists various properties and values for the specified catalog """
        
        args = vars(self.parser.parse_args(line.split()))
        
        if args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            self.set_cwc(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        
        if self.cwc is None:
            self.print_specify_catalog()
        elif args[constants.MAP_ARGUMENT_LONG_NAME]:
            self.list_maps(args)
        elif args[constants.TAG_ARGUMENT_LONG_NAME]:
            self.list_tags(args)
        elif args[constants.FILE_ARGUMENT_LONG_NAME]:
            self.list_files(args)
        else:
            print("Nothing to list!")
    
    def list_maps(self, args):
        """ Shows the file extension maps in an ASCII table sorted in descending alphabetical order """
        
        map_table = PrettyTable([constants.FILE_EXTENSION_HEADER_NAME, constants.CONTENT_FOLDER_HEADER_NAME])
        map_table.align[constants.CONTENT_FOLDER_HEADER_NAME] = constants.CONTENT_FOLDER_HEADER_ALIGNMENT
        parent_path = None
        file_map = self.cwc.content_map.map
                
        if args[constants.VERBOSE_ARGUMENT_LONG_NAME]:
            parent_path = os.path.join(self.cwc.path, constants.CONTENT_FOLDER_NAME)
                
        for file_extension in sorted(file_map):
            row = [file_extension, os.path.join(parent_path, file_map[file_extension])]
            map_table.add_row(row)        
                    
        print(map_table)
    
    def list_tags(self, args):
        """ Shows all of the tags in an ASCII table sorted in descending alphabetical order """
        
        table_headers = [constants.TAG_HEADER_NAME] 
        
        tags_table = PrettyTable(table_headers)
        
        tags = self.cwc.db.get_all_tags()
        
        for tag in tags:
            row = [tag.name]
            tags_table.add_row(row)
        
        print(tags_table)
    
    def list_files(self, args):
        """ Shows all of the files in an ASCII table sorted in descending alphabetical order """
                
        files = self.cwc.db.get_all_files()
                   
        self.print_catalog_files_table(files, args[constants.VERBOSE_ARGUMENT_LONG_NAME])
    
    def do_exit(self, line):
        """ Safely exits the console or interactive mode. """
        
        if self.cwc is not None:
            self.cwc.db.disconnect()
        
        return True
    
    def do_quit(self, line):
        """ Safely exits the console or interactive mode. """
        
        return self.do_exit(line)