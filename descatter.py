# descatter.py
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
import configparser

import descatter

CONFIG_FILE_NAME = 'descatter.ini'
DIRECTIVES_FOLDER_NAME = 'directives'

config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)

def find_default_directive(file):

    default_directive = None

    root_folder_path = os.path.abspath(file)
    directive_folder_path = os.path.abspath(descatter.get_file_path(os.path.join(DIRECTIVES_FOLDER_NAME, file)))

    if os.path.isfile(root_folder_path):
        default_directive = descatter.Directive(root_folder_path)
    elif os.path.isfile(directive_folder_path):
        default_directive = descatter.Directive(directive_folder_path)
    
    return default_directive

cli = descatter.CommandLine(find_default_directive(config['Application']['DefaultDirective']))
cli.parse()