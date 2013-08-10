import sys

from cx_Freeze import setup, Executable

console_exe = Executable('descatter-console.py', base='Console', icon='descatter_icon.ico')
cmd_exe = Executable('descatter-cmd.py', base='Win32GUI', icon='descatter_icon.ico')

executables = [console_exe, cmd_exe]

# Explicitly load these packages; otherwise, runtime errors occur because of missing modules during import.
# cx_Freeze should detect this, so I am not sure why I must explicitly state these packages.
packages = ['lxml']
includes = []
excludes = []

include_files = ['descatter.ini',
                 'directives/',
                 'AUTHORS',
                 'CHANGES',
                 'LICENSE',
                 'README.rst',
                 'descatter_icon.ico',
                 'descatter_icon.png']

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