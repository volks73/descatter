# descatter/organize.py
# Copyright (C) 2013 the Descatter authors and contributers <see AUTHORS file>
#
# This module is part of Descatter.
#
# Descatter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Descatter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Descatter.  If not, see <http://www.gnu.org/licenses/>.

"""The organize module provides the mechanism for copying or moving files to folders based on a structure defined in a directive file.

"""
import os
import tempfile
import shutil

from lxml import etree
from datetime import datetime

class DirectiveError(Exception): pass
class FilerError(Exception): pass

class Filer(object):
    """Responsible for copying and/or moving files to destinations in a root folder based on a directive.
    
    Constructor arguments are as follows:
    
    :param root: The path to the root, or top, destination folder. 
        
        All files will be copied or moved to this folder or a subfolder based on the directive.
    
    :param directive: a :class:'.Directive' object which determines the destination path of files.
    
        The directive is responsible for determining the destination path of files relative to the root, or top, destination folder.
        
    """
    
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
    
    def __init__(self, root, directive):
        self.root = root
        self.directive = directive

    def file_file(self, file, move=False):
        
        return self._file(self._create_context(file), move)
    
    def file_list(self, files, move=False):
        
        filed_paths = []       
        file_count = len(files)
        file_index = 1
        
        for file_path in files:
            if os.path.isfile(file_path):
                filed_path = self._file(self._create_context(file_path, file_index, file_count), move)
                filed_paths.append(filed_path)
                file_index = file_index + 1
        
        return filed_paths
        
    def file_folder(self, folder, deep=False, move=False):
        
        if os.path.isdir(folder):
            files = []
    
            if deep:
                for root, subfolders, file_names in os.walk(folder):
                    for file_name in file_names:
                        files.append(os.path.join(root, file_name))
            else:
                for folder_item in os.listdir(folder):
                    files.append(os.path.join(folder, folder_item))
                
            filed_paths = self.file_list(files, move)
            
            return filed_paths
        else:
            raise FilerError("The folder: '%s' could not be filed because it is not a directory" % folder)

    def _create_context(self, source, file_index=1, file_count=1):
    
        if os.path.isfile(source):
            context = {}
            file_name, file_extension = os.path.splitext(source)
            file_name = os.path.basename(file_name)
            file_extension = file_extension[1:].strip().lower() 
                    
            context[self.CURRENT_DATETIME] = datetime.now()
            context[self.FILE_COUNT] = file_count
            context[self.FILE_EXTENSION] = file_extension
            context[self.FILE_DATE_ACCESSED] = os.path.getatime(source)
            context[self.FILE_DATE_CREATED] = os.path.getctime(source)
            context[self.FILE_DATE_MODIFIED] = os.path.getmtime(source)
            context[self.FILE_INDEX] = file_index
            context[self.FILE_NAME] = file_name
            context[self.FILE_PATH] = os.path.dirname(source)
            context[self.FILE_SIZE] = os.path.getsize(source)
            context[self.FILE_SOURCE] = source    
            
            return context
        else:
            raise FilerError("A filer context could not be created because the source is not a file")

    def _file(self, context, move):
        
        destination_folder_names, destination_file_name = self.directive.get_destination(context)
        destination_file_path = self.root
        
        for destination_folder_name in destination_folder_names:
            if destination_folder_name == Directive.RANDOM_VALUE_WILDCARD:
                destination_file_path = tempfile.mkdtemp(suffix='', prefix='', dir=destination_file_path)
            else:
                destination_file_path = os.path.join(destination_file_path, destination_folder_name)
                os.makedirs(destination_file_path, exist_ok=True)
            
        random_placeholder_index = destination_file_name.find(Directive.RANDOM_VALUE_WILDCARD) 
            
        if random_placeholder_index == -1:
            destination_file_path = os.path.join(destination_file_path, destination_file_name)
        else:
            prefix = destination_file_name[:random_placeholder_index]
            suffix = destination_file_name[random_placeholder_index+1:]
    
            temp_file_handle, destination_file_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=destination_file_path, text=False)
                
            # Ensure the race condition, thread-safe created temporary file has been closed and is not used by another
            # process so that it can be replaced by the source file.
            os.fdopen(temp_file_handle, 'w').close()
        
        filed_path = None
        
        if move:
            filed_path = shutil.move(context[self.FILE_SOURCE], destination_file_path)
        else:
            filed_path = shutil.copy2(context[self.FILE_SOURCE], destination_file_path)
        
        return filed_path
    
