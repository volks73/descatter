from lxml import etree
from datetime import datetime

import os

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
CONDITION_ATTRIBUTE = 'condition'
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
CURRENT_DATE = 'current-date'   
FILE_COUNT = 'file-count'
FILE_EXTENSION = 'file-extension'
FILE_DATE_ACCESSED = 'file-date-accessed'
FILE_DATE_CREATED = 'file-date-created' 
FILE_DATE_MODIFIED = 'file-date-modified'
FILE_INDEX = 'file-index'
FILE_NAME = 'file-name'
FILE_PATH = 'file-path'
FILE_SIZE = 'file-size'

# Random Placeholder
# The '?-folder' and '?-file' is a flag to to create a unique, random folder/file name using 
# the tempfile module. The '?' is used because it is an invalid character for all operating systems
# The folder cannot be created until the entire destination is determined. Once the file is
# ready to copy into the destination, then the folders will be created and this will be 
# replaced in the path with a random folder.
RANDOM_FILE_PLACEHOLDER = '?-file'
RANDOM_FOLDER_PLACEHOLDER = '?-folder'

class PathFinderError(Exception):
    
    def __init__(self, message, file_path):
        super().__init__(message)
        self.file_path = file_path

class PathFinder(object):
    
    def __init__(self, schema_file_path):
        
        schema_document = etree.parse(schema_file_path)
        self.root = schema_document.getroot()
        self.standard_variables = {}
        
        self.get_macro_elements = etree.XPath(("//" +
                                               PREFIX +
                                               ":" + 
                                               MACROS_TAG +
                                               "/" +
                                               PREFIX +
                                               ":" +
                                               MACRO_TAG),
                                              namespaces=XPATH_NAMESPACE)
               
        self.get_use_attribute = etree.XPath(("//" + 
                                              PREFIX + 
                                              ":" + 
                                              DESTINATIONS_TAG + 
                                              "/@" + 
                                              USE_ATTRIBUTE), 
                                             namespaces=XPATH_NAMESPACE)
        
        self.get_destination_elements = etree.XPath(("//" +
                                                     PREFIX +
                                                     ":" +
                                                     DESTINATIONS_TAG +
                                                     "/" +
                                                     PREFIX +
                                                     ":" +
                                                     DESTINATION_TAG),
                                                    namespaces=XPATH_NAMESPACE)
        
        self.get_folder_elements = etree.XPath((".//" +
                                                PREFIX +
                                                ":" +
                                                FOLDER_TAG), 
                                               namespaces=XPATH_NAMESPACE)
        
        self.get_text_elements = etree.XPath(("//" +
                                              PREFIX +
                                              ":" +
                                              MACROS_TAG +
                                              "/" +
                                              PREFIX +
                                              ":" +
                                              MACRO_TAG +
                                              "[@" +
                                              NAME_ATTRIBUTE +
                                              "=$name]/" +
                                              PREFIX +
                                              ":" +
                                              TEXT_TAG),
                                             namespaces=XPATH_NAMESPACE)

        self.get_file_element = etree.XPath((PREFIX + 
                                             ":" +
                                             FOLDER_TAG +
                                             "//" +
                                             PREFIX +
                                             ":" +
                                             FILE_TAG),
                                            namespaces=XPATH_NAMESPACE)
        
        def condition_equals(match_value, use_value):
            
            return match_value == use_value
        
        def condition_greater_than(match_value, use_value):
            
            return match_value > use_value
        
        def condition_less_than(match_value, use_value):
            
            return match_value < use_value
        
        self.conditions = {EQUALS_CONDITION: condition_equals,
                           GREATER_THAN_CONDITION: condition_greater_than,
                           LESS_THAN_CONDITION: condition_less_than} 
        
        def text_value(text, text_element):
            
            return text_element.get(VALUE_ATTRIBUTE)
        
        def text_variable(text, text_element):
            
            text_variable = text_element.get(VARIABLE_ATTRIBUTE)
            return self.standard_variables[text_variable]
        
        def text_case(text, text_element):
            
            case = text_element.get(CASE_ATTRIBUTE)
        
            if case == CASE_LOWER:
                return text.lower()
            elif case == CASE_UPPER:
                return text.upper()
            elif case == CASE_TITLE:
                return text.title()
            else:
                return text
        
        def text_replace_spaces_with(text, text_element):
            
            space_replacement = text_element.get(REPLACE_SPACES_WITH_ATTRIBUTE)
            
            if space_replacement is None:
                return text
            else:
                return text.replace(' ', space_replacement) 
        
        def text_prefix(text, text_element):
            
            prefix = text_element.get(PREFIX_ATTRIBUTE)
            
            if prefix is None:
                return text
            else:
                return prefix + text
    
        def text_suffix(text, text_element):
            
            suffix = text_element.get(SUFFIX_ATTRIBUTE)
            
            if suffix is None:
                return text
            else:
                return text + suffix
        
        # The order is important in the tuple. The various text formatting attributes will be
        # applied in the order in the tuple and the prefix and suffix should be applied after
        # replacing spaces and setting case.
        self.text_attributes = (text_case, text_replace_spaces_with, text_prefix, text_suffix)
    
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
            
            file_element = self.get_file_element(destination_element)[0]
            file_name = self.get_file_name(file_element)
            path = os.path.join(path, file_name)
            
        return path
        
    def load_standard_variables(self, os_file_path):
        
        file_name, file_extension = os.path.splitext(os_file_path)
        file_name = os.path.basename(file_name)
        file_extension = file_extension[1:].strip().lower() 
        
        self.standard_variables[CURRENT_DATE] = datetime.now()
        self.standard_variables[FILE_PATH] = os.path.dirname(os_file_path)
        self.standard_variables[FILE_NAME] = file_name
        self.standard_variables[FILE_EXTENSION] = file_extension
        self.standard_variables[FILE_SIZE] = os.path.getsize(os_file_path)
        self.standard_variables[FILE_DATE_CREATED] = os.path.getctime(os_file_path)
        self.standard_variables[FILE_DATE_MODIFIED] = os.path.getmtime(os_file_path)
        self.standard_variables[FILE_DATE_ACCESSED] = os.path.getatime(os_file_path)
                
        # TODO: Implement file_index and file_count for batch mode processing
        self.standard_variables[FILE_INDEX] = 1 # To be implemented later when the batch mode is finished
        self.standard_variables[FILE_COUNT] = 1
        
    def get_destination_element(self, use_value):
        
        destination_element = None
        destination_elements = self.get_destination_elements(self.root)
            
        for element in destination_elements:
            match_value = element.get(MATCH_ATTRIBUTE)
            match_condition = element.get(CONDITION_ATTRIBUTE)
            case_sensitive = element.get(CASE_SENSITIVE_ATTRIBUTE)
                
            if not case_sensitive:
                match_value = match_value.lower()
                use_value = use_value.lower()
            
            if self.conditions[match_condition](match_value, use_value):
                destination_element = element
                break
            
        return destination_element
    
    def get_text(self, text_element):
        
        text = None
        value = text_element.get(VALUE_ATTRIBUTE)
        variable = text_element.get(VARIABLE_ATTRIBUTE)
        
        if value is not None:
            text = value
        elif variable is not None:
            text = self.standard_variables[variable]
        else:
            raise PathFinderError("The value for the text element could not be determined")
        
        for attribute in self.text_attributes:
            text = attribute(text, text_element)
            
        return text
    
    def process_macro(self, name):
        
        text = ''
        text_elements = self.get_text_elements(self.root, name=name)
        
        for text_element in text_elements:
            text = text + self.get_text(text_element)
        
        return text
    
    def get_folder_name(self, folder_element):
        
        value = folder_element.get(VALUE_ATTRIBUTE)
        variable = folder_element.get(VARIABLE_ATTRIBUTE)
        macro = folder_element.get(MACRO_ATTRIBUTE)
        random = folder_element.get(RANDOM_ATTRIBUTE)
        
        if value is not None:
            return value
        elif variable is not None:
            return self.standard_variables[variable]
        elif macro is not None:
            return self.process_macro(macro)
        elif random:            
            return RANDOM_FOLDER_PLACEHOLDER
        else:
            raise PathFinderError("Folder name could not be determined")
    
    def get_file_name(self, file_element):
        
        value = file_element.get(VALUE_ATTRIBUTE)
        variable = file_element.get(VARIABLE_ATTRIBUTE)
        macro = file_element.get(MACRO_ATTRIBUTE)
        random = file_element.get(RANDOM_ATTRIBUTE)
        
        if value is not None:
            return value
        elif variable is not None:
            return self.standard_variables[variable]
        elif macro is not None:
            return self.process_macro(macro)
        elif random:
            return RANDOM_FILE_PLACEHOLDER
        else:
            raise PathFinderError("File name could not be determined")
