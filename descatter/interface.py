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

from prettytable import PrettyTable

class ConsoleError(Exception): pass
        
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
    FILE_COMMAND_PROG = config.cfg[SECTION_NAME]['FileCommandProg'].strip()
    FILE_COMMAND_DESCRIPTION = config.cfg[SECTION_NAME]['FileCommandDescription'].strip()
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
    NAME_ARGUMENT_NAME = config.cfg[SECTION_NAME]['NameArgumentLongName'].strip()
    NAME_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['NameArgumentShortName'].strip()
    NAME_ARGUMENT_HELP = config.cfg[SECTION_NAME]['NameArgumentHelp'].strip()
    VERBOSE_ARGUMENT_NAME = config.cfg[SECTION_NAME]['VerboseArgumentLongName'].strip()
    VERBOSE_ARGUMENT_SHORT_NAME = config.cfg[SECTION_NAME]['VerboseArgumentShortName'].strip()
    VERBOSE_ARGUMENT_HELP = config.cfg[SECTION_NAME]['VerboseArgumentHelp'].strip()
    HISTORY_COMMAND_PROG = config.cfg[SECTION_NAME]['HistoryCommandProg'].strip()
    HISTORY_COMMAND_DESCRIPTION = config.cfg[SECTION_NAME]['HistoryCommandDescription'].strip()
    HISTORY_NAME_COLUMN = config.cfg[SECTION_NAME]['HistoryTableNameColumn'].strip()
    HISTORY_FILE_PATH_COLUMN = config.cfg[SECTION_NAME]['HistoryTableFilePathColumn'].strip()
    
    intro = INTRODUCTION
    prompt = PROMPT
    
    def __init__(self):
        """Constructor for the :class:'.Console'."""
        
        # TODO: Create default directive that simply copies the files to the destination without change.
        self._most_recent = None
        self._history = {}
        super(Console, self).__init__()               

    def add_directive(self, directive):
        
        self._most_recent = directive
        self._history[directive.get_name()] = directive

    def get_directive(self, args):
        """Gets the directive."""
        
        directive_value = args[self.DIRECTIVE_ARGUMENT_NAME]
        name_value = args[self.NAME_ARGUMENT_NAME]
        
        if directive_value:
            return organize.Directive(directive_value)
        elif name_value:
            if name_value in self._history:
                return self._history[name_value]
            else:
                raise ConsoleError("Directive '%s' not found in history of used directives" % name_value)
        else:
            if self._most_recent is None:
                raise ConsoleError("No directive has been previously used")
            else:
                return self._most_recent
            
    def do_file(self, line):
        """Files a source file to a destination folder based on a directive."""
        
        parser = ConsoleParser(prog=self.FILE_COMMAND_PROG,
                               description=self.FILE_COMMAND_DESCRIPTION)
        parser.add_argument(self.SOURCE_ARGUMENT_NAME,
                            help=self.SOURCE_ARGUMENT_HELP)
        parser.add_argument(self.DESTINATION_ARGUMENT_NAME,
                            help=self.DESTINATION_ARGUMENT_HELP)
        parser.add_argument(ConsoleParser.PREFIX +
                            self.DIRECTIVE_ARGUMENT_SHORT_NAME,
                            ConsoleParser.PREFIX + ConsoleParser.PREFIX +
                            self.DIRECTIVE_ARGUMENT_NAME,
                            help=self.DIRECTIVE_ARGUMENT_HELP)
        parser.add_argument(ConsoleParser.PREFIX +
                            self.RECURSIVE_ARGUMENT_SHORT_NAME,
                            ConsoleParser.PREFIX + ConsoleParser.PREFIX +
                            self.RECURSIVE_ARGUMENT_NAME,
                            action='store_true',
                            help=self.RECURSIVE_ARGUMENT_HELP)
        parser.add_argument(ConsoleParser.PREFIX +
                            self.MOVE_ARGUMENT_SHORT_NAME,
                            ConsoleParser.PREFIX + ConsoleParser.PREFIX +
                            self.MOVE_ARGUMENT_NAME,
                            action='store_true',
                            help=self.MOVE_ARGUMENT_HELP)
        parser.add_argument(ConsoleParser.PREFIX +
                            self.NAME_ARGUMENT_SHORT_NAME,
                            ConsoleParser.PREFIX + ConsoleParser.PREFIX +
                            self.NAME_ARGUMENT_NAME,                            
                            help=self.NAME_ARGUMENT_HELP)
        parser.add_argument(ConsoleParser.PREFIX +
                            self.VERBOSE_ARGUMENT_SHORT_NAME,
                            ConsoleParser.PREFIX + ConsoleParser.PREFIX +
                            self.VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help=self.VERBOSE_ARGUMENT_HELP)
    
        # TODO: Add verbose argument to display text while filing.
    
        args = parser.parse_line(line)
        
        if args:
            try:
                source = args[self.SOURCE_ARGUMENT_NAME]
                destination = args[self.DESTINATION_ARGUMENT_NAME]
                directive = self.get_directive(args)
                recursive = args[self.RECURSIVE_ARGUMENT_NAME]
                move = args[self.MOVE_ARGUMENT_NAME]
                            
                filer = organize.Filer(directive)
                filer.file(source, destination, recursive, move)
                self.add_directive(directive)
            except organize.FilerError as error:
                print(error)
            except ConsoleError as error:
                print(error)
    
    def do_history(self, line):
        """Displays the recently used directives."""
        
        parser = ConsoleParser(prog=self.HISTORY_COMMAND_PROG,
                               description=self.HISTORY_COMMAND_DESCRIPTION)
        
        args = parser.parse_line(line)
        
        if args:
            try:
                history_table = PrettyTable([self.HISTORY_NAME_COLUMN, self.HISTORY_FILE_PATH_COLUMN])
                history_table.align[self.HISTORY_FILE_PATH_COLUMN] = 'l'
                
                for name, directive in self._history.items():
                    history_table.add_row([name, directive.file_path])
                
                print(history_table) 
            except ConsoleError as error:
                print(error)
        
    def do_exit(self, line):
        """Safely exits the console."""
        
        return True
    
    def do_quit(self, line):
        """Safely exits the console."""
        
        return self.do_exit(line)

