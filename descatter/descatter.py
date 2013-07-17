from lxml import etree
from datetime import datetime

import os

class FilerError(Exception): pass
class PathFinderError(Exception):
    
    def __init__(self, message, path):
        super().__init__(message)
        self.path = path
    
class TaggerError(Exception): pass

class Filer(object):
    # Responsible for placing files into folders based on direction from the PathFinder
    # Needs to create a ".descatter" hidden folder in the base folder. This hidden
    # folder contains the tags SQLite database, templates for metadata, and schema definition.
    
    def __init__(self, base_folder_path, schema_file_path):
        self.base_folder_path = base_folder_path
        self.path_finder = PathFinder(schema_file_path)
        
        # TODO: Check if .descatter folder exists
        # TODO: Create .descatter hidden folder
        # TODO: Copy schema definition file to hidden folder
    
    def file(self, os_file_path, delete_source=False):
        destination_path = self.path_finder.find_path(os_file_path)
        # TODO: Finish implementing. After determining the destination path, the folder structure to the destination
        # needs to be created. Any temp folders and files must be created and replaced in the path. Then, copy
        # file.
        
        # TODO: Implement deleting source file
    
    def batch_file(self, os_folder_path):
        # TODO: Add filing of all files in the folder
        pass
    
    def recursive_batch_file(self, os_folder_path):
        # TODO: Add filing of all files in the folder and every subfolder. 
        pass
            
