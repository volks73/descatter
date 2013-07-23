# tests/test_directive.py
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

import os
import unittest

import organize
import config

from lxml import etree
from datetime import datetime

class TestCondition(unittest.TestCase):
    """Test 'condition' element in the XML directive file and its related children elements and attributes."""
    
    def setUp(self):
        
        self.xpath_condition_element = etree.XPath(("//" +
                                                    organize.Directive.PREFIX + 
                                                    ":" + 
                                                    organize.Directive.RULES_TAG + 
                                                    "/" + 
                                                    organize.Directive.PREFIX + 
                                                    ":" + 
                                                    organize.Directive.RULE_TAG + 
                                                    "[@" +
                                                    organize.Directive.NAME_ATTRIBUTE +
                                                    "=$name]/"+
                                                    organize.Directive.PREFIX +
                                                    ":" + 
                                                    organize.Directive.CONDITIONS_TAG +
                                                    "/" +
                                                    organize.Directive.PREFIX +
                                                    ":" + 
                                                    organize.Directive.CONDITION_TAG), 
                                                   namespaces=organize.Directive.XPATH_NAMESPACE)
        
        self.directive = organize.Directive(os.path.join(config.DATA_FOLDER_PATH, "test_directive_TestCondition.xml"))
        
        context = {}
        context[organize.Filer.CURRENT_DATETIME] = datetime.now()
        context[organize.Filer.FILE_COUNT] = str(10)
        context[organize.Filer.FILE_EXTENSION] = 'txt'
        context[organize.Filer.FILE_DATE_ACCESSED] = datetime.now()
        context[organize.Filer.FILE_DATE_CREATED] = datetime.now()
        context[organize.Filer.FILE_DATE_MODIFIED] = datetime.now()
        context[organize.Filer.FILE_INDEX] = str(5)
        context[organize.Filer.FILE_NAME] = 'test_file'
        context[organize.Filer.FILE_PATH] = os.getcwd()
        context[organize.Filer.FILE_SIZE] = str(0)
        context[organize.Filer.FILE_SOURCE_PATH] = os.getcwd()
        
        self.directive._filer_context = context
    
    def tearDown(self):
        pass
    
    def test_type_equals(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-equals-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertTrue(output_value)
    
    def test_type_equals_not(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-equals-not-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertFalse(output_value)
        
    def test_type_equals_wildcard(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-equals-wildcard-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertTrue(output_value)
     
    def test_type_greater_than(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-greater-than-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertTrue(output_value)
     
    def test_type_greater_than_not(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-greater-than-not-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertFalse(output_value)
     
    def test_type_less_than(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-less-than-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertTrue(output_value)
     
    def test_type_less_than_not(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-less-than-not-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertFalse(output_value)
        
    def test_type_not_equal(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-not-equal-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertTrue(output_value)
    
    def test_type_not_equal_not(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-not-equal-not-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertFalse(output_value)
     
    def test_type_unknown(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-unknown-rule')[0]
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)
     
    def test_type_missing(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='type-missing-rule')[0] 
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)

    def test_case_sensitive_true(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='case-sensitive-true-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertFalse(output_value)
        
    def test_case_sensitive_false(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='case-sensitive-false-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertTrue(output_value)

    def test_case_sensitive_unknown(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='case-sensitive-unknown-rule')[0]
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)

    def test_case_sensitive_missing(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='case-sensitive-missing-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
        self.assertTrue(output_value)
    
    def test_variable_unknown(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='variable-unknown-rule')[0] 
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)
         
    def test_variable_missing(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='variable-missing-rule')[0] 
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)
     
    def test_value_missing(self):
        
        condition_element = self.xpath_condition_element(self.directive._root, name='value-missing-rule')[0] 
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)

class TestRule(unittest.TestCase):
    """Test 'rule' element in the XML directive file and its related children elements and attributes.""" 
    
    def setUp(self):
        
        self.xpath_rule_element = etree.XPath(("//" +
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.RULES_TAG + 
                                               "/" + 
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.RULE_TAG + 
                                               "[@" +
                                               organize.Directive.NAME_ATTRIBUTE +
                                               "=$name]"), 
                                              namespaces=organize.Directive.XPATH_NAMESPACE)
        
        self.directive = organize.Directive(os.path.join(config.DATA_FOLDER_PATH, "test_directive_TestRule.xml"))
        
        context = {}
        context[organize.Filer.CURRENT_DATETIME] = datetime.now()
        context[organize.Filer.FILE_COUNT] = str(10)
        context[organize.Filer.FILE_EXTENSION] = 'txt'
        context[organize.Filer.FILE_DATE_ACCESSED] = datetime.now()
        context[organize.Filer.FILE_DATE_CREATED] = datetime.now()
        context[organize.Filer.FILE_DATE_MODIFIED] = datetime.now()
        context[organize.Filer.FILE_INDEX] = str(5)
        context[organize.Filer.FILE_NAME] = 'test_file'
        context[organize.Filer.FILE_PATH] = os.getcwd()
        context[organize.Filer.FILE_SIZE] = str(0)
        context[organize.Filer.FILE_SOURCE_PATH] = os.getcwd()
        
        self.directive._filer_context = context
    
    def tearDown(self):
        pass
    
    def test_match_any(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='match-any-rule')[0]
        expected_value = rule_element.get(organize.Directive.PATH_ATTRIBUTE)
        output_value = self.directive._process_rule(rule_element)
     
        self.assertEqual(output_value, expected_value)
     
    def test_match_any_not(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='match-any-not-rule')[0]
        output_value = self.directive._process_rule(rule_element)
     
        self.assertIsNone(output_value)
    
    def test_match_all(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='match-all-rule')[0]
        expected_value = rule_element.get(organize.Directive.PATH_ATTRIBUTE)
        output_value = self.directive._process_rule(rule_element)
     
        self.assertEqual(output_value, expected_value)
     
    def test_match_all_not(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='match-all-not-rule')[0]
        output_value = self.directive._process_rule(rule_element)
     
        self.assertIsNone(output_value)
     
    def test_match_unknown(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='match-unknown-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._process_rule, rule_element)
     
    def test_match_missing(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='match-missing-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._process_rule, rule_element)
    
    def test_path_missing(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='path-missing-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._process_rule, rule_element)
        
    def test_conditions_missing(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='conditions-missing-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._process_rule, rule_element)
    
    def test_condition_missing(self):
        rule_element = self.xpath_rule_element(self.directive._root, name='condition-missing-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._process_rule, rule_element)

class TestPath(unittest.TestCase):
    """Test 'path' element in the XML directive file and its related children elements and attributes."""
    
    def setUp(self):
        
        self.xpath_path_element = etree.XPath(("//" +
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.PATHS_TAG + 
                                               "/" + 
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.PATH_TAG + 
                                               "[@" +
                                               organize.Directive.NAME_ATTRIBUTE +
                                               "=$name]"), 
                                              namespaces=organize.Directive.XPATH_NAMESPACE)
        
        self.directive = organize.Directive(os.path.join(config.DATA_FOLDER_PATH, "test_directive_TestPath.xml"))
        
        context = {}
        context[organize.Filer.CURRENT_DATETIME] = datetime.now()
        context[organize.Filer.FILE_COUNT] = str(10)
        context[organize.Filer.FILE_EXTENSION] = 'txt'
        context[organize.Filer.FILE_DATE_ACCESSED] = datetime.now()
        context[organize.Filer.FILE_DATE_CREATED] = datetime.now()
        context[organize.Filer.FILE_DATE_MODIFIED] = datetime.now()
        context[organize.Filer.FILE_INDEX] = str(5)
        context[organize.Filer.FILE_NAME] = 'file_variable'
        context[organize.Filer.FILE_PATH] = 'folder_variable'
        context[organize.Filer.FILE_SIZE] = str(0)
        context[organize.Filer.FILE_SOURCE_PATH] = os.getcwd()
        
        self.directive._filer_context = context
    
    def tearDown(self):
        pass
    
    def test_file(self):
        
        output_value = self.directive._process_path('file')[1]
        self.assertEqual(output_value, 'file')
    
    def test_file_missing(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_path, 'file-missing')
    
    def test_file_variable(self):
        
        output_value = self.directive._process_path('file-variable')[1]
        self.assertEqual(output_value, 'file_variable')
    
    def test_file_macro(self):
        
        output_value = self.directive._process_path('file-macro')[1]
        self.assertEqual(output_value, 'file_macro_name')
    
    def test_file_value_missing(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_path, 'file-value-missing')
    
    def test_file_variable_unknown(self):

        self.assertRaises(organize.DirectiveError, self.directive._process_path, 'file-variable-unknown')
        
    def test_file_macro_unknown(self):

        self.assertRaises(organize.DirectiveError, self.directive._process_path, 'file-macro-unknown')
    
    def test_folder(self):
        
        folder_names, file_name = self.directive._process_path('folder')
        self.assertEqual(file_name, 'folder_file')
        self.assertEqual(folder_names[0], 'folder')
    
    def test_folder_value_missing(self):

        self.assertRaises(organize.DirectiveError, self.directive._process_path, 'folder-value-missing')
        
    def test_folder_variable(self):

        folder_names, file_name = self.directive._process_path('folder-variable')
        self.assertEqual(file_name, 'folder_variable_file')
        self.assertEqual(folder_names[0], 'folder_variable')

    def test_folder_variable_unknown(self):

        self.assertRaises(organize.DirectiveError, self.directive._process_path, 'folder-variable-unknown')
        
    def test_folder_macro(self):
        
        folder_names, file_name = self.directive._process_path('folder-macro')
        self.assertEqual(file_name, 'folder_macro_file')
        self.assertEqual(folder_names[0], 'folder_macro_name')

    def test_folder_macro_unknown(self):

        self.assertRaises(organize.DirectiveError, self.directive._process_path, 'folder-macro-unknown')
    
    def test_folder_nested(self):
        
        folder_names, file_name = self.directive._process_path('folder-nested')
        self.assertEqual(file_name, 'folder_nested_file')
        
        for index in range(len(folder_names)):
            self.assertEqual(folder_names[index], 'nested_' + str(index) + '_folder')

class TestMacro(unittest.TestCase):
    """Test 'macro' element in the XML directive file and its related children elements and attributes."""
    
    def setUp(self):
        
        self.xpath_macro_element = etree.XPath(("//" +
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.MACROS_TAG + 
                                               "/" + 
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.MACRO_TAG + 
                                               "[@" +
                                               organize.Directive.NAME_ATTRIBUTE +
                                               "=$name]"), 
                                              namespaces=organize.Directive.XPATH_NAMESPACE)
        
        self.directive = organize.Directive(os.path.join(config.DATA_FOLDER_PATH, "test_directive_TestMacro.xml"))
        
        context = {}
        context[organize.Filer.CURRENT_DATETIME] = datetime.now()
        context[organize.Filer.FILE_COUNT] = str(10)
        context[organize.Filer.FILE_EXTENSION] = 'txt'
        context[organize.Filer.FILE_DATE_ACCESSED] = datetime.now()
        context[organize.Filer.FILE_DATE_CREATED] = datetime.now()
        context[organize.Filer.FILE_DATE_MODIFIED] = datetime.now()
        context[organize.Filer.FILE_INDEX] = str(5)
        context[organize.Filer.FILE_NAME] = 'file_variable'
        context[organize.Filer.FILE_PATH] = 'folder_variable'
        context[organize.Filer.FILE_SIZE] = str(0)
        context[organize.Filer.FILE_SOURCE_PATH] = os.getcwd()
        
        self.directive._filer_context = context
    
    def tearDown(self):
        pass
    
    def test_child_unknown(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'child-unknown')
    
    def test_text_value(self):
        
        output_value = self.directive._process_macro('text-value')
        self.assertEqual(output_value, 'text_value')
    
    def test_text_missing(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'text-missing')
        
    def test_text_value_missing(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'text-value-missing')
    
    def test_text_variable(self):
        
        output_value = self.directive._process_macro('text-variable')
        self.assertEqual(output_value, 'file_variable')    
    
    def test_text_variable_unknown(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'text-variable-unknown')
    
    def test_text_macro(self):
        
        output_value = self.directive._process_macro('text-macro')
        self.assertEqual(output_value, 'text_value')
    
    def test_text_macro_unknown(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'text-macro-unknown')
    
    def test_text_prefix(self):
        
        output_value = self.directive._process_macro('text-prefix')
        self.assertEqual(output_value, 'prefix_text')
    
    def test_text_suffix(self):
        
        output_value = self.directive._process_macro('text-suffix')
        self.assertEqual(output_value, 'text_suffix')
    
    def test_text_replace_underscore(self):
        
        output_value = self.directive._process_macro('text-replace-underscore')
        self.assertEqual(output_value, 'text_replace_underscore')
    
    def test_text_replace_empty(self):
        
        output_value = self.directive._process_macro('text-replace-empty')
        self.assertEqual(output_value, 'TextReplaceEmpty')
    
    def test_text_case_upper(self):
        
        output_value = self.directive._process_macro('text-case-upper')
        self.assertEqual(output_value, 'TEXT CASE UPPER')
    
    def test_text_case_lower(self):
        
        output_value = self.directive._process_macro('text-case-lower')
        self.assertEqual(output_value, 'text case lower')
        
    def test_text_case_title(self):
        
        output_value = self.directive._process_macro('text-case-title')
        self.assertEqual(output_value, 'Text Case Title')
    
    def test_text_case_unknown(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'text-case-unknown')
    
    def test_text_case_all(self):
        
        output_value = self.directive._process_macro('text-all-format')
        self.assertEqual(output_value, 'prefix_Text_All_Format_suffix')
    
    def test_text_compound(self):
        
        output_value = self.directive._process_macro('text-compound')
        self.assertEqual(output_value, 'macro_text_compound')
    
    def test_date_variable(self):
        
        now = datetime.now()
        expected_value = now.strftime('%Y-%m-%d')
        output_value = self.directive._process_macro('date-variable')
        self.assertEqual(output_value, expected_value)
    
    def test_date_variable_missing(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'date-variable-missing')
    
    def test_date_format_missing(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'date-format-missing')
    
    def test_date_variable_unknown(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'date-variable-unknown')
    
    def test_date_variable_not_datetime(self):

        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'date-variable-not-datetime')
    
    def test_date_format_unknown(self):
        
        self.assertRaises(organize.DirectiveError, self.directive._process_macro, 'date-format-unknown')

    def test_date_compound(self):
        
        now = datetime.now()
        expected_value = now.strftime('%Y-%m-%d')
        output_value = self.directive._process_macro('date-compound')
        self.assertEqual(output_value, expected_value)

    def test_text_date_compound(self):
        
        now = datetime.now()
        expected_value = "text_date_compound_" + now.strftime('%Y-%m-%d')
        output_value = self.directive._process_macro('text-date-compound')
        self.assertEqual(output_value, expected_value)
    
    def test_date_text_compound(self):
        
        now = datetime.now()
        expected_value = now.strftime('%Y-%m-%d') + "_date_text_compound"
        output_value = self.directive._process_macro('date-text-compound')
        self.assertEqual(output_value, expected_value)

class TestDestination(unittest.TestCase):
    """Test 'get_destination' method of the 'Directive' class."""
    
    def setUp(self):
        self.xpath_macro_element = etree.XPath(("//" +
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.MACROS_TAG + 
                                               "/" + 
                                               organize.Directive.PREFIX + 
                                               ":" + 
                                               organize.Directive.MACRO_TAG + 
                                               "[@" +
                                               organize.Directive.NAME_ATTRIBUTE +
                                               "=$name]"), 
                                              namespaces=organize.Directive.XPATH_NAMESPACE)
        
        self.directive = organize.Directive(os.path.join(config.DATA_FOLDER_PATH, "test_directive_TestDestination.xml"))
        
        self.context = {}
        self.context[organize.Filer.CURRENT_DATETIME] = datetime.now()
        self.context[organize.Filer.FILE_COUNT] = str(10)
        self.context[organize.Filer.FILE_EXTENSION] = 'file_extension'
        self.context[organize.Filer.FILE_DATE_ACCESSED] = datetime.now()
        self.context[organize.Filer.FILE_DATE_CREATED] = datetime.now()
        self.context[organize.Filer.FILE_DATE_MODIFIED] = datetime.now()
        self.context[organize.Filer.FILE_INDEX] = str(5)
        self.context[organize.Filer.FILE_NAME] = 'file name'
        self.context[organize.Filer.FILE_PATH] = 'file_path'
        self.context[organize.Filer.FILE_SIZE] = str(0)
        self.context[organize.Filer.FILE_SOURCE_PATH] = 'file_source_path'
    
    def tearDown(self):
        pass
    
    def test_destination(self):
        
        expected_file_name = 'prefix_Value_FILE_NAME_suffix'
        expected_folder_names = ('default_folder','file_path','macro_folder')
        folder_names, file_name = self.directive.get_destination(self.context)
        self.assertEquals(file_name, expected_file_name)
        
        for index in range(len(folder_names)):
            self.assertEquals(folder_names[index], expected_folder_names[index])