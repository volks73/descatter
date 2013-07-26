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
    
    :param directive: a :class:'.Directive' object. Determines the destination path of files.
    
        The directive is responsible for determining the destination path of files relative to the root, or top, destination folder.
        
    """
    
    # File Context Variables
    
    # The current datetime stamp
    CURRENT_DATETIME = 'current-datetime'
    
    # The total number of files in the batch of files to be filed   
    FILE_COUNT = 'file-count'
    
    # The file extension minus the leading period
    FILE_EXTENSION = 'file-extension'
    
    # The datetime stamp the file was last accessed
    FILE_DATE_ACCESSED = 'file-date-accessed'
    
    # The datetime stamp the file was created
    FILE_DATE_CREATED = 'file-date-created' 
    
    # The datetime stamp the file was last modified
    FILE_DATE_MODIFIED = 'file-date-modified'
    
    # The index of the file in the batch of files to be filed
    FILE_INDEX = 'file-index'
    
    # The file name without the path or extension
    FILE_NAME = 'file-name'
    
    # The path to the source file without the file name
    FILE_PATH = 'file-path'
    
    # The file size in bytes
    FILE_SIZE = 'file-size'
    
    # The source path, this is the absolute path to the source file and includes the file name and extension.
    FILE_SOURCE_PATH = 'file-source-path'
    
    def __init__(self, directive):
        """Constructor for the :class:`.Filer`."""
        
        if directive is None:
            raise FilerError("The directive does not exist")
                
        self.directive = directive
        self._listeners = []
    
    def subscribe(self, listener):
        self._listeners.append(listener)

    def file(self, source, destination, recursive=False, move=False):
        """Files based on the type of source.
        
        If the 'source' is a single file, it will still be batched but with an index of 1 and a count of 1.
        
        :param source: A file path, a comma-separated list of file paths, or a folder path that will be filed to the destination according to a directive.
        :param destination: A path. The path to a folder where the source will be filed.
        :param recursive: Optional boolean. 'True' indicates a recursive filing if the source is a folder. A recursive filing files all files in subfolders of the source root, or top, folder. 'False' indicates only files in the root, or top, folder are filed.
        :param move: Optional boolean. 'True' indicates the source is moved (copied to the destination then deleted). 'False' indicates the source is copied but not deleted.
        
        """
        # TODO: Add overwrite argument option. If 'True' files are overwritten if they already exist at the destination. If 'False' files are not copied or moved if they already exist at the destination.

        if os.path.isdir(source):
            self.file_folder(source, destination, recursive, move)
        else:
            source_list = source.split(',')
            self.file_list(source_list, destination, move)

    def file_file(self, source, destination, move=False):
        """Files a single file.
        
        :param source: A path. The path to a single file to file.
        :param destination: A path. The path to a folder where the source will be filed.
        :param move: Optional boolean. 'True' indicates the file is moved (copy to the destination then deleted). 'False' indicates the source is copied but not deleted.

        """
        
        return self._file(self._create_context(source), destination, move)
    
    def file_list(self, source, destination, move=False):
        """Files a list of file paths.
        
        :param source: A list. The file paths to be filed as a batch.
        :param destination: A path. The path to a folder where the source will be filed.
        :param move: Optional boolean. 'True' indicates the source is moved (copied to the destination then deleted). 'False' indicates the source is copied but not deleted.
        
        """
        
        filed_paths = []       
        file_count = len(source)
        file_index = 1
        
        for file_path in source:
            if os.path.isfile(file_path):
                filed_path = self._file(self._create_context(file_path, file_index, file_count), destination, move)
                filed_paths.append(filed_path)
                file_index = file_index + 1
        
        return filed_paths
        
    def file_folder(self, source, destination, recursive=False, move=False):
        """Files all of the files in a folder.
        
        :param source: A path. The path to a folder where all files within the folder will be filed as a batch.
        :param destination: A path. The path to a folder where the source will be filed.
        :param recursive: Optional boolean. 'True' indicates a recursive filing if the source is a folder. A recursive filing files all files in subfolders of the source root, or top, folder. 'False' indicates only files in the root, or top, folder are filed.
        :param move: Optional boolean. 'True' indicates the source is moved (copied to the destination then deleted). 'False' indicates the source is copied but not deleted.
        
        """
                
        if os.path.isdir(source):
            files = []
    
            if recursive:
                for root, subfolder_names, file_names in os.walk(source):
                    for file_name in file_names:
                        files.append(os.path.join(root, file_name))
            else:
                for folder_item in os.listdir(source):
                    files.append(os.path.join(source, folder_item))
                
            filed_paths = self.file_list(files, destination, move)
            
            return filed_paths
        else:
            raise FilerError("The source: '%s' could not be filed because it is not a folder" % source)

    def _create_context(self, source, index=1, count=1):
        """Creates a filer context.
        
        :param source: A path. The path to a file, which is the source location to be filed to a destination.
        :param index: Optional integer. Indicates the file index, or number, within a batch operation.
        :param count: Optional integer. Indicates the total number of files within a batch operation.
        
        """
    
        if os.path.isfile(source):
            context = {}
            file_name, file_extension = os.path.splitext(source)
            file_name = os.path.basename(file_name)
            file_extension = file_extension[1:].strip().lower() 
                    
            context[self.CURRENT_DATETIME] = datetime.now()
            
            # Need to change count, index, and size to string; otherwise, the condition tests will try to equate a string with an integer.
            context[self.FILE_COUNT] = str(count)
            context[self.FILE_EXTENSION] = file_extension
            context[self.FILE_DATE_ACCESSED] = datetime.fromtimestamp(os.path.getatime(source))
            context[self.FILE_DATE_CREATED] = datetime.fromtimestamp(os.path.getctime(source))
            context[self.FILE_DATE_MODIFIED] = datetime.fromtimestamp(os.path.getmtime(source))
            context[self.FILE_INDEX] = str(index)
            context[self.FILE_NAME] = file_name
            context[self.FILE_PATH] = os.path.dirname(source)
            context[self.FILE_SIZE] = str(os.path.getsize(source))
            context[self.FILE_SOURCE_PATH] = os.path.abspath(source)    
            
            return context
        else:
            raise FilerError("A filer context could not be created because the source is not a file")

    def _notify_started(self, *args):
        
        for listener in self._listeners:
            listener.file_started(args)
        
    def _notify_completed(self, *args):
        
        for listener in self._listeners:
            listener.file_completed(args)
    
    def _notify_failed(self, *args):
        
        for listener in self._listeners:
            listener.file_failed(args)

    def _file(self, context, destination, move):
        """Files a file based on the filer context.
        
        :param context: A dictionary. The filer context, use _create_context to generate the filer context of a file.
        :param move: A boolean. 'True' indicates the file is moved (copy to destination followed by delete at source). 'False' indicates the source file is copied and not deleted afterwards.

        """
        
        self._notify_started(context[self.FILE_SOURCE_PATH])
        
        try:
            destination_folder_names, destination_file_name = self.directive.get_destination(context)
            destination_file_path = destination
            
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
                filed_path = shutil.move(context[self.FILE_SOURCE_PATH], destination_file_path)
            else:
                filed_path = shutil.copy2(context[self.FILE_SOURCE_PATH], destination_file_path)
            
            self._notify_completed(context[self.FILE_SOURCE_PATH], destination_file_path)
            
            return filed_path
        except:
            self._notify_failed(context[self.FILE_SOURCE_PATH])

class Directive(object):
    """Responsible for reading an XML file and determining the destination of a file.
    
    Constructor arguments are as follows:
    
    :param file: A path. The directive definition XML file path. 
    
    """
    
    # XML    
    NAMESPACE = 'descatter/filer/schema/1.0'
    PREFIX = 'ds'
    XPATH_NAMESPACE = {PREFIX: NAMESPACE}
    TRUE_ATTRIBUTE_VALUE = 'true'
    FALSE_ATTRIBUTE_VALUE = 'false'
            
    # Tags
    AUTHOR_TAG = 'author'
    CONDITIONS_TAG = 'conditions'
    CONDITION_TAG = 'condition'
    DATE_TAG = 'date'
    DATE_TAG_FULL_NAME = "{" + NAMESPACE + "}" + DATE_TAG
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
    TEXT_TAG_FULL_NAME = "{" + NAMESPACE + "}" + TEXT_TAG
    TITLE_TAG = 'title'
        
    # Attributes
    CASE_ATTRIBUTE = 'case'
    CASE_SENSITIVE_ATTRIBUTE = 'case-sensitive'
    FORMAT_ATTRIBUTE = 'format'
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
    CONDITION_TYPE_NOT_EQUAL = 'not-equal'
    CONDITION_TYPE_HAS = 'has' 
    
    # Text case attribute values
    TEXT_CASE_LOWER = 'lower'
    TEXT_CASE_TITLE = 'title'
    TEXT_CASE_UPPER = 'upper'
    
    # Value wildcards
    ANY_VALUE_WILDCARD = '*'
    
    # '?' is used as a placeholder to define a random file name or random folder name because
    # it is an illegal character on all operating systems.
    RANDOM_VALUE_WILDCARD = '?'
    
    # Author dictionary keys
    AUTHOR_NAME_KEY = 'name'
    AUTHOR_EMAIL_KEY = 'email'
    
    # Precompiled XPaths
    XPATH_TITLE_ELEMENT = etree.XPath(PREFIX + ":" + INFO_TAG + "/" + PREFIX + ":" + TITLE_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_NAME_ELEMENT = etree.XPath(PREFIX + ":" + INFO_TAG + "/" + PREFIX + ":" + AUTHOR_TAG + "/" + PREFIX + ":" + NAME_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_EMAIL_ELEMENT = etree.XPath(PREFIX + ":" + INFO_TAG + "/" + PREFIX + ":" + AUTHOR_TAG + "/" + PREFIX + ":" + EMAIL_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_DESCRIPTION_ELEMENT = etree.XPath(PREFIX + ":" + INFO_TAG + "/" + PREFIX + ":" + DESCRIPTION_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_RULE_ELEMENTS = etree.XPath("//" + PREFIX + ":" + RULES_TAG + "/" + PREFIX + ":" + RULE_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_CONDITION_ELEMENTS = etree.XPath(PREFIX + ":" + CONDITIONS_TAG + "/" + PREFIX + ":" + CONDITION_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_MATCH_ATTRIBUTE = etree.XPath(PREFIX + ":" + CONDITIONS_TAG + "/@" + MATCH_ATTRIBUTE, namespaces=XPATH_NAMESPACE)
    XPATH_PATH_ELEMENT = etree.XPath("//" + PREFIX + ":" + PATHS_TAG + "/" + PREFIX + ":" + PATH_TAG + "[@" + NAME_ATTRIBUTE + "=$name]", namespaces=XPATH_NAMESPACE)
    XPATH_FOLDER_ELEMENTS = etree.XPath(".//" + PREFIX + ":" + FOLDER_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_FILE_ELEMENT = etree.XPath(".//" + PREFIX + ":" + FILE_TAG, namespaces=XPATH_NAMESPACE)
    XPATH_MACRO_ELEMENT = etree.XPath("//" + PREFIX + ":" + MACROS_TAG + "/" + PREFIX + ":" + MACRO_TAG + "[@" + NAME_ATTRIBUTE + "=$name]", namespaces=XPATH_NAMESPACE)
    XPATH_TEXT_ELEMENTS = etree.XPath(".//" + PREFIX + ":" + TEXT_TAG, namespaces=XPATH_NAMESPACE)
        
    def __init__(self, file):
        """Constructor for the :class:`.Directive`."""
        
        self.file_path = file
        self._root = etree.parse(self.file_path).getroot()
    
    def get_name(self):
        
        return self._root.get(self.NAME_ATTRIBUTE)
    
    def get_info(self):
        """Gets the contents of the 'info' element and returns a dictionary with the keys as the tag names for each child element."""
        
        info = {}
        
        title_element = self.XPATH_TITLE_ELEMENT(self._root)
        
        if title_element:
            title_element = title_element[0]
            info[self.TITLE_TAG] = title_element.text.strip()
        else:
            info[self.TITLE_TAG] = None
        
        name_element = self.XPATH_NAME_ELEMENT(self._root)
        email_element = self.XPATH_EMAIL_ELEMENT(self._root)
        
        if name_element:
            name_element = name_element[0]
            info[self.NAME_TAG] = name_element.text.strip()
        else:
            info[self.NAME_TAG] = None
        
        if email_element:
            email_element = email_element[0]
            info[self.EMAIL_TAG] = email_element.text.strip()
        else:
            info[self.EMAIL_TAG] = None
        
        description_element = self.XPATH_DESCRIPTION_ELEMENT(self._root)
        
        if description_element:
            description_element = description_element[0]
            info[self.DESCRIPTION_TAG] = description_element.text.strip()
            format_value = description_element.get(self.FORMAT_ATTRIBUTE)
            info[self.FORMAT_ATTRIBUTE] = format_value
        else:
            info[self.DESCRIPTION_TAG] = None
        
        return info
        
    def get_destination(self, filer_context):
        """Determines the destination for a filer context.
        
        :param _filer_context: A dictionary. Contains the variables used within a directive to create rules, folder names, and file names.
            
            This is a container for the various variables that can be references by their names within the directive XML file to create rules and text.
            
            See also:
            
            :ref: `create_context`
        
        """
        
        path_name = None
        self._filer_context = filer_context
        
        for rule_element in self.XPATH_RULE_ELEMENTS(self._root):
            path_name = self._process_rule(rule_element)
            
            if path_name is not None:
                break
        
        if path_name is None:
            raise DirectiveError("A path could not be determined")
        else:
            return self._process_path(path_name)

    def _process_rule(self, rule_element):
        """Processes a rule element.
        
        This retrieves the path name if a rule condition is met.
        
        :param rule_element: An etree element. The 'rule' XML node.
        
        """
        
        path_name = None
        
        condition_results = []        
        
        for condition_element in self.XPATH_CONDITION_ELEMENTS(rule_element):
            condition_results.append(self._get_condition_result(condition_element))
        
        match = self.XPATH_MATCH_ATTRIBUTE(rule_element)
        
        if match:
            match = match[0].lower()
        else:
            raise DirectiveError("The '%s' attribute is missing for the '%s' element" % (self.MATCH_ATTRIBUTE, self.CONDITIONS_TAG))
        
        if self._is_match(match, condition_results):
            path_name = rule_element.get(self.PATH_ATTRIBUTE)
            
            if path_name is None:
                raise DirectiveError("The '%s' attribute is missing for the '%s' element" % (self.PATH_ATTRIBUTE, self.RULE_TAG))
        
        return path_name

    def _process_path(self, name):
        """Processes a path element by its name attribute.
        
        Retrieves a list of folders and a file name based on a path name.
        
        :param name: A String. The value of the 'name' attribute for the path XML node.
        
        """
        
        path_element = self.XPATH_PATH_ELEMENT(self._root, name=name)
        
        if not path_element:
            raise DirectiveError("The '%s' path could not be found" % name)
        else:
            path_element = path_element[0]
        
        folder_names = []
                            
        for folder_element in self.XPATH_FOLDER_ELEMENTS(path_element):
            folder_name = self._get_value(folder_element)
            folder_names.append(folder_name)
            
        file_element = self.XPATH_FILE_ELEMENT(path_element, name=path_element.get(self.NAME_ATTRIBUTE))
        
        if not file_element:
            raise DirectiveError("The '%s' element is missing the child '%s' element" % (self.PATH_TAG, self.FILE_TAG))
        else:
            return folder_names, self._get_value(file_element[0])

    def _process_macro(self, name):
        """Processes a macro element by its name attribute.
        
        Retrieves text based on a macro node.
        
        :param name: A String. The value of the 'name' attribute for the macro XML node.
        
        """
        
        macro_element = self.XPATH_MACRO_ELEMENT(self._root, name=name)
        
        if not macro_element:
            raise DirectiveError("The '%s' macro could not be found")
        else:
            macro_element = macro_element[0]
        
        if len(macro_element):
            text = ''
            
            for child in macro_element:
                if child.tag == self.TEXT_TAG_FULL_NAME:
                    text = text + self._get_text(child)
                elif child.tag == self.DATE_TAG_FULL_NAME:
                    text = text + self._get_date_text(child)
                else:
                    raise DirectiveError("The '%s' element is unknown as a '%s' element child" % (child.tag, self.MACRO_TAG))
            
            return text
        else:
            raise DirectiveError("The '%s' macro is missing one or more '%s' child elements" % (name, self.TEXT_TAG))

    def _is_match(self, match, results):
        """Determines if the rule is match and should be used to determine the path.
        
        :param match: A String. The match conditions attribute value.
        :param results: A List. The boolean values of each condition in the rule.
        
        """
        
        if match == self.CONDITIONS_MATCH_ALL:
            return all(results)
        elif match == self.CONDITIONS_MATCH_ANY:
            return any(results)
        else:
            raise DirectiveError("The '%s' attribute value for the '%s' tag is unknown" % (self.MATCH_ATTRIBUTE, self.CONDITIONS_TAG))
    
    def _get_condition_result(self, condition_element):
        """Gets the boolean result from a condition element.
        
        :param condition_element: An etree element. The 'condition' XML node.
        
        """
        
        type_value = condition_element.get(self.TYPE_ATTRIBUTE)
        variable = condition_element.get(self.VARIABLE_ATTRIBUTE)
        value = condition_element.get(self.VALUE_ATTRIBUTE)
        case_sensitive = condition_element.get(self.CASE_SENSITIVE_ATTRIBUTE)
        
        if type_value is None:
            raise DirectiveError("The '%s' attribute is missing from the '%s' tag" % (self.TYPE_ATTRIBUTE, self.CONDITION_TAG))
        else:
            type_value = type_value.lower()
        
        # TODO: Add support for wildcard variable, which states any variable can be used.
        
        if variable is None:
            raise DirectiveError("The '%s' attribute is missing from the '%s' tag" % (self.VARIABLE_ATTRIBUTE, self.CONDITION_TAG))
        elif variable in self._filer_context:
            variable = self._filer_context[variable]
        else:
            raise DirectiveError("The '%s' value for the '%s' attribute is not a context variable" % (variable, self.VARIABLE_ATTRIBUTE))
            
        if value is None:
            raise DirectiveError("The '%s' attribute is missing from the '%s' tag" % (self.VALUE_ATTRIBUTE, self.CONDITION_TAG))
        
        if case_sensitive is None:
            variable = variable.lower()
            value = value.lower()
        elif case_sensitive.lower() == self.FALSE_ATTRIBUTE_VALUE:
            variable = variable.lower()
            value = value.lower()
        elif case_sensitive.lower() == self.TRUE_ATTRIBUTE_VALUE:
            pass
        else:
            raise DirectiveError("The '%s' attribute value for the '%s' tag is unknown" % (self.CASE_SENSITIVE_ATTRIBUTE, self.CONDITION_TAG))
            
        if type_value == self.CONDITION_TYPE_EQUALS:
            if value == self.ANY_VALUE_WILDCARD:
                return True
            else:
                return variable == value
        elif type_value == self.CONDITION_TYPE_GREATER_THAN:
            return variable > value
        elif type_value == self.CONDITION_TYPE_LESS_THAN:
            return variable < value
        elif type_value == self.CONDITION_TYPE_NOT_EQUAL:
            return variable != value
        elif type_value == self.CONDITION_TYPE_HAS:
            return value in variable
        else:
            raise DirectiveError("The '%s' attribute value for the '%s' tag is unknown" % (self.TYPE_ATTRIBUTE, self.CONDITION_TAG))
    
    def _get_text(self, text_element):
        """Gets the formatted text from a text element.
       
        :param text_element. An etree element. The 'text' XML node.
        
        """
        
        text = self._get_value(text_element)
        
        # Only format the text if it is non-empty
        if text:
            text = self._format_text(text, text_element)
            
        return text
    
    def _get_date_text(self, date_element):
        """Gets the formatted date text from a date element.
       
        :param date_element: An etree element. A 'date' XML node.
        
        """
        
        variable_name = date_element.get(self.VARIABLE_ATTRIBUTE) 
        format_value = date_element.get(self.FORMAT_ATTRIBUTE)
        
        if variable_name is None:
            raise DirectiveError("The '%s' element is missing the '%s' attribute" % (self.DATE_TAG, self.VARIABLE_ATTRIBUTE))
        elif format_value is None:
            raise DirectiveError("The '%s' element is missing the '%s' attribute" % (self.DATE_TAG, self.FORMAT_ATTRIBUTE))
        else:
            value = self._get_variable_value(variable_name)
            
            try:
                formatted_value = value.strftime(format_value)
                
                if formatted_value == format_value:
                    raise DirectiveError("The '%s' attribute value for the '%s' element is not a valid format string" % (self.FORMAT_ATTRIBUTE, self.DATE_TAG))
                else:
                    return formatted_value 
            except AttributeError:
                raise DirectiveError("The '%s' attribute value for the '%s' element is not a date or time" % (self.VARIABLE_ATTRIBUTE, self.DATE_TAG)) 
    
    def _get_value(self, element):
        """Gets the value for an element.
        
        The value is either the text from the 'value' attribute, the text from the 'variable' attribute, or the text from a 'macro' attribute.
        The variable text is converted from the filer context based on the name of the variable. The macro text is the output from processing a macro.
        
        :param element: An etree element. Any XML that can have a 'value', 'variable', or 'macro' attribute.
        
        """
        
        value = element.get(self.VALUE_ATTRIBUTE)
        variable_name = element.get(self.VARIABLE_ATTRIBUTE)
        macro_name = element.get(self.MACRO_ATTRIBUTE)
        
        if value is not None:
            return value
        elif variable_name is not None:
            return self._get_variable_value(variable_name)
        elif macro_name is not None:
            return self._process_macro(macro_name)
        else:
            raise DirectiveError("The '%s' element is missing either the '%s', '%s', or '%s' attribute" % (element.tag, self.VALUE_ATTRIBUTE, self.VARIABLE_ATTRIBUTE, self.MACRO_ATTRIBUTE))
    
    def _get_variable_value(self, variable_name):
        """Gets the text from a filer context variable.
        
        :param variable_name: A String. The name of the variable in the filer context.
        
        """
        
        if variable_name in self._filer_context:
            return self._filer_context[variable_name]
        else:
            raise DirectiveError("The '%s' value for the '%s' attribute is not a context variable" % (variable_name, self.VARIABLE_ATTRIBUTE))
    
    def _format_text(self, text, text_element): 
        """Formats the text based on the attributes of the text element.
        
        :param text: A String. The text to format.
        :param text_element: An etree element. The text element.
        
        """
        
        # The order is important in the tuple. The various text formatting attributes will be
        # applied in the order in the tuple and the prefix and suffix should be applied after
        # replacing spaces and setting case.
        format_methods = (self._format_case, self._format_replace_spaces_with, self._format_prefix, self._format_suffix)
        
        for format_method in format_methods:
            text = format_method(text, text_element)
        
        return text
    
    def _format_case(self, text, text_element):
        """Formats text based on the 'case' attribute.
        
        If the 'case' attribute is not present in the 'text' element, nothing will be formatted.
        
        :param text: A String. The text to format.
        :param text_element: An etree element. The 'text' XML node.
        
        """
            
        case = text_element.get(self.CASE_ATTRIBUTE)
        
        if case is None:
            return text
        else:
            case = case.lower()
            
        if case == self.TEXT_CASE_LOWER:
            return text.lower()
        elif case == self.TEXT_CASE_UPPER:
            return text.upper()
        elif case == self.TEXT_CASE_TITLE:
            return text.title()
        else:
            raise DirectiveError("The '%s' attribute value for the '%s' tag is unknown" % (self.CASE_ATTRIBUTE, self.TEXT_TAG))
        
    def _format_replace_spaces_with(self, text, text_element):
        """Replaces spaces in a text based on the 'replace-spaces-with' attribute of a 'text' element.
        
        If the 'replace-spaces-with' attribute is not present in the 'text' element, nothing will be replaced.
        
        :param text: A String. The text to replace spaces.
        :param text_element: An etree element. The 'text' XML node.
        
        """
            
        space_replacement = text_element.get(self.REPLACE_SPACES_WITH_ATTRIBUTE)
            
        if space_replacement is None:
            return text
        else:
            return text.replace(' ', space_replacement) 
        
    def _format_prefix(self, text, text_element):
        """Prefixes text with the 'prefix' attribute value of a 'text' element.
        
        If the 'prefix' attribute is not present in the 'text' element, nothing will be prefixed.
        
        :param text: A String. The text to prefix.
        :param text_element: An etree element. The 'text' XML node.
        
        """
            
        prefix = text_element.get(self.PREFIX_ATTRIBUTE)
            
        if prefix is None:
            return text
        else:
            return prefix + text
    
    def _format_suffix(self, text, text_element):
        """Suffixes text with the 'suffix' attribute value of a 'text' element.
        
        If the 'suffix' attribute is not present in the 'text' element, nothing will be suffixed.
        
        :param text: A String. The text to suffix.
        :param text_element: An etree element. The 'text' XML node.
        
        """
            
        suffix = text_element.get(self.SUFFIX_ATTRIBUTE)
            
        if suffix is None:
            return text
        else:
            return text + suffix

class Validator(object):
    """Checks a directive to see if it is usable for directing a filer."""
    
    def __init__(self):
        """Constructor for the :class:`.Validator`."""
        
        # TODO: Implement the validator.
        pass