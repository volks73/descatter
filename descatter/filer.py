from lxml import etree
from datetime import datetime

import os
import tempfile
import shutil

class ProcessorError(Exception): pass
class DirectorError(Exception): pass

class Processor(object):
    
    # File Context Variables
    CURRENT_DATETIME = 'current-datetime'   
    FILE_COUNT = 'file-count'
    FILE_EXTENSION = 'file-extension'
    FILE_DATE_ACCESSED = 'file-date-accessed'
    FILE_DATE_CREATED = 'file-date-created' 
    FILE_DATE_MODIFIED = 'file-date-modified'
    FILE_INDEX = 'file-index'
    FILE_NAME = 'file-name'
    FILE_PATH = 'file-path'
    FILE_SIZE = 'file-size'
    FILE_SOURCE = 'file-source'
    
    def __init__(self, base_destination_folder_path, directive_file_path):
        self.base_destination_folder_path = base_destination_folder_path
        self.director = Director(directive_file_path)

    def file_context(self, source_file_path, file_index=1, file_count=1):
        
        context = {}
        file_name, file_extension = os.path.splitext(source_file_path)
        file_name = os.path.basename(file_name)
        file_extension = file_extension[1:].strip().lower() 
            
        context[self.CURRENT_DATETIME] = datetime.now()
        context[self.FILE_COUNT] = file_count
        context[self.FILE_EXTENSION] = file_extension
        context[self.FILE_DATE_ACCESSED] = os.path.getatime(source_file_path)
        context[self.FILE_DATE_CREATED] = os.path.getctime(source_file_path)
        context[self.FILE_DATE_MODIFIED] = os.path.getmtime(source_file_path)
        context[self.FILE_INDEX] = file_index
        context[self.FILE_NAME] = file_name
        context[self.FILE_PATH] = os.path.dirname(source_file_path)
        context[self.FILE_SIZE] = os.path.getsize(source_file_path)
        context[self.FILE_SOURCE] = source_file_path    
    
        return context

    def file(self, source, delete_source=False):
        
        if os.path.isfile(source):
            self.file_single(self.file_context(source), delete_source)

    def file_single(self, file_context, delete_source=False):
        
        destination_folder_names, destination_file_name = self.director.find_destination(file_context)
        destination_file_path = self.base_destination_folder_path
        
        for destination_folder_name in destination_folder_names:
            if destination_folder_name == Director.RANDOM_VALUE_WILDCARD:
                destination_file_path = tempfile.mkdtemp(suffix='', prefix='', dir=destination_file_path)
            else:
                destination_file_path = os.path.join(destination_file_path, destination_folder_name)
                os.makedirs(destination_file_path, exist_ok=True)
            
        random_placeholder_index = destination_file_name.find(Director.RANDOM_VALUE_WILDCARD) 
            
        if random_placeholder_index == -1:
            destination_file_path = os.path.join(destination_file_path, destination_file_name)
        else:
            prefix = destination_file_name[:random_placeholder_index]
            suffix = destination_file_name[random_placeholder_index+1:]
    
            temp_file_handle, destination_file_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=destination_file_path, text=False)
                
            # Ensure the race condition, thread-safe created temporary file has been closed and is not used by another
            # process so that it can be replaced by the source file.
            os.fdopen(temp_file_handle, 'w').close()
            
        shutil.copy2(file_context[self.FILE_SOURCE], destination_file_path)
            
        if delete_source:
            os.remove(file_context[self.FILE_SOURCE])
        
        return destination_file_path
    
    def file_list(self, file_list, delete_source=False):
        pass
    
    def file_folder(self, folder_path, recurisve=False, delete_source=False):
        pass

