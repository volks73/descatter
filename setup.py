import sys

from cx_Freeze import setup, Executable

executables = [Executable('descatter.py')]

packages = ['lxml',
            'prettytable',
            'descatter']

includes = []

include_files = ['descatter.ini',
                 'directives/',
                 'AUTHORS',
                 'CHANGES',
                 'LICENSE',
                 'README.rst']

excludes = ['Tkinter',
            'tcl',
            'Tkconstants',
            'distutils',
            'email',
            'http',
            'json',
            'lib2to3',
            'nose',
            'unittest',
            'xml',
            'ssl',
            'subprocess',
            'tty',
            'webbrowser',
            'urllib',
            'pickle',
            'doctest',
            'socket']

# excludes = []

path = sys.path + ['descatter']

build_exe_options = {'packages': packages,
                     'includes': includes,
                     'include_files': include_files,
                     'excludes': excludes,
                     'path': path,
                     'append_script_to_exe': True,
                     'create_shared_zip': False,
                     'copy_dependent_files': True}

options = {'build_exe': build_exe_options}

setup(name = 'Descatter',
      version = '0.0.1',
      description = "A cross platform desktop application for organizing, tagging, and searching for files",
      options = options,
      executables = executables)