class ConsoleParser(argparse.ArgumentParser):

    PREFIX = config.cfg[Console.SECTION_NAME]['Prefix'].strip()
    HELP_ARGUMENT_NAME = config.cfg[Console.SECTION_NAME]['HelpArgumentLongName'].strip()
    HELP_ARGUMENT_SHORT_NAME = config.cfg[Console.SECTION_NAME]['HelpArgumentShortName'].strip()
    HELP_ARGUMENT_HELP = config.cfg[Console.SECTION_NAME]['HelpArgumentHelp'].strip()    

    def __init__(self, *args, **kwargs):
        super(ConsoleParser, self).__init__(prefix_chars=self.PREFIX, add_help=False, *args, **kwargs)
        self.errors = []
        self.add_argument(self.PREFIX +
                          self.HELP_ARGUMENT_SHORT_NAME,
                          self.PREFIX + self.PREFIX +
                          self.HELP_ARGUMENT_NAME,
                          action='store_true',
                          help=self.HELP_ARGUMENT_HELP)

    def print_errors(self):
        for error in self.errors:
            self.print_usage()
            print(error)

    def parse_line(self, line):
        """Helper function that parses the console input line."""
        
        args = vars(self.parse_args(line.split()))
    
        if args[ConsoleParser.HELP_ARGUMENT_NAME]:
            self.print_help()
            args = None
        elif self.errors:
            self.print_errors()
            args = None
        else:
            return args
    
    # The exit function must be overridden otherwise the help argument will exit the
    # application and therefore the console. The console should only exit when
    # the users enters the 'exit' or 'quit' command.
    def exit(self, status=0, message=None):
        pass
         
    def error(self, message):
        # Keep track of all error messages, but do not display to the user unless the 'help' argument has NOT been set.
        # The argparse parent class will print an error message if positional arguments are not present but the
        # 'help' argument is also included. I want all errors and arguments to be ignored if the 'help' argument
        # is included. This is a result of the argparse module being used to parse console commands instead of its
        # intended purpose of parsing command line arguments.
        self.errors.append(message)