class Director(object):
    
    # XML    
    NAMESPACE = 'descatter/filer/schema/1.0'
    PREFIX = 'ds'
    XPATH_NAMESPACE = {PREFIX: NAMESPACE}
            
    # Tags
    AUTHOR_TAG = 'author'
    CONDITIONS_TAG = 'conditions'
    CONDITION_TAG = 'condition'
    DESCRIPTION_TAG = 'description'
    EMAIL_TAG = 'email'
    FILE_TAG = 'file'
    FOLDER_TAG = 'folder'
    GROUP_TAG = 'group'
    INFO_TAG = 'info'
    MACRO_TAG = 'macro'
    MACROS_TAG = 'macros'
    NAME_TAG = 'name'
    PATHS_TAG = 'paths'
    PATH_TAG = 'path'
    RULES_TAG = 'rules'
    RULE_TAG = 'rule'
    TEXT_TAG = 'text'
    TITLE_TAG = 'title'
        
    # Attributes
    CASE_ATTRIBUTE = 'case'
    CASE_SENSITIVE_ATTRIBUTE = 'case-sensitive'
    MACRO_ATTRIBUTE = 'macro'
    MATCH_ATTRIBUTE = 'match'
    NAME_ATTRIBUTE = 'name'
    PATH_ATTRIBUTE = 'path'
    PREFIX_ATTRIBUTE = 'prefix'
    REPLACE_SPACES_WITH_ATTRIBUTE = 'replace-spaces-with'
    SUFFIX_ATTRIBUTE = 'suffix'
    TYPE_ATTRIBUTE = 'type'
    VALUE_ATTRIBUTE = 'value'
    VARIABLE_ATTRIBUTE = 'variable'
    
    # Conditions match attribute values
    CONDITIONS_MATCH_ALL = 'all'
    CONDITIONS_MATCH_ANY = 'any'
    
    # Condition type attribute values
    CONDITION_TYPE_EQUALS = 'equals'
    CONDITION_TYPE_GREATER_THAN = 'greater-than'
    CONDITION_TYPE_LESS_THAN = 'less-than'    
    
    # Text case attribute values
    TEXT_CASE_LOWER = 'lower'
    TEXT_CASE_TITLE = 'title'
    TEXT_CASE_UPPER = 'upper'
    
    # Value wildcards
    ANY_VALUE_WILDCARD = '*'
    
    # '?' is used as a placeholder to define a random file name or random folder name because
    # it is an illegal character on all operating systems.
    RANDOM_VALUE_WILDCARD = '?'
    
    def __init__(self, directive_file_path):
        
        self.root = etree.parse(directive_file_path).getroot()
        
        self.rule_elements = etree.XPath(("//" +
                                          self.PREFIX +
                                          ":" +
                                          self.RULES_TAG +
                                          "/" +
                                          self.PREFIX +
                                          ":" +
                                          self.RULE_TAG),
                                        namespaces=self.XPATH_NAMESPACE)
        
        self.condition_elements = etree.XPath((self.PREFIX +
                                               ":" +
                                               self.CONDITIONS_TAG +
                                               "/" +
                                               self.PREFIX +
                                               ":" +
                                               self.CONDITION_TAG),
                                              namespaces=self.XPATH_NAMESPACE)
        
        self.macro_elements = etree.XPath(("//" +
                                           self.PREFIX +
                                           ":" + 
                                           self.MACROS_TAG +
                                           "/" +
                                           self.PREFIX +
                                           ":" +
                                           self.MACRO_TAG),
                                          namespaces=self.XPATH_NAMESPACE)
               
        self.match_attribute = etree.XPath((self.PREFIX + 
                                            ":" + 
                                            self.CONDITIONS_TAG + 
                                            "/@" +
                                            self.MATCH_ATTRIBUTE), 
                                           namespaces=self.XPATH_NAMESPACE)
        
        self.path_element = etree.XPath(("//" +
                                         self.PREFIX +
                                         ":" +
                                         self.PATHS_TAG +
                                         "/" +
                                         self.PREFIX +
                                         ":" +
                                         self.PATH_TAG +
                                         "[@" +
                                         self.NAME_ATTRIBUTE +
                                         "=$name]"),
                                        namespaces=self.XPATH_NAMESPACE)
        
        self.folder_elements = etree.XPath((".//" +
                                            self.PREFIX +
                                            ":" +
                                            self.FOLDER_TAG), 
                                            namespaces=self.XPATH_NAMESPACE)
        
        self.text_elements = etree.XPath(("//" +
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
                                         namespaces=self.XPATH_NAMESPACE)

        self.file_element = etree.XPath((self.PREFIX + 
                                         ":" +
                                         self.FOLDER_TAG +
                                         "//" +
                                         self.PREFIX +
                                         ":" +
                                         self.FILE_TAG),
                                        namespaces=self.XPATH_NAMESPACE)
        
        def format_case(text, text_element):
            
            case = text_element.get(self.CASE_ATTRIBUTE)
        
            if case is None:
                return text
            elif case == self.TEXT_CASE_LOWER:
                return text.lower()
            elif case == self.TEXT_CASE_UPPER:
                return text.upper()
            elif case == self.TEXT_CASE_TITLE:
                return text.title()
            else:
                raise DirectorError("The '%s' attribute value for the '%s' tag is unknown" % (self.CASE_ATTRIBUTE, self.TEXT_TAG))
        
        def format_replace_spaces_with(text, text_element):
            
            space_replacement = text_element.get(self.REPLACE_SPACES_WITH_ATTRIBUTE)
            
            if space_replacement is None:
                return text
            else:
                return text.replace(' ', space_replacement) 
        
        def format_prefix(text, text_element):
            
            prefix = text_element.get(self.PREFIX_ATTRIBUTE)
            
            if prefix is None:
                return text
            else:
                return prefix + text
    
        def format_suffix(text, text_element):
            
            suffix = text_element.get(self.SUFFIX_ATTRIBUTE)
            
            if suffix is None:
                return text
            else:
                return text + suffix
        
        # The order is important in the tuple. The various text formatting attributes will be
        # applied in the order in the tuple and the prefix and suffix should be applied after
        # replacing spaces and setting case.
        self.format_attributes = (format_case, format_replace_spaces_with, format_prefix, format_suffix)
    
    def find_destination(self, file_context):
        
        file_name = None
        path_name = None
        self.file_context = file_context
        
        for rule_element in self.rule_elements(self.root):
            path_name = self.process_rule(rule_element)
            
            if path_name is not None:
                break
        
        if path_name is None:
            raise DirectorError("A path name could not be determined for the file")
        else:
            path_element = self.path_element(self.root, name=path_name)[0]
        
            if path_element is None:
                raise DirectorError("A path could not be determined for the file")
            else:           
                folder_names = []
                            
                for folder_element in self.folder_elements(path_element):
                    folder_name = self.get_folder_name(folder_element)
                    folder_names.append(folder_name)
            
                file_element = self.file_element(path_element)[0]
                file_name = self.get_file_name(file_element)
            
        return folder_names, file_name

    def process_rule(self, rule_element):
        
        path_name = None
        
        match = self.match_attribute(rule_element)[0].lower()
        condition_results = []        
        
        for condition_element in self.condition_elements(rule_element):
            condition_results.append(self.get_condition_result(condition_element))
        
        if self.is_match(match, condition_results):
            path_name = rule_element.get(self.PATH_ATTRIBUTE)
        
        return path_name

    def is_match(self, match, results):
        
        if match == self.CONDITIONS_MATCH_ALL:
            return all(results)
        elif match == self.CONDITIONS_MATCH_ANY:
            return any(results)
        else:
            raise DirectorError("The '%s' attribute value for the '%s' tag is unknown" % (self.MATCH_ATTRIBUTE, self.CONDITIONS_TAG))
    
    def get_condition_result(self, condition_element):
        
        type_value = condition_element.get(self.TYPE_ATTRIBUTE).lower()
        variable = condition_element.get(self.VARIABLE_ATTRIBUTE)
        value = condition_element.get(self.VALUE_ATTRIBUTE)
        
        # TODO: Add case-sensitive option to the condition tag
        
        if variable is None:
            raise DirectorError("The '%s' attribute must be present in the '%s' tag" % (self.VARIABLE_ATTRIBUTE, self.CONDITION_TAG))
        else:
            variable = self.file_context[variable].lower()
            
        if value is None:
            raise DirectorError("The '%s' attribute must be present in the '%s' tag" % (self.VALUE_ATTRIBUTE, self.CONDITION_TAG))
        else:
            value = value.lower()
                
        if type_value == self.CONDITION_TYPE_EQUALS:
            if value == self.ANY_VALUE_WILDCARD:
                return True
            else:
                return variable == value
        elif type_value == self.CONDITION_TYPE_GREATER_THAN:
            return variable > value
        elif type_value == self.CONDITION_TYPE_LESS_THAN:
            return variable < value
        else:
            raise DirectorError("The '%s' attribute value for the '%s' tag is unknown" % (self.TYPE_ATTRIBUTE, self.CONDITION_TAG))
    
    def get_text(self, text_element):
        
        # TODO: Add date formatting if a date child tag is present
        text = None
        value = text_element.get(self.VALUE_ATTRIBUTE)
        variable = text_element.get(self.VARIABLE_ATTRIBUTE)
        
        if value is not None:
            text = value
        elif variable is not None:
            text = self.file_context[variable]
        else:
            raise DirectorError("The '%s' tag is missing either the '%s' or '%s' attribute to determine the value" % (self.TEXT_TAG, self.VALUE_ATTRIBUTE, self.VARIABLE_ATTRIBUTE))
        
        for format_attribute in self.format_attributes:
            text = format_attribute(text, text_element)
            
        return text
    
    def process_macro(self, name):
        
        text = ''
        text_elements = self.text_elements(self.root, name=name)
        
        for text_element in text_elements:
            text = text + self.get_text(text_element)
        
        return text
    
    def get_folder_name(self, folder_element):
        
        value = folder_element.get(self.VALUE_ATTRIBUTE)
        variable = folder_element.get(self.VARIABLE_ATTRIBUTE)
        macro = folder_element.get(self.MACRO_ATTRIBUTE)
        
        if value is not None:
            return value
        elif variable is not None:
            return self.file_context[variable]
        elif macro is not None:
            return self.process_macro(macro)
        else:
            raise DirectorError("The '%s' tag is missing either the '%s', '%s', or '%s' attribute to determine the value" % (self.FOLDER_TAG, self.VALUE_ATTRIBUTE, self.VARIABLE_ATTRIBUTE, self.MACRO_ATTRIBUTE))
    
    def get_file_name(self, file_element):
        
        value = file_element.get(self.VALUE_ATTRIBUTE)
        variable = file_element.get(self.VARIABLE_ATTRIBUTE)
        macro = file_element.get(self.MACRO_ATTRIBUTE)
        
        if value is not None:
            return value
        elif variable is not None:
            return self.file_context[variable]
        elif macro is not None:
            return self.process_macro(macro)
        else:
            raise DirectorError("The '%s' tag is missing either the '%s', '%s', or '%s' attribute to determine the value" % (self.FILE_TAG, self.VALUE_ATTRIBUTE, self.VARIABLE_ATTRIBUTE, self.MACRO_ATTRIBUTE))