class PathFinder(object):
    
    # XML    
    NAMESPACE = 'descatter/2013/content_schema/1.0'
    PREFIX = 'ds'
    XPATH_NAMESPACE = {PREFIX: NAMESPACE}
        
    # Tags
    AUTHOR_TAG = 'author'
    DESCRIPTION_TAG = 'description'
    DESTINATION_TAG = 'destination'
    DESTINATIONS_TAG = 'destinations'
    EMAIL_TAG = 'email'
    FILE_TAG = 'file'
    FOLDER_TAG = 'folder'
    GROUP_TAG = 'group'
    INFO_TAG = 'info'
    MACRO_TAG = 'macro'
    MACROS_TAG = 'macros'
    METADATA_TAG = 'metadata'
    NAME_TAG = 'name'
    TEXT_TAG = 'text'
    TITLE_TAG = 'title'
    
    # Attributes
    CASE_ATTRIBUTE = 'case'
    CASE_SENSITIVE_ATTRIBUTE = 'case-sensitive'
    CONDITION_ATTRIBUTE = 'conditions'
    MACRO_ATTRIBUTE = 'macro'
    MATCH_ATTRIBUTE = 'match'
    NAME_ATTRIBUTE = 'name'
    PREFIX_ATTRIBUTE = 'prefix'
    RANDOM_ATTRIBUTE = 'random'
    REPLACE_SPACES_WITH_ATTRIBUTE = 'replace-spaces-with'
    SUFFIX_ATTRIBUTE = 'suffix'
    TEMPLATE_ATTRIBUTE = 'template'
    USE_ATTRIBUTE = 'use'
    VALUE_ATTRIBUTE = 'value'
    VARIABLE_ATTRIBUTE = 'variable'
        
    # Condition options
    ANY_WILDCARD = '*'
    EQUALS_CONDITION = 'equals'
    GREATER_THAN_CONDITION = 'greater-than'
    LESS_THAN_CONDITION = 'less-than'
    
    # Case options
    CASE_LOWER = 'lower'
    CASE_TITLE = 'title'
    CASE_UPPER = 'upper'
    
    # Standard Variables
    
    FILE_COUNT = 'file-count'
    FILE_EXTENSION = 'file-extension'
    FILE_DATE_ACCESSED = 'file-date-accessed'
    FILE_DATE_ADDED = 'file-date-added'
    FILE_DATE_CREATED = 'file-date-created' 
    FILE_DATE_MODIFIED = 'file-date-modified'
    FILE_INDEX = 'file-index'
    FILE_NAME = 'file-name'
    FILE_PATH = 'file-path'
    FILE_SIZE = 'file-size'
    
    def __init__(self, schema_file_path):
        
        self.root = etree.parse(self.schema_file_path).getroot()
        self.standard_variables = {}
        
        self.get_macro_elements = etree.XPath(("//" +
                                               self.PREFIX +
                                               ":" + 
                                               self.MACROS_TAG +
                                               "/" +
                                               self.PREFIX +
                                               ":" +
                                               self.MACRO_TAG),
                                              namespaces=self.XPATH_NAMESPACE)
               
        self.get_use_attribute = etree.XPath(("//" + 
                                              self.PREFIX + 
                                              ":" + 
                                              self.DESTINATIONS_TAG + 
                                              "/@" + 
                                              self.USE_ATTRIBUTE), 
                                             namespaces=self.XPATH_NAMESPACE)
        
        self.get_destination_elements = etree.XPath(("//" +
                                                     self.PREFIX +
                                                     ":" +
                                                     self.DESTINATIONS_TAG +
                                                     "/" +
                                                     self.PREFIX +
                                                     ":" +
                                                     self.DESTINATION_TAG),
                                                    namespaces=self.XPATH_NAMESPACE)
        
        self.get_folder_elements = etree.XPath(("/" +
                                                self.PREFIX +
                                                ":" +
                                                self.FOLDER_TAG), 
                                               namespaces=self.XPATH_NAMESPACE)
        
        self.get_text_elements = etree.XPath(("//" +
                                              self.PREFIX +
                                              ":" +
                                              self.MACROS_TAG +
                                              "/" +
                                              self.PREFIX +
                                              ":" +
                                              self.MACRO_TAG +
                                              "[@" +
                                              self.NAME_ATTRIBUTE +
                                              "=$name]/" +
                                              self.PREFIX +
                                              ":" +
                                              self.TEXT_TAG),
                                             namespace=self.XPATH_NAMESPACE)

        self.get_file_element = etree.XPath(("//" + 
                                             self.PREFIX + 
                                             ":" +
                                             self.FOLDER_TAG +
                                             "/" +
                                             self.FILE_TAG),
                                            namespace=self.XPATH_NAMESPACE)
        
        def condition_equals(self, match_value, use_value):
            
            return match_value == use_value
        
        def condition_greater_than(self, match_value, use_value):
            
            return match_value > use_value
        
        def condition_less_than(self, match_value, use_value):
            
            return match_value < use_value
        
        self.conditions = {self.EQUALS_CONDITION: condition_equals,
                           self.GREATER_THAN_CONDITION: condition_greater_than,
                           self.LESS_THAN_CONDITION: condition_less_than} 
        
        def text_value(self, text, text_element):
            
            return text_element.get(self.VALUE_ATTRIBUTE)
        
        def text_variable(self, text, text_element):
            
            text_variable = text_element.get(self.VARIABLE_ATTRIBUTE)
            return self.standard_variables[text_variable]
        
        def text_case(self, text, text_element):
            
            case = text_element.get(self.CASE_ATTRIBUTE)
        
            if case == self.CASE_LOWER:
                return text.lower()
            elif case == self.CASE_UPPER:
                return text.upper()
            elif case == self.CASE_TITLE:
                return text.title()
            else:
                return text
        
        def text_replace_spaces_with(self, text, text_element):
            
            space_replacement = text_element.get(self.REPLACE_SPACES_WITH_ATTRIBUTE)
            return text.replace(' ', space_replacement) 
        
        def text_prefix(self, text, text_element):
            
            prefix = text_element.get(self.PREFIX_ATTRIBUTE)
            return prefix + text
    
        def text_suffix(self, text, text_element):
            
            suffix = text_element.get(self.SUFFIX_ATTRIBUTE)
            return text + suffix
        
        self.text_attributes(text_case, text_replace_spaces_with, text_prefix, text_suffix)
    
    def find_path(self, os_file_path):
        
        path = None
        self.load_standard_variables(os_file_path)
        
        use_variable = self.get_use_attribute(self.root)[0]
        use_value = self.standard_variables[use_variable]
        destination_element = self.get_destination_element(use_value)
        
        if destination_element is None:
            raise PathFinderError("A destination could not be determined for the file", os_file_path)
        else:        
            folder_elements = self.get_folder_elements(destination_element)
                
            for folder_element in folder_elements:
                folder_name = self.get_folder_name(folder_element)
                path = os.path.join(path, folder_name)
            
            file_element = self.get_file_element(destination_element)
            file_name = self.get_file_name(file_element)
            
            path = os.path.join(path, file_name)
            
        return path
        
    def load_standard_variables(self, os_file_path):
        
        file_name, file_extension = os.path.splitext(os_file_path)
        file_name = os.path.basename(file_name)
        file_extension = file_extension[1:].strip().lower() 
        
        self.standard_variables[self.FILE_PATH] = os.path.dirname(os_file_path)
        self.standard_variables[self.FILE_NAME] = file_name
        self.standard_variables[self.FILE_EXTENSION] = file_extension
        self.standard_variables[self.FILE_SIZE] = os.path.getsize(os_file_path)
        self.standard_variables[self.FILE_DATE_CREATED] = os.path.getctime(os_file_path)
        self.standard_variables[self.FILE_DATE_MODIFIED] = os.path.getmtime(os_file_path)
        self.standard_variables[self.FILE_DATE_ACCESSED] = os.path.getatime(os_file_path)
        self.standard_variables[self.FILE_DATE_ADDED] = datetime.now()
        
        # TODO: Implement file_index and file_count for batch mode processing
        self.standard_variables[self.FILE_INDEX] = 1 # To be implemented later when the batch mode is finished
        self.standard_variables[self.FILE_COUNT] = 1
        
    def get_destination_element(self, use_value):
        
        destination_element = None
        destination_elements = self.get_destination_elements(self.root)
            
        for element in destination_elements:
            match_value = element.get(self.MATCH_ATTRIBUTE)
            match_condition = element.get(self.CONDITION_ATTRIBUTE)
            case_sensitive = element.get(self.CASE_SENSITIVE_ATTRIBUTE)
                
            if not case_sensitive:
                match_value = match_value.lower()
                use_value = use_value.lower()
                
            if self.conditions[match_condition](match_value, use_value):
                destination_element = element
                break
            
        return destination_element
    
    def get_text_from_element(self, text_element):
        
        text = None
        for attribute in self.text_attributes:
            text = attribute(text, text_element)
            
        return text
    
    def get_text_from_macro(self, name):
        
        text = None
        text_elements = self.get_text_elements(self.root, name=name)
        
        for text_element in text_elements:
            text = text + self.get_text_from_element(text_element)
        
        return text
    
    def get_folder_name(self, folder_element):
        
        name = folder_element.get(self.NAME_ATTRIBUTE)
        variable = folder_element.get(self.VARIABLE_ATTRIBUTE)
        macro = folder_element.get(self.MACRO_ATTRIBUTE)
        random = folder_element.get(self.RANDOM_ATTRIBUTE)
        
        # TODO: Add handling of unique-random-folder
        
        if name is not None:
            return name
        elif variable is not None:
            return self.standard_variables[variable]
        elif macro is not None:
            return self.get_text_from_macro(macro)
        elif random:
            # The '?-folder' is a flag to to create a unique, random folder name using the tempfile module 
            # The '?' is used because it is an invalid character for all operating systems
            # The folder cannot be created until the entire destination is determined. Once the file is
            # ready to copy into the destination, then the folders will be created and this will be 
            # replaced in the path with a random folder.
            return '?-folder'
        else:
            raise PathFinderError("Folder name could not be determined")
    
    def get_file_name(self, file_element):
        
        name = file_element.get(self.NAME_ATTRIBUTE)
        variable = file_element.get(self.VARIABLE_ATTRIBUTE)
        macro = file_element.get(self.MACRO_ATTRIBUTE)
        random = file_element.get(self.RANDOM_ATTRIBUTE)
        
        if name is not None:
            return name
        elif variable is not None:
            return self.standard_variables[variable]
        elif macro is not None:
            return self.get_text_from_macro(macro)
        elif random:
            # The '?-file' is a flag to create a random file name using the tempfile module
            # The '?' is used because it is an invalid character for all operating systems
            # The file name cannot be created until the entire desintaiton is determined. Once the file
            # is ready to copy into the desintation, then the file name will be generated.
            return '?-file'
        else:
            raise PathFinderError("File name could not be determined")

