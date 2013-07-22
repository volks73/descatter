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
import tempfile
import shutil

import organize

from lxml import etree
from datetime import datetime

TESTS_FOLDER_NAME = 'tests'
TESTS_DATA_FOLDER_NAME = 'data'
TESTS_DATA_FOLDER_PATH = os.path.join(os.path.join(os.getcwd(), TESTS_FOLDER_NAME), TESTS_DATA_FOLDER_NAME)

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
        
        self.directive = organize.Directive(os.path.join(TESTS_DATA_FOLDER_PATH, "test_directive_TestConditionElement.xml"))
        
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
    
    def test_equals(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='equals-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertTrue(output_value)
    
    def test_equals_not(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='equals-not-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertFalse(output_value)
     
    def test_equals_case_sensitive(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='equals-case-sensitive-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertFalse(output_value)

    def test_equals_missing_case_sensitive(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='equals-missing-case-sensitive-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertTrue(output_value)
     
    def test_greater_than(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='greater-than-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertTrue(output_value)
     
    def test_greater_than_not(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='greater-than-not-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertFalse(output_value)
     
    def test_less_than(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='less-than-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertTrue(output_value)
     
    def test_less_than_not(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='less-than-not-rule')[0]
        output_value = self.directive._get_condition_result(condition_element)
     
        self.assertFalse(output_value)
     
    def test_missing_type(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='missing-type-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)
         
    def test_missing_variable(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='missing-variable-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)
     
    def test_missing_value(self):
        condition_element = self.xpath_condition_element(self.directive._root, name='missing-value-rule')[0]
         
        self.assertRaises(organize.DirectiveError, self.directive._get_condition_result, condition_element)

class TestConditions(unittest.TestCase):
    """Test 'conditions' element, or tag in the XML file, and its related attributes processing.""" 
    pass