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

# TODO: Test paths with spaces

import argparse
import cmd
import os

from descatter import organize, metadata
from prettytable import PrettyTable

ARGUMENT_PREFIX = '-'
SOURCE_ARGUMENT_NAME = 'source' 
DESTINATION_ARGUMENT_NAME = 'destination'
TAG_ARGUMENT_NAME = 'tag'
DIRECTIVE_ARGUMENT_NAME = 'directive'
MOVE_ARGUMENT_NAME = 'move'
RECURSIVE_ARGUMENT_NAME = 'recursive'
VERBOSE_ARGUMENT_NAME = 'verbose'
ABSOLUTE_ARGUMENT_NAME = 'absolute'
FILE_ARGUMENT_NAME = 'file'
CONSOLE_ARGUMENT_NAME = 'interactive'
HELP_ARGUMENT_NAME = 'help'

def file(source, destination, directive, recursive, move, verbose, absolute):
    """Files a file.
    
    :param source: A path or list. The path to a file, the path to a folder, or a list of paths to copy or move.
    :param destination: A path. The folder where the source will be copied or moved.
    :param directive: An :class:`.Directive' object. The directive to control the copy or move of the source to the destination.
    :param recursive: A boolean value. 'True' if the source is a path to a folder, all files in the folder and subfolders will be copied or moved.
    :param move: A boolean value. 'True' the source is copied to the destination and then deleted at the source. 'False' the source is only copied.
    :param verbose: A boolean value. 'True' additional information is displayed during the filing.
    :param absolute: A boolean value. 'True' all paths are displayed as absolute paths. 'False' all paths are displayed as relative or abbreviated paths.
    
    """
                  
    filer = organize.Filer(directive)    
              
    if verbose:
        filer.subscribe(FilerListener(absolute))
                    
    filer.file(source, destination, recursive, move)

def tag(file, tag_name):
    """Tags a file.
    
    :param tag: A string. A tag to place on a file.
    :param file: A path. A path to a file to be tagged.
    
    """
    
    session = metadata.Session()
            
    db_tag = session.query(metadata.Tag).filter_by(name=tag_name).first()
    db_file = session.query(metadata.File).filter_by(path=file).first()
            
    if not db_tag:
        db_tag = metadata.Tag(tag_name)
            
    if not db_file:
        db_file = metadata.File(file)
        session.add(db_file)
        
    db_file.tags.append(db_tag)
            
    session.commit()
    session.close()

class ConsoleError(Exception): 
    """Raised when the interactive console interface encounters an error."""
    pass

class CommandLineError(Exception): 
    """Raised when the command line interface encounters an error."""
    pass

