# descatter/application.py
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

import configparser
import os
import sys

from descatter import organize
from descatter import interface

CONFIG_FILE_NAME = 'descatter.ini'

config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)

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

def _load_directives():
    
    root_folder_path = get_root_folder()
    directives_folder_path = os.path.join(root_folder_path, config['Application']['DirectivesFolderPath'])
    directives_folder_path = os.path.abspath(directives_folder_path)
    
    loaded = {}
    for root, subfolder_names, file_names in os.walk(directives_folder_path):  # @UnusedVariable
        for file_name in file_names:
            directive_file_path = os.path.join(root, file_name)
            directive = organize.Directive(directive_file_path)
            loaded[directive.get_name()] = directive

    return loaded

def main():
    """Starts the descatter application."""
    
    loaded = _load_directives()
    default = loaded[config['Application']['DefaultDirectiveName']]    
    
    cli = interface.CommandLine(loaded, default)
    cli.parse()