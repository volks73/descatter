import os
import sqlite3
import xml.etree.ElementTree as ET
import shutil
import constants

class Catalog(object):
    
    def __init__(self, path):
        self.db = Database()
        self.path = path
        self.name = None
        self.file_associations = {}
            
        while not self.name:
            self.name = os.path.basename(path)
            path = os.path.dirname(path)      
    
    def create_database(self):
        self.db.create(self.path, self.name)
             
    def create_folder_structure(self):        
        for folder_name in constants.CATALOG_FOLDER_NAMES:
            folder_path = os.path.join(self.path, folder_name)
            os.mkdir(folder_path)
            
        self.create_hook_folders()

    def create_hook_folders(self):
        hooks_folder_path = os.path.join(self.path, constants.HOOKS_FOLDER_NAME)
        
        for hook_folder_name in constants.HOOK_NAMES:
            hook_path = os.path.join(hooks_folder_path, hook_folder_name)
            os.mkdir(hook_path)
            
            for trigger_name in constants.TRIGGER_NAMES:
                trigger_path = os.path.join(hook_path, trigger_name)
                os.mkdir(trigger_path)

    def create(self, schema_path=None):
        self.create_folder_structure()
        self.create_database()
        
        if schema_path:
            self.create_file_associations(schema_path)
            # TODO: Add associations to catalog database
    
    def create_file_associations(self, schema_path):
        tree = ET.parse(schema_path)
        root = tree.getroot()
            
        self.create_destination_path(root)
    
    def create_destination_path(self, parent, file_destination=''):
        for child in parent:
            if child.tag == constants.FOLDER_TAG_NAME:
                self.create_destination_path(child, file_destination + os.pathsep + child.get(constants.NAME_ATTRIBUTE_NAME))
        
        if parent.tag == constants.FOLDER_TAG_NAME:
            for extension in parent.findall(constants.EXTENSIONS_TAG_NAME + '/' + constants.EXTENSION_TAG_NAME):
                self.file_associations[extension.get(constants.ID_ATTRIBUTE_NAME)] = (file_destination, extension.text)
    
    def destroy(self):
        content_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
        templates_path = os.path.join(self.path, constants.TEMPLATES_FOLDER_NAME)
        hooks_path = os.path.join(self.path, constants.HOOKS_FOLDER_NAME)
        log_path = os.path.join(self.path, constants.LOG_FOLDER_NAME)
        
        shutil.rmtree(content_path)
        shutil.rmtree(templates_path)
        shutil.rmtree(hooks_path)     
        shutil.rmtree(log_path)
        
        self.db.destroy()
                        
class Database(object):
    
    def __init__(self):
        self.path = None
        self.name = None
        self.connection = None
    
    def copy_default(self, path, catalog_name):
        data_path = os.path.join(os.getcwd(), constants.APPLICATION_NAME)
        data_path = os.path.join(data_path, constants.DATA_FOLDER_NAME)
        default_catalog_db_path = os.path.join(data_path, constants.DEFAULT_CATALOG_DB_NAME)
        
        self.name = catalog_name        
        db_file_name = self.name + constants.SQLITE_EXTENSION
        self.path = os.path.join(path, db_file_name)
        
        shutil.copyfile(default_catalog_db_path, self.path)
    
    def destroy(self):
        self.connection.close()
        os.remove(self.path)
        
    def create(self, path, catalog_name):
        self.copy_default(path, catalog_name)
        self.connection = sqlite3.connect(self.path)
        
#         insert_tuple = (constants.FILE_EXTENSIONS_TABLE_NAME, 
#                         constants.EXTENSION_COLUMN_NAME, 
#                         constants.DESCRIPTION_COLUMN_NAME)
#         
#         sql = "INSERT INTO %s ('%s', '%s') VALUES (?, ?)" % insert_tuple
#         
#         self.connection.executemany(sql, constants.DEFAULT_FILE_EXTENSIONS)
#         self.connection.commit()
#         
#         insert_tuple = (constants.CONTENT_TYPES_TABLE_NAME, 
#                         constants.MEDIA_TYPE_NAME_COLUMN_NAME, 
#                         constants.MEDIA_SUBTYPE_NAME_COLUMN_NAME)
#         
#         sql = "INSERT INTO %s ('%s', '%s') VALUES (?, ?)" % insert_tuple
#         
#         self.connection.commit()
        
        # TODO: Add population of default file associations