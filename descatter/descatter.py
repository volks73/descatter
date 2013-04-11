import argparse
import os 
import constants

class Descatter(object):
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='An application for cataloging, organizing, and tagging files', prog='descatter')
        subparsers = self.parser.add_subparsers(dest="sub_command", help="sub-command help")

        parser_create = subparsers.add_parser(constants.CREATE_SUBCOMMAND_NAME, help="creates a catalog")
        parser_create.add_argument('path', nargs='?', default=os.getcwd(), help="path of new catalog")

    def run(self):
        args = self.parser.parse_args([constants.CREATE_SUBCOMMAND_NAME])
        print(args)
    
        if args.sub_command == constants.CREATE_SUBCOMMAND_NAME:
            print('CREATE!')
        else:
            print('NO CREATE!')    