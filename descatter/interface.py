# descatter/interface.py
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

import argparse
import cmd

import config

class CommandLine(object):
    
    # Configuration keys
    SECTION_NAME = 'CommandLine'
    SHORT_PREFIX = 'ShortPrefix'
    LONG_PREFIX = 'LongPrefix'
    CONSOLE_ARGUMENT_SHORT_NAME = 'ConsoleArgumentShortName'
    CONSOLE_ARGUMENT_LONG_NAME = 'ConsoleArgumentLongName'
    CONSOLE_ARGUMENT_HELP = 'ConsoleArgumentHelp'
    CONFIG = config.CONFIG[SECTION_NAME]
    
    def __init__(self):
        """Constructor for the :class:'.CommandLine'."""
        
        self.parser = argparse.ArgumentParser()    
        self.parser.add_argument(self.CONFIG[self.SHORT_PREFIX] +
                                 self.CONFIG[self.CONSOLE_ARGUMENT_SHORT_NAME],
                                 self.CONFIG[self.LONG_PREFIX] +
                                 self.CONFIG[self.CONSOLE_ARGUMENT_LONG_NAME],
                                 action='store_true',
                                 help=self.CONFIG[self.CONSOLE_ARGUMENT_HELP])
        
    def parse(self, param_args=None):
        
        args = vars(self.parser.parse_args(param_args))
                      
        if args[self.CONFIG[self.CONSOLE_ARGUMENT_LONG_NAME]]:
            Console().cmdloop()

class Console(cmd.Cmd):
    
    # Configuration keys
    SECTION_NAME = 'Console'
    INTRODUCTION = 'Introduction'
    PROMPT = 'Prompt'
    DESCRIPTION = 'Description'
    SHORT_PREFIX = 'ShortPrefix'
    LONG_PREFIX = 'LongPrefix'
    DIRECTIVE_ARGUMENT_SHORT_NAME = 'DirectiveArgumentShortName'
    DIRECTIVE_ARGUMENT_LONG_NAME = 'DirectiveArgumentLongName'
    DIRECTIVE_ARGUMENT_HELP = 'DirectiveArgumentHelp'
    CONFIG = config.CONFIG[SECTION_NAME]
    
    intro = CONFIG[INTRODUCTION]
    prompt = CONFIG[PROMPT].strip() + ' '
    
    def __init__(self):
        """Constructor for the :class:'.Console'."""
        
        self._directive = None
        self.parser = argparse.ArgumentParser(description=self.CONFIG[self.DESCRIPTION])
        self.parser.add_argument(self.CONFIG[self.SHORT_PREFIX] +
                                 self.CONFIG[self.DIRECTIVE_ARGUMENT_SHORT_NAME],
                                 self.CONFIG[self.LONG_PREFIX] +
                                 self.CONFIG[self.DIRECTIVE_ARGUMENT_LONG_NAME],
                                 action='store_true',
                                 help=self.CONFIG[self.DIRECTIVE_ARGUMENT_HELP])
        
        super(Console, self).__init__()               
    
    def do_cwd(self, line):
        """Displays the current working directive."""
        
        print(line)
            
    def do_file(self, line):
        """Files a source file to a destination folder based on a directive."""
        
        print(line)
        
    def do_exit(self, line):
        """Safely exits the console."""
        
        return True
    
    def do_quit(self, line):
        """Safely exits the console."""
        
        return self.do_exit(line)