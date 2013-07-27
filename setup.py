import sys

from cx_Freeze import setup, Executable

# config_file_path = os.path.join('descatter', 'data', 'descatter.ini')

packages = ['lxml',
            'prettytable',
            'descatter']

includes = []

include_files = ['descatter.ini', 'directives/']

excludes = ['Tkinter','tcl','Tkconstants','distutils','email','http','json','lib2to3','nose','unittest','xml']

path = sys.path + ['descatter']

build_exe_options = {'compressed': True,
                     'packages': packages,
                     'includes': includes,
                     'include_files': include_files,
                     'excludes': excludes,
                     'path': path}

options = {'build_exe': build_exe_options}

setup(name = 'Descatter',
      version = '0.0.1',
      description = "A cross platform desktop application for organizing, tagging, and searching for files",
      options = options,
      executables = [Executable('descatter.py')])