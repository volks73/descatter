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

"""Interfaces for using the Descatter application.

Provides a number of interfaces for interacting with the Descatter application.
These interactions include a command line interface (CLI), an interactive console, and a graphical user interface (GUI).

"""

import argparse
import cmd
import os

import descatter

from prettytable import PrettyTable

class ConsoleError(Exception): 
    """Raised when the interface console encounters an error in the syntax of a command."""
    pass
        
class CommandLine(object):
    """The command line interface."""
    
    # Configuration keys
    SECTION_NAME = 'CommandLine'
    SHORT_PREFIX = descatter.config[SECTION_NAME]['ShortPrefix'].strip()
    LONG_PREFIX = descatter.config[SECTION_NAME]['LongPrefix'].strip()
    CONSOLE_ARGUMENT_SHORT_NAME = descatter.config[SECTION_NAME]['ConsoleArgumentShortName'].strip()
    CONSOLE_ARGUMENT_LONG_NAME = descatter.config[SECTION_NAME]['ConsoleArgumentLongName'].strip()
    CONSOLE_ARGUMENT_HELP = descatter.config[SECTION_NAME]['ConsoleArgumentHelp'].strip()
    
    
    def __init__(self):
        """Constructor for the :class:`.CommandLine`."""
        
        self.parser = argparse.ArgumentParser()    
        self.parser.add_argument(self.SHORT_PREFIX +
                                 self.CONSOLE_ARGUMENT_SHORT_NAME,
                                 self.LONG_PREFIX +
                                 self.CONSOLE_ARGUMENT_LONG_NAME,
                                 action='store_true',
                                 help=self.CONSOLE_ARGUMENT_HELP)
        
    def parse(self, param_args=None):
        """Parses the arguments supplied from the shell."""
        
        args = vars(self.parser.parse_args(param_args))
                      
        if args[self.CONSOLE_ARGUMENT_LONG_NAME]:
            Console().cmdloop()

