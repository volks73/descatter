try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
          'name': 'Zombie File',
          'author': 'Christopher R. Field',
          'description': 'A brain-dead simple system for organizing scientific data files',
          'url': 'http://github.com/zombie-file/zombie-file.git',
          'download_url': 'http://github.com/zombie-file/zombie-file.git',
          'author_email': 'cfield2@gmail.com',
          'version': '0.0.1',
          'install_requires': [],
          'packages': [],
          'scripts': []
}

setup(**config)