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

import descatter.organize

from prettytable import PrettyTable

SOURCE_ARGUMENT_NAME = 'source' 
DESTINATION_ARGUMENT_NAME = 'destination'
DIRECTIVE_ARGUMENT_NAME = 'directive'
MOVE_ARGUMENT_NAME = 'move'
RECURSIVE_ARGUMENT_NAME = 'recursive'
VERBOSE_ARGUMENT_NAME = 'verbose'
ABSOLUTE_ARGUMENT_NAME = 'absolute'
FILE_ARGUMENT_NAME = 'file'
CONSOLE_ARGUMENT_NAME = 'interactive'
HELP_ARGUMENT_NAME = 'help'

def file(source, destination, directive, recursive, move, verbose, absolute):
                  
    filer = descatter.organize.Filer(directive)    
              
    if verbose:
        filer.subscribe(FilerListener(absolute))
                    
    filer.file(source, destination, recursive, move)

class ConsoleError(Exception): 
    """Raised when the interface console encounters an error in the syntax of a command."""
    pass

class CommandLine(object):
    """The command line interface."""
        
    def __init__(self, default_directive):
        """Constructor for the :class:`.CommandLine`."""
               
        self.default_directive = default_directive
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-i',
                                 '--' + CONSOLE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Starts the interactive console')
        self.parser.add_argument('-f',
                                 '--' + FILE_ARGUMENT_NAME,
                                 nargs=2,
                                 help='Files a source to a destination based on a directive')
        self.parser.add_argument('-d',
                                 '--' + DIRECTIVE_ARGUMENT_NAME,                              
                                 help='Defines the directive to use when filing. The most recent past directive will be used for the filing if this argument is omitted')
        self.parser.add_argument('-m',
                                 '--' + MOVE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Moves the source to the destination, which deletes the source after copying to the destination')
        self.parser.add_argument('-r',
                                 '--' + RECURSIVE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Files all files in every sub-folder if the source is a folder')
        self.parser.add_argument('-v',
                                 '--' + VERBOSE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Displays additional status information during and after filing')
        self.parser.add_argument('-a',
                                 '--' + ABSOLUTE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Displays all paths as absolute paths')
        
    def parse(self, param_args=None):
        """Parses the arguments supplied from the shell."""
        
        args = vars(self.parser.parse_args(param_args))
                      
        if args[CONSOLE_ARGUMENT_NAME]:
            self._do_console(args)
        elif args[FILE_ARGUMENT_NAME]:
            self._do_file(args)
        else:
            print("Nothing to do!")
    
    def _do_console(self, args):
        
        Console(self._get_directive(args)).cmdloop()
    
    def _do_file(self, args):
        source = args[self.file_arg][0]
        destination = args[self.file_arg][1]
        recursive = args[self.recursive_arg]
        move = args[self.move_arg]
        verbose = args[self.verbose_arg]
        absolute = args[self.absolute_arg]       

        file(source, destination, self._get_directive(args), recursive, move, verbose, absolute)
    
    def _get_directive(self, args):
               
        if args[DIRECTIVE_ARGUMENT_NAME]:
            return descatter.organize.Directive(args[DIRECTIVE_ARGUMENT_NAME])
        else:
            return self.default_directive            

class Console(cmd.Cmd):
    """The interactive console interface."""
    
    intro = 'Welcome to the descatter interactive console!'
    prompt = 'descatter: '
    
    def __init__(self, default_directive):
        """Constructor for the :class:`.Console`."""
        
        self._history = {}
        self._most_recent = default_directive
        self._add_directive(self._most_recent)
        super(Console, self).__init__()               

    def _add_directive(self, directive):
        """Adds a directive to the history of used directives.
        
        :param directive: A :class:`.Directive` object.
                
        """
        
        self._most_recent = directive
        self._history[directive.get_name()] = directive

    def _get_directive(self, args):
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
            return descatter.organize.Directive(directive_value)
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
    
    def _print_directive_table(self, directives, verbose, absolute):
        """Prints an ASCII table for the list of directives to the console.
        
        :param directives: A list of :class:`.Directive` objects.
        :param verbose: A boolean value. 'True' displays additional information about each directive in the table.
        :param absolute: A boolean value. 'True' displays paths in a absolute path format.
        
        """

        if verbose:
            directive_table = PrettyTable(['name', 'file', 'path'])
            directive_table.align['path'] = 'l'
        else:
            directive_table = PrettyTable(['name', 'file'])
                    
            directive_table.align['file'] = 'l'
        
        for directive in directives:
            name = directive.get_name()
            file_name = os.path.basename(directive.file_path)
            
            if verbose:    
                path = os.path.dirname(directive.file_path)
                        
                if absolute:
                    path = os.path.abspath(path)
                            
                directive_table.add_row([name, file_name, path])
            else:
                directive_table.add_row([name, file_name])
                        
        print(directive_table) 
      
    def do_file(self, line):
        """Files a source file to a destination folder based on a directive."""
        
        parser = ConsoleParser(prog='file',
                               description='Files a source to a destination based on a directive. The directive is saved as the default directive after successful completion of the command')
        
        parser.add_argument(SOURCE_ARGUMENT_NAME,
                            help='A file path, a comma-separated list of file paths, or a folder path to be filed')
        parser.add_argument(DESTINATION_ARGUMENT_NAME,
                            help='The folder where the source will be filed')
        parser.add_argument('-d',
                            '--' + DIRECTIVE_ARGUMENT_NAME,                              
                            help='Defines the directive to use when filing. The most recent past directive will be used for the filing if this argument is omitted')
        parser.add_argument('-m',
                            '--' + MOVE_ARGUMENT_NAME,
                            action='store_true',
                            help='Moves the source to the destination, which deletes the source after copying to the destination')
        parser.add_argument('-r',
                            '--' + RECURSIVE_ARGUMENT_NAME,
                            action='store_true',
                            help='Files all files in every sub-folder if the source is a folder')
        parser.add_argument('-v',
                            '--' + VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays additional status information during and after filing')
        parser.add_argument('-a',
                            '--' + ABSOLUTE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays all paths as absolute paths')
    
        args = parser.parse_line(line)
        
        if args:
            try:
                source = args[SOURCE_ARGUMENT_NAME]
                destination = args[DESTINATION_ARGUMENT_NAME]
                directive = self._get_directive(args)
                recursive = args[RECURSIVE_ARGUMENT_NAME]
                move = args[MOVE_ARGUMENT_NAME]
                verbose = args[VERBOSE_ARGUMENT_NAME]
                absolute = args[ABSOLUTE_ARGUMENT_NAME]
        
                file(source, destination, directive, recursive, move, verbose, absolute)
                
                self._add_directive(directive)
            except descatter.organize.FilerError as error:
                print(error)
            except ConsoleError as error:
                print(error)
    
    def do_history(self, line):
        """Displays the recently used directives."""
        
        parser = ConsoleParser(prog='history',
                               description="Displays a list of recently used directives that can be called by name in the 'file' command")
        parser.add_argument('-v',
                            '--' + VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays additional information about each directive')
        parser.add_argument('-a',
                            '--' + ABSOLUTE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays all paths as absolute paths')
        
        args = parser.parse_line(line)
        
        if args:
            try:
                verbose = args[VERBOSE_ARGUMENT_NAME]
                absolute = args[ABSOLUTE_ARGUMENT_NAME]
            
                self._print_directive_table(self._history.values(), verbose, absolute) 
            except ConsoleError as error:
                print(error)
    
    def do_recent(self, line):
        """Displays the most recently used directive."""
        
        parser = ConsoleParser(prog='recent',
                               description="Displays the most recently used directive that is the default for subsequent calls to 'file' command")
        parser.add_argument('-v',
                            '--' + VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays additional information about the recently used directive')
        parser.add_argument('-a',
                            '--' + ABSOLUTE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays all paths as absolute paths')
        
        args = parser.parse_line(line)
        
        if args:
            try:
                verbose = args[VERBOSE_ARGUMENT_NAME]
                absolute = args[ABSOLUTE_ARGUMENT_NAME]
            
                self._print_directive_table((self._most_recent,), verbose, absolute)
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

    def __init__(self, *args, **kwargs):
        """Constructor for the :class:`.ConsoleParser`.
        
        The prefix character is defined from the configuration file for the application. 
        The default help action defined in the parent class is disabled and a new help argument is added. 
        The new help argument action is 'store_true' so that if the 'help' argument is detected, it prints the help message without exiting.  
        
        """
        
        super(ConsoleParser, self).__init__(add_help=False, *args, **kwargs)
        self.errors = []
        self.add_argument('-h',
                          '--' + HELP_ARGUMENT_NAME,
                          action='store_true',
                          help='Display this message')

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
    
        if args[HELP_ARGUMENT_NAME]:
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

class FilerListener(object):
    """Listener for filer.file events when operating in verbose mode."""
    
    def __init__(self, absolute=False):
        """Constructor for the :class:`.FilerListener`."""
        
        self.absolute = absolute
    
    def file_started(self, *args):
        """Called when a filing is started.
        
        See also:
        
        :ref: :class:`.Filer`
        
        """
        
        source_path = args[0][0]
        
        if self.absolute:
            display = os.path.abspath(source_path)
        else:
            parent = os.path.dirname(source_path)
            parent = os.path.basename(parent)
            display =  os.path.join(parent, os.path.basename(source_path))
        
        print("Filed: %s to " % display, end="")
    
    def file_completed(self, *args):
        """Called when a filing is completed.
        
        See also:
        
        :ref: :class:`.Filer`
        
        """
        
        destination_path = args[0][1]
        
        if self.absolute:
            display = os.path.abspath(destination_path)
        else:
            parent = os.path.dirname(destination_path)
            parent = os.path.basename(parent)
            display =  os.path.join(parent, os.path.basename(destination_path))
        
        print("%s" % display)
    
    def file_failed(self, *args):
        """Called when a filing has failed.
        
        See also:
        
        :ref: :class:`.Filer`
        
        """
        
        print("FAIL!")