class Directive(object):
    """Responsible for reading an XML file and determining the destination of a file.
    
    Constructor arguments are as follows:
    
    :param file: The directive definition XML file path. 
    
    """
    
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
    
    # Precompiled XPaths
    XPATH_RULE_ELEMENTS = etree.XPath("//" + PREFIX + ":" + RULES_TAG + "/" + PREFIX + ":" + RULE_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_CONDITION_ELEMENTS = etree.XPath(PREFIX + ":" + CONDITIONS_TAG + "/" + PREFIX + ":" + CONDITION_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_MACRO_ELEMENTS = etree.XPath("//" + PREFIX + ":" + MACROS_TAG + "/" + PREFIX + ":" + MACRO_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_MATCH_ATTRIBUTE = etree.XPath(PREFIX + ":" + CONDITIONS_TAG + "/@" + MATCH_ATTRIBUTE, namespaces=XPATH_NAMESPACE)
    XPATH_PATH_ELEMENT = etree.XPath("//" + PREFIX + ":" + PATHS_TAG + "/" + PREFIX + ":" + PATH_TAG + "[@" + NAME_ATTRIBUTE + "=$name]", namespaces=XPATH_NAMESPACE)
    XPATH_FOLDER_ELEMENTS = etree.XPath(".//" + PREFIX + ":" + FOLDER_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_TEXT_ELEMENTS = etree.XPath("//" + PREFIX + ":" + MACROS_TAG + "/" + PREFIX + ":" + MACRO_TAG + "[@" + NAME_ATTRIBUTE + "=$name]/" + PREFIX + ":" + TEXT_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_FILE_ELEMENT = etree.XPath(PREFIX + ":" + FOLDER_TAG + "//" + PREFIX + ":" + FILE_TAG, namespaces=XPATH_NAMESPACE)
    
    def __init__(self, file):
        
        self.file_path = file
        self._root = etree.parse(self.file_path).getroot()
        
    def get_destination(self, file_context):
        
        file_name = None
        path_name = None
        self.file_context = file_context
        
        for rule_element in self.XPATH_RULE_ELEMENTS(self._root):
            path_name = self._process_rule(rule_element)
            
            if path_name is not None:
                break
        
        if path_name is None:
            raise DirectiveError("A path name could not be determined for the file")
        else:
            path_element = self.XPATH_PATH_ELEMENT(self._root, name=path_name)
            
            if path_element is None:
                raise DirectiveError("A path could not be determined for the file: '%s'" % file_context[Filer.FILE_SOURCE])
            else:
                path_element = path_element[0]
  
            folder_names = []
                            
            for folder_element in self.XPATH_FOLDER_ELEMENTS(path_element):
                folder_name = self._get_folder_name(folder_element)
                folder_names.append(folder_name)
            
            file_element = self.XPATH_FILE_ELEMENT(path_element)[0]
            file_name = self._get_file_name(file_element)
            
        return folder_names, file_name

    def _process_rule(self, rule_element):
        
        path_name = None
        
        match = self.XPATH_MATCH_ATTRIBUTE(rule_element)[0].lower()
        condition_results = []        
        
        for condition_element in self.XPATH_CONDITION_ELEMENTS(rule_element):
            condition_results.append(self._get_condition_result(condition_element))
        
        if self._is_match(match, condition_results):
            path_name = rule_element.get(self.PATH_ATTRIBUTE)
        
        return path_name

    def _is_match(self, match, results):
        
        if match == self.CONDITIONS_MATCH_ALL:
            return all(results)
        elif match == self.CONDITIONS_MATCH_ANY:
            return any(results)
        else:
            raise DirectiveError("The '%s' attribute value for the '%s' tag is unknown" % (self.MATCH_ATTRIBUTE, self.CONDITIONS_TAG))
    
    def _get_condition_result(self, condition_element):
        
        type_value = condition_element.get(self.TYPE_ATTRIBUTE).lower()
        variable = condition_element.get(self.VARIABLE_ATTRIBUTE)
        value = condition_element.get(self.VALUE_ATTRIBUTE)
        case_sensitive = condition_element.get(self.CASE_SENSITIVE_ATTRIBUTE)
        
        if variable is None:
            raise DirectiveError("The '%s' attribute must be present in the '%s' tag" % (self.VARIABLE_ATTRIBUTE, self.CONDITION_TAG))
        else:
            variable = self.file_context[variable]
            
        if value is None:
            raise DirectiveError("The '%s' attribute must be present in the '%s' tag" % (self.VALUE_ATTRIBUTE, self.CONDITION_TAG))
        
        if not case_sensitive:
            variable = variable.lower()
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
            raise DirectiveError("The '%s' attribute value for the '%s' tag is unknown" % (self.TYPE_ATTRIBUTE, self.CONDITION_TAG))
    
    def _get_text(self, text_element):
        
        # TODO: Add date formatting if a date child tag is present
        # TODO: Add numeric formatting if a numeric child tag is present
        text = ''
        value = text_element.get(self.VALUE_ATTRIBUTE)
        variable = text_element.get(self.VARIABLE_ATTRIBUTE)
        
        if value is not None:
            text = value
        elif variable is not None:
            text = self.file_context[variable]
        else:
            raise DirectiveError("The '%s' tag is missing either the '%s' or '%s' attribute to determine the value" % (self.TEXT_TAG, self.VALUE_ATTRIBUTE, self.VARIABLE_ATTRIBUTE))
        
        text = self._format_text(text, text_element)
            
        return text
    
    def _format_text(self, text, text_element): 
        
        # The order is important in the tuple. The various text formatting attributes will be
        # applied in the order in the tuple and the prefix and suffix should be applied after
        # replacing spaces and setting case.
        format_methods = (self._format_case, self._format_replace_spaces_with, self._format_prefix, self._format_suffix)
        
        for format_method in format_methods:
            text = format_method(text, text_element)
        
        return text
    
    def _format_case(self, text, text_element):
            
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
            raise DirectiveError("The '%s' attribute value for the '%s' tag is unknown" % (self.CASE_ATTRIBUTE, self.TEXT_TAG))
        
    def _format_replace_spaces_with(self, text, text_element):
            
        space_replacement = text_element.get(self.REPLACE_SPACES_WITH_ATTRIBUTE)
            
        if space_replacement is None:
            return text
        else:
            return text.replace(' ', space_replacement) 
        
    def _format_prefix(self, text, text_element):
            
        prefix = text_element.get(self.PREFIX_ATTRIBUTE)
            
        if prefix is None:
            return text
        else:
            return prefix + text
    
    def _format_suffix(self, text, text_element):
            
        suffix = text_element.get(self.SUFFIX_ATTRIBUTE)
            
        if suffix is None:
            return text
        else:
            return text + suffix
    
    def _process_macro(self, name):
        
        text = ''
        text_elements = self.XPATH_TEXT_ELEMENTS(self._root, name=name)
        
        for text_element in text_elements:
            text = text + self._get_text(text_element)
        
        return text
    
    def _get_folder_name(self, folder_element):
        
        value = folder_element.get(self.VALUE_ATTRIBUTE)
        variable = folder_element.get(self.VARIABLE_ATTRIBUTE)
        macro = folder_element.get(self.MACRO_ATTRIBUTE)
        
        if value is not None:
            return value
        elif variable is not None:
            return self.file_context[variable]
        elif macro is not None:
            return self._process_macro(macro)
        else:
            raise DirectiveError("The '%s' tag is missing either the '%s', '%s', or '%s' attribute to determine the value" % (self.FOLDER_TAG, self.VALUE_ATTRIBUTE, self.VARIABLE_ATTRIBUTE, self.MACRO_ATTRIBUTE))
    
    def _get_file_name(self, file_element):
        
        value = file_element.get(self.VALUE_ATTRIBUTE)
        variable = file_element.get(self.VARIABLE_ATTRIBUTE)
        macro = file_element.get(self.MACRO_ATTRIBUTE)
        
        if value is not None:
            return value
        elif variable is not None:
            return self.file_context[variable]
        elif macro is not None:
            return self._process_macro(macro)
        else:
            raise DirectiveError("The '%s' tag is missing either the '%s', '%s', or '%s' attribute to determine the value" % (self.FILE_TAG, self.VALUE_ATTRIBUTE, self.VARIABLE_ATTRIBUTE, self.MACRO_ATTRIBUTE))
