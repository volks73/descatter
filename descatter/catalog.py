import os
import sqlite3
import shutil
import constants

class Catalog(object):
    
    def __init__(self, path):
        self.db = Database()
        self.path = path
        self.name = None
            
        while not self.name:
            self.name = os.path.basename(path)
            path = os.path.dirname(path)      
    
    def create_database(self):
        self.db.copy_default(self.path, self.name)
        
        # TODO: Add SQL table creation
    
    def create_folder_structure(self):        
        for folder_name in constants.CATALOG_FOLDER_NAMES:
            folder_path = os.path.join(self.path, folder_name)
            os.mkdir(folder_path)
            
        self.create_content_type_folders()
        self.create_hook_folders()
                        
    def create_content_type_folders(self):
        content_folder_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
        
        for media_type_name in constants.MEDIA_TYPE_NAMES:
            media_type_path = os.path.join(content_folder_path, media_type_name)
            os.mkdir(media_type_path)
            
        for media_subtype_name, media_type_name in constants.DEFAULT_CONTENT_TYPES.items():
            # TODO: Add folder creation for vnd subtypes
            # TODO: Add folder creation for prs subtypes
            # TODO: Replace '.' in subtypes with underscores
            # TODO: Add santization of subtypes with special characters, i.e. '+'
            media_subtype_path = os.path.join(content_folder_path, media_type_name)
            media_subtype_path = os.path.join(media_subtype_path, media_subtype_name)
            os.mkdir(media_subtype_path)
                
            number_folder_path = os.path.join(media_subtype_path, '1')
            os.mkdir(number_folder_path)

    def create_hook_folders(self):
        hooks_folder_path = os.path.join(self.path, constants.HOOKS_FOLDER_NAME)
        
        for hook_folder_name in constants.HOOK_NAMES:
            hook_path = os.path.join(hooks_folder_path, hook_folder_name)
            os.mkdir(hook_path)
            
            for trigger_name in constants.TRIGGER_NAMES:
                trigger_path = os.path.join(hook_path, trigger_name)
                os.mkdir(trigger_path)

    def establish(self):
        self.create_folder_structure()
        self.create_database()
        
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

class File(object):
    
    def __init__(self):
        pass