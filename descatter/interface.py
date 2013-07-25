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
import os

import config
import constants
import organize

class ConsoleParser(argparse.ArgumentParser):

    # TODO: Investigate help action in argparse and override it to display help appropriately in console.
    
    # The exit function must be overridden otherwise the help argument will exit the
    # application and therefore the console. The console should only be exitted when
    # the users wants to exit.
    def exit(self, status=0, message=None):
        pass
         
    def error(self, message):
        self.print_usage()

class CommandLine(object):
    
    # Configuration keys
    SECTION_NAME = 'CommandLine'
    SHORT_PREFIX = config.cfg[SECTION_NAME]['ShortPrefix'].strip()
    LONG_PREFIX = config.cfg[SECTION_NAME]['LongPrefix'].strip()
    CONSOLE_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['ConsoleArgumentShortName'].strip()
    CONSOLE_ARGUMENT_LONG_NAME = config.cfg[SECTION_NAME]['ConsoleArgumentLongName'].strip()
    CONSOLE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['ConsoleArgumentHelp'].strip()
    
    
    def __init__(self):
        """Constructor for the :class:'.CommandLine'."""
        
        self.parser = argparse.ArgumentParser()    
        self.parser.add_argument(self.SHORT_PREFIX +
                                 self.CONSOLE_ARGUMENT_SHORT_NAME,
                                 self.LONG_PREFIX +
                                 self.CONSOLE_ARGUMENT_LONG_NAME,
                                 action='store_true',
                                 help=self.CONSOLE_ARGUMENT_HELP)
        
    def parse(self, param_args=None):
        
        args = vars(self.parser.parse_args(param_args))
                      
        if args[self.CONSOLE_ARGUMENT_LONG_NAME]:
            Console().cmdloop()

class Console(cmd.Cmd):
    
    # Configuration keys
    SECTION_NAME = 'Console'
    INTRODUCTION = config.cfg[SECTION_NAME]['Introduction'].strip()
    PROMPT = config.cfg[SECTION_NAME]['Prompt'].strip() + ' '
    SHORT_PREFIX = config.cfg[SECTION_NAME]['ShortPrefix'].strip()
    LONG_PREFIX = config.cfg[SECTION_NAME]['LongPrefix'].strip()
    FILE_COMMAND_DESCRIPTION = config.cfg[SECTION_NAME]['FileCommandDescription'].strip()
    SOURCE_ARGUMENT_NAME = 'source' 
    SOURCE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['SourceArgumentHelp'].strip()
    DESTINATION_ARGUMENT_NAME = 'destination'
    DESTINATION_ARGUMENT_HELP = config.cfg[SECTION_NAME]['DestinationArgumentHelp'].strip()
    DIRECTIVE_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['DirectiveArgumentShortName'].strip()
    DIRECTIVE_ARGUMENT_NAME = config.cfg[SECTION_NAME]['DirectiveArgumentLongName'].strip()
    DIRECTIVE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['DirectiveArgumentHelp'].strip()
    
    intro = INTRODUCTION
    prompt = PROMPT
    
    def __init__(self):
        """Constructor for the :class:'.Console'."""
        
        self._directive = None
        super(Console, self).__init__()               
    
    def do_cwd(self, line):
        """Displays the current working directive."""
        
        print(self._directive)
            
    def do_file(self, line):
        """Files a source file to a destination folder based on a directive."""
        
        parser = ConsoleParser(prog=constants.APPLICATION_NAME,
                               description=self.FILE_COMMAND_DESCRIPTION)
        parser.add_argument(self.SOURCE_ARGUMENT_NAME,
                            help=self.SOURCE_ARGUMENT_HELP)
        parser.add_argument(self.DESTINATION_ARGUMENT_NAME,
                            help=self.DESTINATION_ARGUMENT_HELP)
        parser.add_argument(self.SHORT_PREFIX +
                            self.DIRECTIVE_ARGUMENT_SHORT_NAME,
                            self.LONG_PREFIX +
                            self.DIRECTIVE_ARGUMENT_NAME,
                            action='store_true',
                            help=self.DIRECTIVE_ARGUMENT_HELP)
        
        args = vars(parser.parse_args(line.split()))
              
        if args[self.DIRECTIVE_ARGUMENT_NAME]:
            self._directive = organize.Directive(args[self.DIRECTIVE_ARGUMENT_NAME])
                    
        if self._directive is None:
            print("No directive was selected and there was no previously used directive")
        else:
            filer = organize.Filer(self._directive)
                    
            source = args[self.SOURCE_ARGUMENT_NAME]
            destination = args[self.DESTINATION_ARGUMENT_NAME]
                    
            if os.path.isdir(source):
                filer.file_folder(source, destination, False)
            else:
                source_list = source.split(',')
                filer.file_list(source_list, destination, False)

        
    def do_exit(self, line):
        """Safely exits the console."""
        
        return True
    
    def do_quit(self, line):
        """Safely exits the console."""
        
        return self.do_exit(line)