class ReFiler(object): pass
    # Responsible for searching the base folder and ensuring all files conform to the schema
    # or changing the structure if a new schema is selected.
    
class Tagger(object): pass
    # Responsible for tagging files and managing the database
    # Creates a hidden folder named ".descatter" in a folder and places a SQLite
    # database in the hidden folder. This stores the tags for all files in the
    # sub-folder of the base folder.

class Viewer(object): pass # Or maybe rename to Organizer
    # Graphical User Interface (GUI) to view a folder that has been descattered
    # A descattered folder has a hidden folder ".descatter" that contains
    # the tags database, templates for metadata, and schema definition and has all files
    # filed and organized according to a schema.
    
    # The viewer has four panes that can be re-sized and hidden as needed.
    # Left-most pane, or pane 1, is a file manager/explorer similar to Windows Explorer
    # with files and folders listed in various user selected views. Advanced features for
    # navigation will exist. Center pane, or pane 2, shows the tags database. This includes
    # a listing of all tags and virtual folders which the user can select and deselect
    # to show files and metadata in the right most pane, or pane 3. A search bar above the tag
    # listing allows for searching of files by tags and metadata. Pane 3 shows a list
    # of files based on selected tags. The files can be clicked on to expand the node and
    # show the metadata for the file. An advanced search option is also available. GUI
    # commands include filing, batch filing, re-filing, tagging, detagging, creating virtual
    # folders, export to csv, etc. If the folder selected in pane 1 is has not been descatter, 
    # the remaining two panes are empty and hidden to maximize the viewing the of file system view.
