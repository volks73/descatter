try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
          'name': 'Descatter',
          'author': 'Christopher R. Field',
          'description': 'A desktop application for organizing, cataloging, and tagging files',
          'url': '',
          'download_url': '',
          'author_email': 'cfield2@gmail.com',
          'version': '0.0.1',
          'install_requires': [],
          'packages': [],
          'scripts': []
}

setup(**config)