class Console(cmd.Cmd):
    """The interactive console interface."""
    
    # Configuration keys
    SECTION_NAME = 'Console'
    INTRODUCTION = descatter.config[SECTION_NAME]['Introduction'].strip()
    PROMPT = descatter.config[SECTION_NAME]['Prompt'].strip() + ' '
    FILE_COMMAND_PROG = descatter.config[SECTION_NAME]['FileCommandProg'].strip()
    FILE_COMMAND_DESCRIPTION = descatter.config[SECTION_NAME]['FileCommandDescription'].strip()
    SOURCE_ARGUMENT_NAME = 'source' 
    SOURCE_ARGUMENT_HELP = descatter.config[SECTION_NAME]['SourceArgumentHelp'].strip()
    DESTINATION_ARGUMENT_NAME = 'destination'
    DESTINATION_ARGUMENT_HELP = descatter.config[SECTION_NAME]['DestinationArgumentHelp'].strip()
    DIRECTIVE_ARGUMENT_SHORT_NAME = descatter.config[SECTION_NAME]['DirectiveArgumentShortName'].strip()
    DIRECTIVE_ARGUMENT_NAME = descatter.config[SECTION_NAME]['DirectiveArgumentLongName'].strip()
    DIRECTIVE_ARGUMENT_HELP = descatter.config[SECTION_NAME]['DirectiveArgumentHelp'].strip()
    RECURSIVE_ARGUMENT_NAME = descatter.config[SECTION_NAME]['RecursiveArgumentLongName'].strip()
    RECURSIVE_ARGUMENT_SHORT_NAME = descatter.config[SECTION_NAME]['RecursiveArgumentShortName'].strip()
    RECURSIVE_ARGUMENT_HELP = descatter.config[SECTION_NAME]['RecursiveArgumentHelp'].strip()
    MOVE_ARGUMENT_NAME = descatter.config[SECTION_NAME]['MoveArgumentLongName'].strip()
    MOVE_ARGUMENT_SHORT_NAME = descatter.config[SECTION_NAME]['MoveArgumentShortName'].strip()
    MOVE_ARGUMENT_HELP = descatter.config[SECTION_NAME]['MoveArgumentHelp'].strip()
    NAME_ARGUMENT_NAME = descatter.config[SECTION_NAME]['NameArgumentLongName'].strip()
    NAME_ARGUMENT_SHORT_NAME = descatter.config[SECTION_NAME]['NameArgumentShortName'].strip()
    NAME_ARGUMENT_HELP = descatter.config[SECTION_NAME]['NameArgumentHelp'].strip()
    VERBOSE_ARGUMENT_NAME = descatter.config[SECTION_NAME]['VerboseArgumentLongName'].strip()
    VERBOSE_ARGUMENT_SHORT_NAME = descatter.config[SECTION_NAME]['VerboseArgumentShortName'].strip()
    VERBOSE_ARGUMENT_HELP = descatter.config[SECTION_NAME]['VerboseArgumentHelp'].strip()
    HISTORY_COMMAND_PROG = descatter.config[SECTION_NAME]['HistoryCommandProg'].strip()
    HISTORY_COMMAND_DESCRIPTION = descatter.config[SECTION_NAME]['HistoryCommandDescription'].strip()
    HISTORY_NAME_COLUMN = descatter.config[SECTION_NAME]['HistoryTableNameColumn'].strip()
    HISTORY_FILE_PATH_COLUMN = descatter.config[SECTION_NAME]['HistoryTableFilePathColumn'].strip()
    
    intro = INTRODUCTION
    prompt = PROMPT
    
    def __init__(self):
        """Constructor for the :class:`.Console`."""
        
        self._history = {}
        default_directive_file_name = descatter.config[self.SECTION_NAME]['DefaultDirective']
        default_directive_file_path = descatter.get_file_path(descatter.DIRECTIVES_FOLDER_NAME, default_directive_file_name)
        self._most_recent = descatter.Directive(default_directive_file_path)
        self.add_directive(self._most_recent)
        super(Console, self).__init__()               

    def add_directive(self, directive):
        """Adds a directive to the history of used directives.
        
        :param directive: A :class:`.Directive` object.
                
        """
        
        self._most_recent = directive
        self._history[directive.get_name()] = directive

    def get_directive(self, args):
        """Returns a directive to use for the 'file' command.
        
        If a directive is supplied with the '-d' argument, then it will be returned.
        If the '-d' argument is not used, then a directive will be returned based on its name from the histroy of used directives if the '-n' argument is used. 
        If the '-d' and '-n' arguments are not used, then the most recently used directive will be returned. 
        The most recently used directive is by default, the default.xml directive upon first usage of the 'file' command. 
        
        :param args: A list. The arguments submitted with the command.
        
        """
        
        directive_value = args[self.DIRECTIVE_ARGUMENT_NAME]
        name_value = args[self.NAME_ARGUMENT_NAME]
        
        if directive_value:
            return descatter.Directive(directive_value)
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

    def file_started(self, *args):
        """Called when a filing is started.
        
        See also:
        
        :ref: :class:`.Filer`
        
        """
        
        print("Filed: %s to " % args[0], end="")
    
    def file_completed(self, *args):
        """Called when a filing is completed.
        
        See also:
        
        :ref: :class:`.Filer`
        
        """
        
        print("%s" % args[0][1])
    
    def file_failed(self, *args):
        """Called when a filing has failed.
        
        See also:
        
        :ref: :class:`.Filer`
        
        """
        
        print("FAIL!")
            
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
    
        args = parser.parse_line(line)
        
        if args:
            try:
                source = args[self.SOURCE_ARGUMENT_NAME]
                destination = args[self.DESTINATION_ARGUMENT_NAME]
                directive = self.get_directive(args)
                recursive = args[self.RECURSIVE_ARGUMENT_NAME]
                move = args[self.MOVE_ARGUMENT_NAME]
                
                filer = descatter.Filer(directive)
                
                if args[self.VERBOSE_ARGUMENT_NAME]:
                    filer.subscribe(self)
                    
                filer.file(source, destination, recursive, move)
                self.add_directive(directive)
            except descatter.FilerError as error:
                print(error)
            except ConsoleError as error:
                print(error)
    
    def do_history(self, line):
        """Displays the recently used directives."""
        
        parser = ConsoleParser(prog=self.HISTORY_COMMAND_PROG,
                               description=self.HISTORY_COMMAND_DESCRIPTION)
        
        # TODO: Add verbose or absolute argument to display paths as absolute paths as opposed to relative paths.
        
        args = parser.parse_line(line)
        
        if args:
            try:
                history_table = PrettyTable([self.HISTORY_NAME_COLUMN, self.HISTORY_FILE_PATH_COLUMN])
                history_table.align[self.HISTORY_FILE_PATH_COLUMN] = 'l'
                
                for name, directive in self._history.items():
                    history_table.add_row([name, os.path.relpath(directive.file_path)])
                
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
    """A modified argument parser to use with the console.
    
    The :class:`.ArgumentParser` of the `argparse` module provides a lot of desirable functionality for parsing console commands and arguments, but it is designed for parsing arguments from the command line interface (CLI). 
    For example, the default parser exits the application after showing the help message. 
    If the help argument is supplied, the command is still executed. 
    The :class:`.ConsoleParser` does not exist after displaying the help message and all other arguments are ignored if the help argument is detected.
    
    Errors in parsing console arguments are saved in a list and can be access later rather than raising an error and exiting the application.
    
    """

    PREFIX = descatter.config[Console.SECTION_NAME]['Prefix'].strip()
    HELP_ARGUMENT_NAME = descatter.config[Console.SECTION_NAME]['HelpArgumentLongName'].strip()
    HELP_ARGUMENT_SHORT_NAME = descatter.config[Console.SECTION_NAME]['HelpArgumentShortName'].strip()
    HELP_ARGUMENT_HELP = descatter.config[Console.SECTION_NAME]['HelpArgumentHelp'].strip()    

    def __init__(self, *args, **kwargs):
        """Constructor for the :class:`.ConsoleParser`.
        
        The prefix character is defined from the configuration file for the application. 
        The default help action defined in the parent class is disabled and a new help argument is added. 
        The new help argument action is 'store_true' so that if the 'help' argument is detected, it prints the help message without exiting.  
        
        """
        
        super(ConsoleParser, self).__init__(prefix_chars=self.PREFIX, add_help=False, *args, **kwargs)
        self.errors = []
        self.add_argument(self.PREFIX +
                          self.HELP_ARGUMENT_SHORT_NAME,
                          self.PREFIX + self.PREFIX +
                          self.HELP_ARGUMENT_NAME,
                          action='store_true',
                          help=self.HELP_ARGUMENT_HELP)

    def print_errors(self):
        """Prints the list of errors to the console."""
        
        for error in self.errors:
            self.print_usage()
            print(error)

    def parse_line(self, line):
        """Parses the console input line.
        
        This should be used instead of the 'parse_args' method of the :class:`.ArgumentParser`.
        If a 'help' argument is detected, the help message is printed and the rest of the arguments are ignored and 'None' is returned.
        Also, the rest of arguments are still parsed for correctness and any errors are saved in the 'self.errors' attribute, but the errors are not automatically displayed.        
        If errors are detected and the 'help' argument is not detected, the errors are printed and 'None' is returned.
        Otherwise, the arguments are parsed and returned as a dictionary instead of a :class:`.Namespace` object. 
            
        """
        
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
        """Overrides the parent 'exit' method to avoid exiting the console."""
        pass
         
    def error(self, message):
        """Overrides the parent 'error' method to avoid exiting.
        
        All error messages are saved in an internal list and can be displayed to the console using the 'print_errors' method. 
        Errors are still determined, but not printed if the 'help' argument is detected.
        
        """
        
        # Keep track of all error messages, but do not display to the user unless the 'help' argument has NOT been set.
        # The argparse parent class will print an error message if positional arguments are not present but the
        # 'help' argument is also included. I want all errors and arguments to be ignored if the 'help' argument
        # is included. This is a result of the argparse module being used to parse console commands instead of its
        # intended purpose of parsing command line arguments.
        self.errors.append(message)