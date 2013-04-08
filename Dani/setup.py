try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
          'name': 'dani',
          'author': 'Christopher R. Field',
          'description': 'A desktop application for catalogin, organizing, and tagging research data files',
          'url': '',
          'download_url': '',
          'author_email': 'cfield2@gmail.com',
          'version': '0.0.1',
          'install_requires': [],
          'packages': [],
          'scripts': []
}

setup(**config)