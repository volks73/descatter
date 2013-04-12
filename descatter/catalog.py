import os
import sqlite3
import shutil
import constants

class Catalog(object):
    
    def __init__(self, path):
        if os.path.isdir(path):
            self.db = Database()
            self.path = path
            self.name = None
            
            while not self.name:
                self.name = os.path.basename(path)
                path = os.path.dirname(path)    
            
        else:
            raise OSError("The path for a catalog is not a folder")  
    
    def create_database(self):
        self.db.copy_default(self.path, self.name)
        
        # TODO: Add SQL table creation
    
    def create_folder_structure(self):        
        for folder_name in constants.CATALOG_FOLDER_NAMES:
            folder_path = os.path.join(self.path, folder_name)
            os.mkdir(folder_path)
    
            if folder_name == constants.CONTENT_FOLDER_NAME:
                self.create_content_type_folders(folder_path)
        
            if folder_name == constants.HOOKS_FOLDER_NAME:
                for sub_command_name in constants.HOOK_NAMES:     
                    sub_command_path = os.path.join(folder_path, sub_command_name)
                    os.mkdir(sub_command_path)
            
                    for trigger_name in constants.TRIGGER_NAMES: 
                        os.mkdir(os.path.join(sub_command_path, trigger_name))
                        
    def create_content_type_folders(self):
        for media_type_name in constants.MEDIA_TYPE_NAMES:
            media_type_path = os.path.join(self.path, media_type_name)
            os.mkdir(media_type_path)
            
        for media_subtype_name, media_type_name in constants.DEFAULT_CONTENT_TYPES.items():
            media_subtype_path = os.path.join(self.path, media_type_name)
            media_subtype_path = os.path.join(media_subtype_path, media_subtype_name)
            os.mkdir(media_subtype_path)
                
            number_folder_path = os.path.join(media_subtype_path, '1')
            os.mkdir(number_folder_path)

    def establish(self):        
        # TODO: Add check for empty folder
        # TODO: Add warning to user if folder is not empty

        self.create_folder_structure(self.path)
        self.create_database(self.path)
        
class Database(object):
    
    def __init__(self):
        self.connection = None
    
    def copy_default(self, path, catalog_name):
        data_path = os.path.join(os.getcwd(), constants.APPLICATION_NAME)
        data_path = os.path.join(data_path, constants.DATA_FOLDER_NAME)
        default_catalog_db_path = os.path.join(data_path, constants.DEFAULT_CATALOG_DB_NAME)
                
        db_file_name = catalog_name + constants.SQLITE_EXTENSION
        db_file_path = os.path.join(path, db_file_name)
        
        shutil.copyfile(default_catalog_db_path, db_file_path)
        
        # TODO: Add population of tables with default data