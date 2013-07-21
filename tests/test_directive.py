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

TESTS_FOLDER_NAME = 'tests'
TESTS_DATA_FOLDER_NAME = 'data'
TESTS_DATA_FOLDER_PATH = os.path.join(os.path.join(os.getcwd(), TESTS_FOLDER_NAME), TESTS_DATA_FOLDER_NAME)

class TestConditionElement(unittest.TestCase):
    # TODO: Implement tests for condition element
    pass