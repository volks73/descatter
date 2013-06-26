from prettytable import PrettyTable

from catalog import CatalogError

import argparse
import cmd
import os 
import re

import constants
import catalog

class InputError(ValueError): pass

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
    
    intro = constants.CONSOLE_INTRODUCTION
    prompt = constants.CONSOLE_PROMPT
    
    def __init__(self, catalog=None, file=None):
        
        self.current_working_catalog = catalog
        self.current_working_file = file
        
        self.parser = argparse.ArgumentParser(description=constants.CONSOLE_DESCRIPTION)
        
        self.parser.add_argument(constants.FIRST_ARGUMENT_LONG_NAME,  
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
    
    def create_catalog_files_table(self, catalog_files, verbose=False):
        
        table_headers = [constants.ID_HEADER_NAME,
                         constants.TITLE_HEADER_NAME,
                         constants.CONTENT_PATH_HEADER_NAME,
                         constants.CONTENT_NAME_HEADER_NAME]
        
        if verbose:
            table_headers.append(constants.ORIGINAL_PATH_HEADER_NAME)
            table_headers.append(constants.ORIGINAL_NAME_HEADER_NAME) 
        
        catalog_files_table = PrettyTable(table_headers)
        catalog_files_table.align[constants.TITLE_HEADER_NAME] = constants.TITLE_HEADER_ALIGNMENT
        catalog_files_table.align[constants.CONTENT_PATH_HEADER_NAME] = constants.CONTENT_PATH_HEADER_ALIGNMENT
        
        for catalog_file in catalog_files:
            row = [catalog_file.id,
                   catalog_file.title,
                   catalog_file.content_path,
                   catalog_file.content_name]
            
            if verbose:
                row.append(catalog_file.original_path)
                row.append(catalog_file.original_name)
            
            catalog_files_table.add_row(row)
        
        return catalog_files_table
    
    def create_catalog_table(self, catalog, verbose):
        
        table_headers = [constants.NAME_HEADER_NAME]
        
        if verbose:
            table_headers.append(constants.PATH_HEADER_NAME)
        
        catalog_table = PrettyTable(table_headers)
        
        row = [catalog.name]
        
        if verbose:
            row.append(catalog.path)
        
        catalog_table.add_row(row)
        
        return catalog_table
    
    def print_current_working_catalog(self, verbose=False):
        
        if self.current_working_catalog is None:
            print("No current working catalog has been set!")
        else:
            print("Current working catalog set to:")
            print(self.create_catalog_table(self.current_working_catalog, verbose))
            
    def print_current_working_file(self, verbose=False):
        
        if self.current_working_file is None:
            print("No current working file has been set!")
        else:
            print("Current working file set to:")
            print(self.create_catalog_files_table((self.current_working_file,), verbose))    
    
    def prompt_generic(self, value, input_method):
        
        prompt = (constants.CONSOLE_PROMPT_PREFIX + 
                  value + 
                  constants.CONSOLE_PROMPT_SUFFIX + 
                  constants.CONSOLE_PROMPT_TERMINATOR)
        
        # TODO: Add a cancel option
        
        return input_method(prompt)
    
    def prompt_yes_or_no(self, input_method):
               
        return self.sanitize_yes_or_no_input(self.prompt_generic('(Y)es or (N)o', input_method))

    def prompt_path(self, input_method):
        
        print("Please specify a path")
        user_input = self.prompt_generic('path', input_method)
        
        return self.sanitize_folder_path_input(user_input)

    def prompt_catalog_path(self, input_method):
        
        print("Please specify a path to the catalog")
        user_input = self.prompt_generic('catalog path', input_method)
        
        return self.sanitize_catalog_path_input(user_input)

    def prompt_file_paths(self, input_method):
        
        print("Please specify the path(s) to the file(s)")
        user_input = self.prompt_generic('file path(s)', input_method)
        
        return self.sanitize_file_paths_input(user_input)
    
    def prompt_catalog_file_id(self, input_method):
        
        print("Please specify the ID for the catalog file")
        user_input = self.prompt_generic('ID', input_method)
        
        return self.sanitize_catalog_file_id_input(user_input)
        
    def prompt_catalog_file_ids(self, input_method):
        
        print("Please specify the ID(s) for the catalog file(s)")
        user_input = self.prompt_generic('ID(s)', input_method)
    
        return self.sanitize_catalog_file_ids_input(user_input)

    def prompt_tags(self, input_method):
        
        print("Please specify the tag(s)")
        user_input = self.prompt_generic('tag(s)', input_method)
        
        return self.sanitize_tags_input(user_input)
    
    def prompt_file_extensions(self, input_method):
        
        print("Please specify the file extension(s)")
        user_input = self.prompt_generic('file extension', input_method)
        
        return self.sanitize_file_extensions_input(user_input)
    
    def prompt_title(self, file_path, input_method):
        
        print("Please enter a title for: %s" % os.path.basename(file_path))
        user_input = self.prompt_generic('title', input_method)
        
        return self.sanitize_title_input(user_input)
    
    def sanitize_user_input(self, user_input):
        
        if user_input is None:
            raise ValueError("User input is 'None'")
        elif user_input:
            return user_input.strip()
        else:
            raise InputError("No user input")
    
    def sanitize_yes_or_no_input(self, user_input):
        
        response = self.sanitize_user_input(user_input).lower()
        
        if response == 'yes' or response == 'y':
            return True
        elif response == 'no' or response == 'n':
            return False                                 
        else:
            raise InputError("Not (Y)es or (N)o")
    
    def sanitize_folder_path_input(self, user_input):
        
        folder_path = os.path.abspath(self.sanitize_user_input(user_input))
        basename = os.path.basename(folder_path)
        
        if not basename:
            basename = os.path.basename(os.path.dirname(folder_path))
        
        if re.search(r'[^A-Za-z0-9_\-\\]', basename) or os.path.isfile(folder_path): 
            raise InputError("Invalid folder path")
        else:
            return folder_path
    
    def sanitize_catalog_path_input(self, user_input):
        
        catalog_path = self.sanitize_folder_path_input(user_input)
           
        if os.path.isdir(catalog_path):
            
            if catalog.is_catalog(catalog_path):
                return catalog_path
            else:
                raise InputError("Path is not to a %s catalog" % constants.APPLICATION_NAME)
        else:
            raise InputError("Path is not to a folder")

    def sanitize_file_path_input(self, user_input):
        
        file_path = os.path.normcase(os.path.abspath(self.sanitize_user_input(user_input)))
        if os.path.isfile(file_path):
            return file_path
        else:
            raise InputError("Not a file path")

    def sanitize_file_paths_input(self, user_input):
        
        file_paths = self.sanitize_user_input(user_input).split(constants.LIST_SEPARATOR)
        
        return tuple([self.sanitize_file_path_input(file_path) for file_path in file_paths])

    def sanitize_catalog_file_ids_input(self, user_input):
        
        catalog_file_ids = self.sanitize_user_input(user_input).split(constants.LIST_SEPARATOR)
            
        return tuple([self.sanitize_catalog_file_id_input(catalog_file) for catalog_file in catalog_file_ids])
    
    def sanitize_catalog_file_id_input(self, user_input):
        
        # TODO: Add check for id in database
        
        return self.sanitize_user_input(user_input)

    def sanitize_tag_input(self, user_input):
        
        return self.sanitize_user_input(user_input)

    def sanitize_tags_input(self, user_input):
        
        tags = self.sanitize_user_input(user_input).split(constants.LIST_SEPARATOR)
            
        return tuple([self.sanitize_tag_input(tag) for tag in tags])

    def sanitize_file_extension_input(self, user_input):
        
        file_extension = self.sanitize_user_input(user_input)
        
        if file_extension[0] == '.':
            file_extension = file_extension[1:]
            
        return file_extension

    def sanitize_file_extensions_input(self, user_input):
        
        file_extensions = self.sanitize_user_input(user_input).split(constants.LIST_SEPARATOR)
                
        return tuple([self.sanitize_file_extension_input(file_extension) for file_extension in file_extensions])
    
    def sanitize_title_input(self, user_input):
        
        return self.sanitize_user_input(user_input)

    def get_working_catalog(self, args, input_method):
        
        working_catalog = None
        catalog_path = args[constants.CATALOG_ARGUMENT_LONG_NAME]
        
        if catalog_path:
            catalog_path = self.sanitize_catalog_path_input(catalog_path)
            working_catalog = catalog.Catalog(catalog_path)
        elif self.current_working_catalog is None:
            catalog_path = self.prompt_catalog_path(input_method)
            working_catalog = catalog.Catalog(catalog_path)
        else:
            working_catalog = self.current_working_catalog
        
        return working_catalog
    
    def get_catalog_file_ids(self, args, input_method):
        
        catalog_file_ids = args[constants.FIRST_ARGUMENT_LONG_NAME]
            
        if catalog_file_ids:
            catalog_file_ids = self.sanitize_catalog_file_ids_input(catalog_file_ids[0])
        elif self.current_working_file is None:
            catalog_file_ids = self.prompt_catalog_file_ids(input_method)
        else:
            catalog_file_ids = (self.current_working_file.id,)
        
        return catalog_file_ids

    def get_tag_names(self, args):
        
        tag_names = args[constants.FIRST_ARGUMENT_LONG_NAME]
        
        if tag_names:
            tag_names = tag_names[0]
            tag_names = self.sanitize_tags_input(tag_names)
        else:
            tag_names = self.prompt_tags()
        
        return tag_names
    
    def get_file_extensions(self, args):
        
        file_extensions = args[constants.FIRST_ARGUMENT_LONG_NAME]
        
        if file_extensions:
            file_extensions = self.sanitize_file_extensions_input(file_extensions[0])
        else:
            file_extensions = self.prompt_file_extensions()
        
        return file_extensions
    
    def get_folder_path(self, args, input_method):
        
        folder_path = args[constants.FIRST_ARGUMENT_LONG_NAME]
        
        if folder_path:
            folder_path = self.sanitize_folder_path_input(folder_path[0])
        else:
            folder_path = self.prompt_path(input_method)
        
        return folder_path            
    
    def get_catalog_path(self, args, input_method):
        
        catalog_path = args[constants.FIRST_ARGUMENT_LONG_NAME]
        
        if catalog_path:
            catalog_path = self.sanitize_catalog_path_input(catalog_path[0])
        elif args[constants.CATALOG_ARGUMENT_LONG_NAME]:
            catalog_path = self.sanitize_catalog_path_input(args[constants.CATALOG_ARGUMENT_LONG_NAME])
        else:
            catalog_path = self.prompt_catalog_path(input_method)
        
        return catalog_path

    def get_catalog_file_id(self, args, input_method):
        
        catalog_file_id = args[constants.FIRST_ARGUMENT_LONG_NAME]
        
        if catalog_file_id:
            catalog_file_id = self.sanitize_catalog_file_id_input(catalog_file_id[0])
        else:
            catalog_file_id = self.prompt_catalog_file_id(input_method)
        
        return catalog_file_id

    def get_file_paths(self, args, input_method):
        
        file_paths = args[constants.FIRST_ARGUMENT_LONG_NAME]
            
        if file_paths:
            file_paths = self.sanitize_file_paths_input(file_paths[0])
        else:
            file_paths = self.prompt_file_paths(input_method)
        
        return file_paths
        
    def get_args(self, line):
        
        return vars(self.parser.parse_args(line.split()))
    
    def set_current_working_catalog(self, catalog, verbose=False):
        
        self.current_working_catalog = catalog
        self.print_current_working_catalog(verbose)
    
    def set_current_working_file(self, catalog_file, verbose=False):
        
        self.current_working_file = catalog_file
        self.print_current_working_file(verbose)

    def tag_file(self, catalog_file_id):
        
        tagged_file = self.current_working_catalog.file(catalog_file_id)
                
        if tagged_file is None:
            print("No catalog file found with ID: '%s'" % catalog_file_id)
        else:    
            print("Tagging catalog file: '%s'" % tagged_file.title)   
                    
            for tag_name in self.prompt_tags():
                self.current_working_catalog.tag(tagged_file, tag_name)
                        
            print("The '%s' catalog file successfully tagged!" % tagged_file.title)
            
        return tagged_file
    
    def detag_file(self, catalog_file_id):
        
        detagged_file = self.current_working_catalog.file(catalog_file_id)
               
        if detagged_file is None:
            print("No catalog file found with ID: '%s'" % catalog_file_id)
        else:
            print("Detagging catalog file: '%s'" % detagged_file.title)
                                
            for tag_name in self.prompt_tags():
                self.current_working_catalog.detag(detagged_file, tag_name)
                    
            print("The '%s' catalog file successfully detagged!" % detagged_file.title)
        
        return detagged_file
    
    def create_map(self, args):
        """ Creates a file extension map for the specified catalog. """
        
        file_extensions = self.get_file_extensions(args)
        
        for file_extension in file_extensions:
            print("Please specify a content path for the '%s' file extension." % file_extension)
            destination = self.prompt_generic("content folder path")
                
            self.current_working_catalog.content_map.add(file_extension, destination)
            
            catalog_destination = self.current_working_catalog.content_map.get_destination(file_extension)
            print("The '%s' file extension is mapped to the '%s' content folder" % (file_extension, catalog_destination))
    
    def create_tag(self, args):
        """ Creates a tag to attach to files checked into the specified catalog. """
                       
        for tag_name in self.get_tag_names(args):
            self.current_working_catalog.create_tag(tag_name)
            print("The '%s' tag created" % tag_name)
    
    def remove_map(self, args):
        """ Removes a file extension map from a catalog. """
        
        file_extensions = self.get_file_extensions(args)
           
        for file_extension in file_extensions: 
            try:
                self.current_working_catalog.content_map.remove(file_extension)
                print("File extension map successfully removed!")
            except KeyError:
                print("The '%s' file extension is not mapped in the '%s' catalog" % (file_extension, self.current_working_catalog.name))

    def remove_tag(self, args):
        """ Removes a tag from a catalog. """
               
        for tag_name in self.get_tag_names(args):
            self.current_working_catalog.remove_tag(tag_name)
            print("The '%s' tag successfully removed!" % tag_name)
    
    def remove_file(self, args):
        """ Removes a catalog file from a catalog. """

        print("Removing files from a catalog cannot be undone!")
           
        for catalog_file_id in self.get_catalog_file_ids(args):
            remove_file = self.current_working_catalog.file(catalog_file_id)
                
            if remove_file is None:
                print("No catalog file found with ID: '%s'" % catalog_file_id)
            else:
                print("Are you sure you want to remove the '%s' file from the '%s' catalog?" % (remove_file.title, self.current_working_catalog.name))
                
                if self.prompt_yes_or_no():
                    self.current_working_catalog.remove_file(remove_file)
                    print("The '%s' catalog file successfully removed!" % remove_file.title)
                else:
                    print("Good choice!")

    def checkout_file(self, catalog_file_id):
        
        checkout_file = self.current_working_catalog.file(catalog_file_id)
                
        if checkout_file is None:
            print("No catalog file found with ID: '%s'" % catalog_file_id)
        else:
            print("Please enter a folder path for: %s" % checkout_file.title)
            dst_path = self.prompt_generic('path')
            
            dst_path = os.path.abspath(dst_path)
            
            self.current_working_catalog.checkout(checkout_file, dst_path)
            print("The '%s' catalog file successfully checked out!" % checkout_file.title)
        
        return checkout_file
    
    def list_maps(self, args):
        """ Shows the file extension maps in an ASCII table sorted in descending alphabetical order """
        
        map_table = PrettyTable([constants.FILE_EXTENSION_HEADER_NAME, constants.CONTENT_FOLDER_HEADER_NAME])
        map_table.align[constants.CONTENT_FOLDER_HEADER_NAME] = constants.CONTENT_FOLDER_HEADER_ALIGNMENT
        parent_path = None
        file_map = self.current_working_catalog.content_map.map
                
        if args[constants.VERBOSE_ARGUMENT_LONG_NAME]:
            parent_path = os.path.join(self.current_working_catalog.path, constants.CONTENT_FOLDER_NAME)
                
        for file_extension in sorted(file_map):
            row = [file_extension, os.path.join(parent_path, file_map[file_extension])]
            map_table.add_row(row)        
                    
        print(map_table)
    
    def list_tags(self, args):
        """ Shows all of the tags in an ASCII table sorted in descending alphabetical order """
        
        table_headers = None
        
        if args[constants.VERBOSE_ARGUMENT_LONG_NAME]:
            table_headers = [constants.ID_HEADER_NAME, constants.TAG_HEADER_NAME] 
        else:
            table_headers = [constants.TAG_HEADER_NAME]
        
        tags_table = PrettyTable(table_headers)
        
        tags = self.current_working_catalog.tags()
        
        for tag in tags:
            row = None
            
            if args[constants.VERBOSE_ARGUMENT_LONG_NAME]:
                row = [tag.id, tag.name]
            else:
                row = [tag.name]
            
            tags_table.add_row(row)
        
        print(tags_table)
    
    def list_files(self, args):
        """ Shows all of the files in an ASCII table sorted in descending alphabetical order """
                                  
        print(self.create_catalog_files_table(self.current_working_catalog.files(), args[constants.VERBOSE_ARGUMENT_LONG_NAME]))
    
    def do_cwc(self, line=''):
        """ Displays the current working catalog. """
        
        args = self.get_args(line)
        self.print_current_working_catalog(args[constants.VERBOSE_ARGUMENT_LONG_NAME])
        
    def do_cwf(self, line=''):
        """ Displays the current working file. """
        
        args = self.get_args(line)
        self.print_current_working_file(args[constants.VERBOSE_ARGUMENT_LONG_NAME])    
    
    def do_cwd(self, line):
        """ Displays the current working directory. """
        
        print("Current working directory is: %s" % os.getcwd())
    
    def do_catalog(self, line, input_method=input):
        """ Sets the current working catalog. """
        
        args = self.get_args(line)
        catalog_path = self.get_catalog_path(args, input_method)
        
        if catalog.is_catalog(catalog_path):
            self.set_current_working_catalog(catalog.Catalog(catalog_path), args[constants.VERBOSE_ARGUMENT_LONG_NAME])
        else:
            print("The path is not to a " + constants.APPLICATION_NAME + " catalog")
            
        # TODO: Add saving a history of catalogs used in User home directory installation of descatter
    
    def do_checkin(self, line, catalog_input=input, file_paths_input=input, title_input=input):
        """ Checks in the current working file into the current working catalog """
    
        try:
            args = self.get_args(line)
            catalog = self.get_working_catalog(args, catalog_input)
            self.set_current_working_catalog(catalog)            
            checked_in_files = []
            
            for file_path in self.get_file_paths(args, file_paths_input):
                title = self.prompt_title(file_path, title_input)
                checked_in_file = catalog.checkin(file_path, title)
                
                if checked_in_file is not None:
                    checked_in_files.append(checked_in_file)    
                
            if checked_in_files:
                verbose = args[constants.VERBOSE_ARGUMENT_LONG_NAME]
                
                print("Files successfully checked in to '%s' as:" % catalog.name)    
                print(self.create_catalog_files_table(checked_in_files, verbose))
                self.set_current_working_file(checked_in_files[-1])
        except InputError as error:
            print(str(error))
    
    def do_file(self, line, input_method=input):
        """ Sets the current working file. """
        
        args = self.get_args(line)
        catalog = self.get_working_catalog(args)
        
        if catalog:
            catalog_file = catalog.file(self.get_catalog_file_id(input_method))
            
            if catalog_file:   
                self.set_current_working_file(catalog_file, args[constants.VERBOSE_ARGUMENT_LONG_NAME])
                self.set_current_working_catalog(catalog, args[constants.VERBOSE_ARGUMENT_LONG_NAME])
            else:
                print("The ID is not to a catalog file in the '%s' catalog" % catalog.name)
        else:
            raise InputError("No catalog specified", catalog) 
            
        # TODO: Add history of recently used files

    def do_tag(self, line):
        """ Tags one or more files """
        
        args = self.get_args(line)
        catalog = self.get_working_catalog(args)
        
        if catalog:
            self.set_current_working_catalog(catalog)
            last_tagged_file = None    
            
            for catalog_file_id in self.get_catalog_file_ids(args):
                last_tagged_file = self.tag_file(catalog_file_id)
            
            if last_tagged_file is not None:
                self.set_current_working_file(last_tagged_file)
        else:
            raise InputError("No catalog specified", catalog)
    
    def do_detag(self, line):
        """ Detags one or more files """
        
        args = self.get_args(line)
        catalog = self.get_working_catalog(args)
                        
        if catalog:
            self.set_current_working_catalog(catalog)
            last_detagged_file = None
            
            for catalog_file_id in self.get_catalog_file_ids(args):
                last_detagged_file = self.detag_file(catalog_file_id)
            
            if last_detagged_file is not None:
                self.set_current_working_file(last_detagged_file)
        else:
            raise InputError("No catalog specified", catalog)
    
    def do_create(self, line):
        """ Sub-command to create file extension maps and tags. """
        
        try:
            args = self.get_args(line)
            catalog = self.get_working_catalog(args, input) 
    
            if catalog:
                self.set_current_working_catalog(catalog)
                
                if args[constants.MAP_ARGUMENT_LONG_NAME]:
                    self.create_map(args)
                elif args[constants.TAG_ARGUMENT_LONG_NAME]:
                    self.create_tag(args)
                else:
                    # TODO: Change to prompt for (M)ap or (T)ag
                    print("Nothing to create!")
            else:
                raise InputError("No catalog specified", catalog)
        except InputError as error:
            print(error.message)

    def do_remove(self, line):
        """ Sub-command to remove file extension maps, tags, and files from a catalog. """
        
        args = self.get_args(line)
        catalog = self.get_working_catalog(args)
               
        if catalog:
            self.set_current_working_catalog(catalog)
            
            if args[constants.MAP_ARGUMENT_LONG_NAME]:
                self.remove_map(args)
            elif args[constants.TAG_ARGUMENT_LONG_NAME]:
                self.remove_tag(args)
            elif args[constants.FILE_ARGUMENT_LONG_NAME]:
                self.remove_file(args)
            else:
                # TODO: Change to prompt for (M)ap or (T)ag or (F)ile
                print("Nothing to remove!")
        else:
            raise InputError("No catalog specified", catalog)  

    def do_establish(self, line, input_method=input):
        """ Establishes a new catalog at the specified path. """
        
        try:
            args = self.get_args(line)
            folder_path = self.get_folder_path(args, input_method)
            
            schema_path = None
            if args[constants.SCHEMA_ARGUMENT_LONG_NAME] is not None:
                schema_path = self.sanitize_file_path_input(args[constants.SCHEMA_ARGUMENT_LONG_NAME])
                        
            established_catalog = catalog.create(folder_path, schema_path)
            print("Catalog established!")
            self.set_current_working_catalog(established_catalog, args[constants.VERBOSE_ARGUMENT_LONG_NAME])
        except InputError as error:
            print(str(error))

    def do_destroy(self, line, catalog_path_input=input, yes_or_no_input=input):
        """ Destroys or deletes a catalog at the specified path. This will delete all of the files as well. """
                
        try:
            args = self.get_args(line)
            catalog_path = self.get_catalog_path(args, catalog_path_input)
            
            print("All files will be lost and this cannot be undone!")
            print("Are you sure you want to destroy the catalog?")
            
            if self.prompt_yes_or_no(yes_or_no_input):
                catalog.destroy(catalog_path)
                    
                if self.current_working_catalog is not None:
                    if self.current_working_catalog.path == catalog_path:
                        self.current_working_catalog = None
            else:
                print("Good choice!")
        except InputError as error:
            print(str(error))
    
    def do_checkout(self, line, catalog_input=input, file_ids_input=input):
        """ Copies a catalog file to its original path and name in the file system """
        
        try:
            args = self.get_args(line)                      
            catalog = self.get_working_catalog(args, catalog_input)
            checked_out_files = []
                
            for catalog_file_id in self.get_catalog_file_ids(args, file_ids_input):
                checked_out_file = catalog.checkout(catalog_file_id)
                    
                if checked_out_file is not None:
                    checked_out_files.append(checked_out_file)
            
            if checked_out_files:
                verbose = args[constants.VERBOSE_ARGUMENT_LONG_NAME]
                    
                print("Files successfully checked in to '%s' as:" % catalog.name)    
                print(self.create_catalog_files_table(checked_out_files, verbose))
                self.set_current_working_file(checked_out_files[-1])
        except InputError as error:
            print(str(error))
        except CatalogError as error:
            print(str(error))
    
    def do_find(self, line):
        """ Finds files based on specified tags. """
        
        args = self.get_args(line)
        
        if self.get_working_catalog(args):
            tag_names = self.get_tag_names(args)
                
            files = self.current_working_catalog.get_files_by_tags(tag_names)
            print(self.create_catalog_files_table(files, args[constants.VERBOSE_ARGUMENT_LONG_NAME]))
    
    def do_list(self, line):
        """ Lists various properties and values for the specified catalog """
        
        args = self.get_args(line)
        
        if self.get_working_catalog(args):
            if args[constants.MAP_ARGUMENT_LONG_NAME]:
                self.list_maps(args)
            elif args[constants.TAG_ARGUMENT_LONG_NAME]:
                self.list_tags(args)
            elif args[constants.FILE_ARGUMENT_LONG_NAME]:
                self.list_files(args)
            else:
                print("Nothing to list!")
    
    def do_exit(self, line):
        """ Safely exits the console or interactive mode. """
        
        return True
    
    def do_quit(self, line):
        """ Safely exits the console or interactive mode. """
        
        return self.do_exit(line)