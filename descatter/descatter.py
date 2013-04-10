import argparse
import os

parser = argparse.ArgumentParser(description='An application for cataloging, organizing, and tagging files', prog='descatter')
subparsers = parser.add_subparsers(dest="sub_command", help="sub-command help")

parser_create = subparsers.add_parser('create', help="creates a catalog")
parser_create.add_argument('path', nargs='?', default=os.getcwd(), help="path of new catalog")

args = parser.parse_args(['create'])
print(args)

if args.sub_command == 'create':
    print('CREATE!')
else:
    print('NO CREATE!')