from lxml import etree
from datetime import datetime

import os

import constants

# XML    
PREFIX = 'ds'
NAMESPACE = 'descatter/2013/content_schema/1.0'
XPATH_NAMESPACE = {PREFIX: NAMESPACE}
    
# Tags
INFO_TAG = 'info'
TITLE_TAG = 'title'
AUTHOR_TAG = 'author'
NAME_TAG = 'name'
EMAIL_TAG = 'email'
DESCRIPTION_TAG = 'description'
MACROS_TAG = 'macros'
MACRO_TAG = 'macro'
TEXT_TAG = 'text'
GROUP_TAG = 'group'
DESTINATIONS_TAG = 'destinations'
DESTINATION_TAG = 'destination'
FOLDER_TAG = 'folder'
FILE_TAG = 'file'
METADATA_TAG = 'metadata'
    
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
    
ANY_WILDCARD = '*'
    
# Condition options
EQUALS_CONDITION = 'equals'
GREATER_THAN_CONDITION = 'greater-than'
LESS_THAN_CONDITION = 'less-than'

# Case options
CASE_LOWER = 'lowercase'
CASE_UPPER = 'uppercase'
CASE_SENTENCE = 'sentence'
CASE_TITLE = 'title'

# Standard Variables
FILE_PATH = 'file-path'
FILE_NAME = 'file-name'
FILE_EXTENSION = 'file-extension'
FILE_SIZE = 'file-size'
FILE_DATE_CREATED = 'file-date-created' 
FILE_DATE_MODIFIED = 'file-date-modified'
FILE_DATE_ACCESSED = 'file-date-accessed'
FILE_DATE_ADDED = 'file-date-added'
FILE_TITLE = 'file-title'
FILE_INDEX = 'file-index'
FILE_COUNT = 'file-count'

class SchemaError(Exception): pass

class MatchConditions(object):
    
    def __init__(self):
        self.conditions = {}
    
    def add(self, condition):
        self.conditions[condition.attribute_value] = condition
    
    def matches(self, match_value, use_value, match_condition):
        return self.conditions[match_condition].matches(match_value, use_value)

class EqualsCondition(object):
    
    def __init__(self):
        self.name = EQUALS_CONDITION
    
    def matches(self, match_value, use_value):
        return match_value == use_value
    
class GreaterThanCondition(object):
    
    def __init_(self):
        self.name = GREATER_THAN_CONDITION
        
    def matches(self, match_value, use_value):
        return match_value > use_value

class LessThanCondition(object):
    
    def __init_(self):
        self.name = LESS_THAN_CONDITION
    
    def matches(self, match_value, use_value):
        return match_value < use_value

class CatalogSchema(object):                       
    
    def __init__(self, catalog):
        
        self.schema_file_path = os.path.join(catalog.path, constants.CONTENT_SCHEMA_FILE_NAME)
        self.content_folder_path = os.path.join(catalog.path, constants.CONTENT_FOLDER_NAME)
        self.root = etree.parse(self.schema_file_path).getroot() 
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
        
        self.get_folder_elements = etree.XPath(("/" +
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
                                              "[@name=$name]/" +
                                              PREFIX +
                                              ":" +
                                              TEXT_TAG),
                                             namespace=XPATH_NAMESPACE)

        self.get_file_element = etree.XPath(("//" + 
                                             PREFIX + 
                                             ":" +
                                             FOLDER_TAG +
                                             "/" +
                                             FILE_TAG),
                                            namespace=XPATH_NAMESPACE)

        self.conditions = MatchConditions()
        self.conditions.add(EqualsCondition())
        self.conditions.add(GreaterThanCondition())
        self.conditions.add(LessThanCondition())
    
    def load_standard_variables(self, os_file_path, title):
        
        file_name, file_extension = os.path.splitext(os_file_path)
        file_name = os.path.basename(file_name)
        file_extension = file_extension[1:].strip().lower() 
    
        self.standard_variables[FILE_PATH] = os.path.dirname(os_file_path)
        self.standard_variables[FILE_NAME] = file_name
        self.standard_variables[FILE_EXTENSION] = file_extension
        self.standard_variables[FILE_SIZE] = os.path.getsize(os_file_path)
        self.standard_variables[FILE_DATE_CREATED] = os.path.getctime(os_file_path)
        self.standard_variables[FILE_DATE_MODIFIED] = os.path.getmtime(os_file_path)
        self.standard_variables[FILE_DATE_ACCESSED] = os.path.getatime(os_file_path)
        self.standard_variables[FILE_DATE_ADDED] = datetime.now()
        self.standard_variables[FILE_TITLE] = title
        self.standard_variables[FILE_INDEX] = 1
        self.standard_variables[FILE_COUNT] = 1
    
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
            
            if self.conditions.matches(match_value, use_value, match_condition):
                destination_element = element
                break
        
        return destination_element
    
    def get_text_from_macro(self, name):
        
        text = None
        text_elements = self.get_text_elements(self.root, name=name)
        
        for text_element in text_elements:
            value = text_element.get(VALUE_ATTRIBUTE)
            
            if value is None:
                text_variable = text_element.get(VARIABLE_ATTRIBUTE)
                value = self.standard_variables[text_variable]
            
            # TODO: Add handling of case
            # TODO: Add handling of prefix
            # TODO: Add handling of suffix
            # TODO: Add handling of replace-space-with
            
            text = text + value
        
        return text
    
    def get_folder_name(self, folder_element):
        
        name = folder_element.get(NAME_ATTRIBUTE)
        variable = folder_element.get(VARIABLE_ATTRIBUTE)
        macro = folder_element.get(MACRO_ATTRIBUTE)
        random = folder_element.get(RANDOM_ATTRIBUTE)
        
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
            raise SchemaError("Folder name could not be determined")
    
    def get_file_name(self, file_element):
        
        name = file_element.get(NAME_ATTRIBUTE)
        variable = file_element.get(VARIABLE_ATTRIBUTE)
        macro = file_element.get(MACRO_ATTRIBUTE)
        random = file_element.get(RANDOM_ATTRIBUTE)
        
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
            raise SchemaError("File name could not be determined")
    
    def get_destination_path(self, destination_element):
        
        destination_file_path = self.content_folder_path
        destination_metadata_path = self.content_folder_path
        folder_elements = self.get_folder_elements(destination_element)
            
        for folder_element in folder_elements:
            folder_name = self.get_folder_name(folder_element)
            destination_file_path = os.path.join(destination_file_path, folder_name)
        
        file_element = self.get_file_element(destination_element)
        file_name = self.get_file_name(file_element)
        
        destination_file_path = os.path.join(destination_file_path, file_name)

        # TODO: Add handling of metadata tag
            
        return destination_file_path, destination_metadata_path
    
    def get_destination(self, os_file_path, title):
        
        self.load_standard_variables(os_file_path, title)
        
        use_variable = self.get_use_attribute(self.root)[0]
        use_value = self.standard_variables[use_variable]
        destination_element = self.get_destination_element(use_value)
        
        if destination_element is None:
            raise SchemaError("A destination could not be determined for the checkin file")
        else:
            return self.get_destination_path(destination_element) 