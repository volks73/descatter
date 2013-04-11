import os
import sqlite3
import constants

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
        db_file_name = self.get_name_from_path(path) + constants.SQLITE_EXTENSION
        db_file_path = os.path.join(path, db_file_name)
        
        self.db = sqlite3.connect(db_file_path)
    
    def create_database(self, path):
        self.connect_database(path)
        
        # TODO: Add SQL table creation
        
        self.db.close()
    
    def create_folder_structure(self, path):        
        for folder_name in constants.CATALOG_FOLDER_NAMES:
            folder_path = os.path.join(path, folder_name)
            os.mkdir(folder_path)
    
            if folder_name == constants.CONTENT_FOLDER_NAME:
                self.create_content_type_folders(folder_path)
        
            if folder_name == constants.HOOKS_FOLDER_NAME:
                for sub_command_name in constants.SUB_COMMAND_NAMES:     
                    sub_command_path = os.path.join(folder_path, sub_command_name)
                    os.mkdir(sub_command_path)
            
                    for trigger_name in constants.TRIGGER_NAMES: 
                        os.mkdir(os.path.join(sub_command_path, trigger_name))
                        
    def create_content_type_folders(self, path):
        if os.path.isdir(path):
            for media_type_name in constants.MEDIA_TYPE_NAMES:
                media_type_path = os.path.join(path, media_type_name)
                os.mkdir(media_type_path)
            
            for media_subtype_name, media_type_name in constants.CONTENT_TYPES.items():
                media_subtype_path = os.path.join(path, media_type_name)
                media_subtype_path = os.path.join(media_subtype_path, media_subtype_name)
                os.mkdir(media_subtype_path)
                
                number_folder_path = os.path.join(media_subtype_path, '1')
                os.mkdir(number_folder_path)
        else:
            raise OSError("The path for creating the content type folders is not a folder")

    def create(self, path):
        if not os.path.isdir(path):
            raise OSError("The path for creating the catalog is not a folder")
        elif os.listdir(path):
            raise OSError("The folder for creating the catalog is not empty")
        else:
            self.create_folder_structure(path)
            self.create_database(path)
    
    def open(self, path):
        # TODO: Add check if path points to a descatter catalog
        self.path = path
        self.get_name_from_path()