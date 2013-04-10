import os
import sqlite3

SQLITE_EXTENSION = '.sqlite'

class Catalog(object):
    
    def __init__(self):
        self.db = None    
       
    def get_name_from_path(self, path):
        name = None 
                           
        while not name:
            name = os.path.basename(path)
            path = os.path.dirname(path)
        
        return name     
    
    def connect_database(self, path):
        db_file_name = self.get_name_from_path(path) + SQLITE_EXTENSION
        db_file_path = os.path.join(path, db_file_name)
        
        self.db = sqlite3.connect(db_file_path)
    
    def create_database(self, path):
        self.connect_database(path)
        
        # TODO: Add SQL table creation
        
        self.db.close()
    
    def create_folder_structure(self, path):
        folders = ['content', 'templates', 'hooks', 'log']
        action_subfolders = ['before','after']
        hook_actions = ['create']
        
        for folder in folders:
            folder_path = os.path.join(path, folder)
            os.mkdir(folder_path)
        
            if folder == 'hooks':
                for action in hook_actions:     
                    action_path = os.path.join(folder_path, action)
                    os.mkdir(action_path)
            
                    for subfolder in action_subfolders: 
                        os.mkdir(os.path.join(action_path, subfolder))

    def create(self, path):

        if not os.path.isdir(path):
            raise IOError("The path for creating the catalog is not a folder")
        elif os.listdir(path):
            raise IOError("The folder for creating the catalog is not empty")
        else:
            self.create_folder_structure(path)
            self.create_database(path)
    
    def open(self, path):
        # TODO: Add check if path points to a descatter catalog
        self.path = path
        self.get_name_from_path()