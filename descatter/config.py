# descatter/config.py
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

"""Provides information and text based on the application's configuration file."""

import configparser
import os
import sys

import descatter

def get_root_folder():
    
    if getattr(sys, 'frozen', False):
        # The application is frozen
        root_folder = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store data files
        root_folder = os.path.dirname(sys.argv[0])
        
    return root_folder

def get_file_path(*args):
    """Finds a data file."""
    
    return os.path.join(get_root_folder(), *args)

config = configparser.ConfigParser()
config.read(descatter.CONFIG_FILE_NAME)