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
    """Test 'condition' element, or tag in the XML file, and its related attributes processing."""
    
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
    """Test 'conditions' element, or tag in the XML file, and its related attributes processing.""" 
    
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