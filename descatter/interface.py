import argparse
import os 
import constants
import catalog
import sys

class CommandLine(object):
    
    def __init__(self):
        self.catalog = None
        self.parser = argparse.ArgumentParser(description='An application for cataloging, organizing, and tagging files', prog='descatter')
        subparsers = self.parser.add_subparsers(help="sub-command help")

        parser_create = subparsers.add_parser(constants.CREATE_SUBCOMMAND_NAME, help="creates a catalog")
        parser_create.add_argument('path', nargs='?', default=os.getcwd(), help="path of new catalog")
        parser_create.set_defaults(func=self.create_catalog)

    def parse(self):
        args = self.parser.parse_args()
        
        if len(sys.argv) > 1:
            args.func(args.path)
            
    def create_catalog(self, path):
        self.catalog = catalog.Catalog()
        self.catalog.create(path)