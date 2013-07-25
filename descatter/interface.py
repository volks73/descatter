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
import organize

class ConsoleParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(ConsoleParser, self).__init__(*args, **kwargs)
        self.errors = []

    def parse_line(self, line):
        """Helper function that parses the console input line."""
        
        return vars(self.parse_args(line.split()))

    # TODO: Investigate help action in argparse and override it to display help appropriately in console.
    
    # The exit function must be overridden otherwise the help argument will exit the
    # application and therefore the console. The console should only exit when
    # the users enters the 'exit' or 'quit' command.
    def exit(self, status=0, message=None):
        pass
         
    def error(self, message):
        self.errors.append(message)
        
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
    FILE_COMMAND_PROG = config.cfg[SECTION_NAME]['FileCommandProg'].strip()
    FILE_COMMAND_DESCRIPTION = config.cfg[SECTION_NAME]['FileCommandDescription'].strip()
    HELP_ARGUMENT_NAME = config.cfg[SECTION_NAME]['HelpArgumentLongName'].strip()
    HELP_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['HelpArgumentShortName'].strip()
    HELP_ARGUMENT_HELP = config.cfg[SECTION_NAME]['HelpArgumentHelp'].strip()
    SOURCE_ARGUMENT_NAME = 'source' 
    SOURCE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['SourceArgumentHelp'].strip()
    DESTINATION_ARGUMENT_NAME = 'destination'
    DESTINATION_ARGUMENT_HELP = config.cfg[SECTION_NAME]['DestinationArgumentHelp'].strip()
    DIRECTIVE_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['DirectiveArgumentShortName'].strip()
    DIRECTIVE_ARGUMENT_NAME = config.cfg[SECTION_NAME]['DirectiveArgumentLongName'].strip()
    DIRECTIVE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['DirectiveArgumentHelp'].strip()
    RECURSIVE_ARGUMENT_NAME = config.cfg[SECTION_NAME]['RecursiveArgumentLongName'].strip()
    RECURSIVE_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['RecursiveArgumentShortName'].strip()
    RECURSIVE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['RecursiveArgumentHelp'].strip()
    MOVE_ARGUMENT_NAME = config.cfg[SECTION_NAME]['MoveArgumentLongName'].strip()
    MOVE_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['MoveArgumentShortName'].strip()
    MOVE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['MoveArgumentHelp'].strip()
    
    intro = INTRODUCTION
    prompt = PROMPT
    
    def __init__(self):
        """Constructor for the :class:'.Console'."""
        
        # TODO: Create default directive that simply copies the files to the destination without change.
        self._directive = None
        super(Console, self).__init__()               

    def get_directive(self, args):
        """Gets the directive."""
        
        argument_value = args[self.DIRECTIVE_ARGUMENT_NAME]
        
        if argument_value:
            return argument_value
        else:
            return self._directive
    
    def print_errors(self, parser):
        for error in parser.errors:
            parser.print_usage()
            print(error)
            
    def do_file(self, line):
        """Files a source file to a destination folder based on a directive."""
        
        parser = ConsoleParser(prog=self.FILE_COMMAND_PROG,
                               description=self.FILE_COMMAND_DESCRIPTION,
                               add_help=False)
        parser.add_argument(self.SOURCE_ARGUMENT_NAME,
                            help=self.SOURCE_ARGUMENT_HELP)
        parser.add_argument(self.DESTINATION_ARGUMENT_NAME,
                            help=self.DESTINATION_ARGUMENT_HELP)
        parser.add_argument(self.SHORT_PREFIX +
                            self.HELP_ARGUMENT_SHORT_NAME,
                            self.LONG_PREFIX +
                            self.HELP_ARGUMENT_NAME,
                            action='store_true',
                            help=self.HELP_ARGUMENT_HELP)
        parser.add_argument(self.SHORT_PREFIX +
                            self.DIRECTIVE_ARGUMENT_SHORT_NAME,
                            self.LONG_PREFIX +
                            self.DIRECTIVE_ARGUMENT_NAME,
                            help=self.DIRECTIVE_ARGUMENT_HELP)
        parser.add_argument(self.SHORT_PREFIX +
                            self.RECURSIVE_ARGUMENT_SHORT_NAME,
                            self.LONG_PREFIX +
                            self.RECURSIVE_ARGUMENT_NAME,
                            action='store_true',
                            help=self.RECURSIVE_ARGUMENT_HELP)
        parser.add_argument(self.SHORT_PREFIX +
                            self.MOVE_ARGUMENT_SHORT_NAME,
                            self.LONG_PREFIX +
                            self.MOVE_ARGUMENT_NAME,
                            action='store_true',
                            help=self.MOVE_ARGUMENT_HELP)
    
        args = parser.parse_line(line)
  
        if args[self.HELP_ARGUMENT_NAME]:
            parser.print_help()
        elif parser.errors:
            self.print_errors(parser)
        else:
            source = args[self.SOURCE_ARGUMENT_NAME]
            destination = args[self.DESTINATION_ARGUMENT_NAME]
            directive = self.get_directive(args)
            recursive = args[self.RECURSIVE_ARGUMENT_NAME]
            move = args[self.MOVE_ARGUMENT_NAME]
            
            try:            
                filer = organize.Filer(directive)
                filer.file(source, destination, recursive, move)
                        
                # If the filing is successfully, save the directive as the default for future calls to file.
                self._directive = directive
            except organize.FilerError as error:
                print(error)
        
    def do_exit(self, line):
        """Safely exits the console."""
        
        return True
    
    def do_quit(self, line):
        """Safely exits the console."""
        
        return self.do_exit(line)