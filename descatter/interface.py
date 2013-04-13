import argparse
import os 
import constants
import catalog

class CommandLine(object):
    
    def __init__(self):
        self.catalog = None
        self.parser = argparse.ArgumentParser(description='An application for cataloging, organizing, and tagging files', 
                                              prog='descatter')
        
        self.parser.add_argument(constants.CATALOG_ARGUMENT_SHORT_NAME, 
                                 constants.CATALOG_ARGUMENT_LONG_NAME, 
                                 nargs='?', 
                                 default=os.getcwd(), 
                                 help="specify the catalog")
        
        self.parser.add_argument(constants.ESTABLISH_ARGUMENT_SHORT_NAME, 
                                 constants.ESTABLISH_ARGUMENT_LONG_NAME, 
                                 help="establish or create a catalog",
                                 action='store_true')
        
    def parse(self, test_args=None):
        args = self.parser.parse_args(test_args)
    
        if args.establish:
            self.establish_catalog(args.catalog)
        elif args.checkin:
            self.checkin_file(args.file_path)
        else:
            print(args)
    
    def establish_catalog(self, path):
        if not os.path.isdir(path):
            raise OSError("Path to establish the catalog is not a directory")
        
        proceed = False
        response = None
        
        if os.listdir(path):
            while not response:
                print("The folder for establishing a catalog is not empty")
                response = input("Would you like to proceed? (Y/Yes or N/No): ")
            
                if response == 'Y' or response == 'Yes':      
                    proceed = True
                elif response == 'N' or response == 'No':
                    proceed = False
                else:
                    print("Response not recognized, try again")
                    response = None
        else:
            proceed = True
        
        if proceed:
            self.catalog = catalog.Catalog(path)
            self.catalog.establish()
            
            print("Catalog established at '%s'" % path)
        else:
            print("Failed to establish catalog at '%s'" % path)
        
    def destroy_catalog(self, path):
        pass
    
    def checkin_file(self, path):
        pass