class CommandLine(object):
    """The command line interface."""
        
    def __init__(self, loaded, default):
        """Constructor for the :class:`.CommandLine`.
        
        :param loaded: A dictionary of :class:`.Directive` objects.
        :param default: A :class:`.Directive` object. The default directive to use if the '-d' argument is not specified.
        
        """
        
        self._loaded = loaded       
        self._default = default
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument(ARGUMENT_PREFIX + 'i',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + CONSOLE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Starts the interactive console')
        self._parser.add_argument(ARGUMENT_PREFIX + 'f',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + FILE_ARGUMENT_NAME,
                                 nargs=2,
                                 help='Files a source to a destination based on a directive')
        self._parser.add_argument(ARGUMENT_PREFIX + 't',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + TAG_ARGUMENT_NAME,
                                 nargs=2,
                                 help='Files a source to a destination based on a directive')
        self._parser.add_argument(ARGUMENT_PREFIX + 'd',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + DIRECTIVE_ARGUMENT_NAME,                              
                                 help='Defines the directive to use when filing. The most recent past directive will be used for the filing if this argument is omitted')
        self._parser.add_argument(ARGUMENT_PREFIX + 'm',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + MOVE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Moves the source to the destination, which deletes the source after copying to the destination')
        self._parser.add_argument(ARGUMENT_PREFIX + 'r',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + RECURSIVE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Files all files in every sub-folder if the source is a folder')
        self._parser.add_argument(ARGUMENT_PREFIX + 'v',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + VERBOSE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Displays additional status information during and after filing')
        self._parser.add_argument(ARGUMENT_PREFIX + 'a',
                                 ARGUMENT_PREFIX + ARGUMENT_PREFIX + ABSOLUTE_ARGUMENT_NAME,
                                 action='store_true',
                                 help='Displays all paths as absolute paths')
        
    def parse(self, param_args=None):
        """Parses the arguments supplied from the shell."""
        
        args = vars(self._parser.parse_args(param_args))
                      
        if args[CONSOLE_ARGUMENT_NAME]:
            self._do_console(args)
        elif args[FILE_ARGUMENT_NAME]:
            self._do_file(args)
        else:
            print("Nothing to do!")
    
    def _do_console(self, args):
        """Run the interfacetive console."""
        
        Console(self._loaded, self._default).cmdloop()
    
    def _do_file(self, args):
        """Run the file command."""
        
        source = args[self.file_arg][0]
        destination = args[self.file_arg][1]
        directive = self._get_directive(args[self.DIRECTIVE_ARGUMENT_NAME])
        recursive = args[self.recursive_arg]
        move = args[self.move_arg]
        verbose = args[self.verbose_arg]
        absolute = args[self.absolute_arg]       

        file(source, destination, directive, recursive, move, verbose, absolute)
    
    def _get_directive(self, source):
        """Get the directive.
        
        :param source: A path or string. A path to a directive file or the name of loaded directive. If 'None', the default directive is used.
        
        """
        
        if source is None:
            return self._default
        elif source in self._loaded:
            return self._loaded[source]
        elif os.path.isfile(source):
            return organize.Directive(source)
        else:
            raise CommandLineError("A directive could not be determined!")          

class Console(cmd.Cmd):
    """The interactive console interface."""
    
    intro = 'Welcome to the descatter interactive console!'
    prompt = 'descatter: '
    
    def __init__(self, loaded, default):
        """Constructor for the :class:`.Console`.
        
        :param loaded: A distionary of :class:`.Directive` objects. The directives loaded during application start.
        :param default: A :class:`.Directive` object. The default directive to use if no directive is specified.
        
        """
        
        self._loaded = loaded
        self._history = {}
        self._most_recent = default
        super(Console, self).__init__()               

    def _add_to_history(self, directive):
        """Adds a directive to the history of used directives.
        
        :param directive: A :class:`.Directive` object.
                
        """
        
        self._most_recent = directive
        self._history[directive.get_name()] = directive

    def _get_directive(self, source):
        """Returns a directive to use for the 'file' command. 
        
        :param source: A string or path. If string, then the directive will be found from the history or loaded directives. If path, then the directive will be loaded from the path.
        
        """
        
        if source is None:
            return self._most_recent
        elif source in self._history:
            return self._history[source]
        elif source in self._loaded:
            return self._loaded[source]
        elif os.path.isfile(source):
            return organize.Directive(source)
        else:
            raise ConsoleError("A directive could not be determined!") 
    
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
                               description='Files a source to a destination based on a directive. The directive is saved as the default directive after successful completion of the command.')
        
        parser.add_argument(SOURCE_ARGUMENT_NAME,
                            help='A file path, a comma-separated list of file paths, or a folder path to be filed.')
        parser.add_argument(DESTINATION_ARGUMENT_NAME,
                            help='The folder where the source will be filed.')
        parser.add_argument(ARGUMENT_PREFIX + 'd',
                            '--' + DIRECTIVE_ARGUMENT_NAME,                              
                            help='Defines the directive to use when filing. The most recent past directive will be used for the filing if this argument is omitted. The value can be the name of directive that was preloaded at the start of the application, the name of directive in the history, or the path to a directive file.')
        parser.add_argument(ARGUMENT_PREFIX + 'm',
                            '--' + MOVE_ARGUMENT_NAME,
                            action='store_true',
                            help='Moves the source to the destination, which deletes the source after copying to the destination.')
        parser.add_argument(ARGUMENT_PREFIX + 'r',
                            '--' + RECURSIVE_ARGUMENT_NAME,
                            action='store_true',
                            help='Files all files in every sub-folder if the source is a folder.')
        parser.add_argument(ARGUMENT_PREFIX + 'v',
                            '--' + VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays additional status information during and after filing.')
        parser.add_argument(ARGUMENT_PREFIX + 'a',
                            '--' + ABSOLUTE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays all paths as absolute paths.')
    
        args = parser.parse_line(line)
        
        if args:
            try:
                source = args[SOURCE_ARGUMENT_NAME]
                destination = args[DESTINATION_ARGUMENT_NAME]
                directive = self._get_directive(args[DIRECTIVE_ARGUMENT_NAME])
                recursive = args[RECURSIVE_ARGUMENT_NAME]
                move = args[MOVE_ARGUMENT_NAME]
                verbose = args[VERBOSE_ARGUMENT_NAME]
                absolute = args[ABSOLUTE_ARGUMENT_NAME]
        
                file(source, destination, directive, recursive, move, verbose, absolute)
                
                self._add_to_history(directive)
            except organize.FilerError as error:
                print(error)
            except ConsoleError as error:
                print(error)
    
    def do_history(self, line):
        """Displays the recently used directives."""
        
        parser = ConsoleParser(prog='history',
                               description="Displays a list of recently used directives that can be called by name in the 'file' command")
        parser.add_argument(ARGUMENT_PREFIX + 'v',
                            '--' + VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays additional information about each directive')
        parser.add_argument(ARGUMENT_PREFIX + 'a',
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
        parser.add_argument(ARGUMENT_PREFIX + 'v',
                            '--' + VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays additional information about the recently used directive')
        parser.add_argument(ARGUMENT_PREFIX + 'a',
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

    def do_loaded(self, line):
        """Displays the directives loaded at the start of the application."""
        
        parser = ConsoleParser(prog='loaded',
                               description="Displays a list of loaded directives that can be called by name in the 'file' command")
        parser.add_argument(ARGUMENT_PREFIX + 'v',
                            '--' + VERBOSE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays additional information about each directive')
        parser.add_argument(ARGUMENT_PREFIX + 'a',
                            '--' + ABSOLUTE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays all paths as absolute paths')
        
        args = parser.parse_line(line)
        
        if args:
            try:
                verbose = args[VERBOSE_ARGUMENT_NAME]
                absolute = args[ABSOLUTE_ARGUMENT_NAME]
            
                self._print_directive_table(self._loaded.values(), verbose, absolute) 
            except ConsoleError as error:
                print(error)
    
    def do_tag(self, line):
        """Tags a file."""
        
        parser = ConsoleParser(prog='tag',
                               description="Places a tag on a file")
        parser.add_argument(FILE_ARGUMENT_NAME,
                            help='The path to the file to be tagged.')
        parser.add_argument(TAG_ARGUMENT_NAME,
                            help='A file path, a comma-separated list of file paths, or a folder path to be filed.')
        
        args = parser.parse_line(line)
        
        if args:
            file = args[FILE_ARGUMENT_NAME]
            tag_name = args[TAG_ARGUMENT_NAME]
            
            if os.path.isfile(file):
                tag(file, tag_name)
            else:
                print("Failed to tag file. The path must be to a file.")

    def do_files(self, line):
        """Lists all files that have been tagged."""
        
        parser = ConsoleParser(prog='files',
                               description="Displays a list of tagged files and the tags associated with each file as a comma-separated list.")
        parser.add_argument(ARGUMENT_PREFIX + 'a',
                            '--' + ABSOLUTE_ARGUMENT_NAME,
                            action='store_true',
                            help='Displays all paths as absolute paths')
        
        args = parser.parse_line(line)
        
        if args:
            absolute = args[ABSOLUTE_ARGUMENT_NAME]
            session = metadata.Session()
            files = session.query(metadata.File).order_by(metadata.File.id)
                        
            files_table = PrettyTable(['files', 'tags'])
            files_table.align['files'] = 'l'
            files_table.align['tags'] = 'l'
        
            for file in files:
                tag_names = []
                for tag in file.tags:
                    tag_names.append(tag.name)
                
                file_path = ''
                if absolute:
                    file_path = os.path.abspath(file.path)
                else:
                    parent = os.path.dirname(file.path)
                    parent = os.path.basename(parent)
                    file_path =  os.path.join(parent, os.path.basename(file.path))
                    
                files_table.add_row([file_path, ','.join(tag_names)])
                        
            print(files_table)
            
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