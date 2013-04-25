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
                    
        while not self.name:
            self.name = os.path.basename(path)
            path = os.path.dirname(path)
            
        self.content_schema_path = os.path.join(self.path, constants.CONTENT_SCHEMA_FILE_NAME)
                  
    def create_database(self):
        
        self.db.create(self.path, self.name)
             
    def create_folder_structure(self):        
        
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        
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
            shutil.copyfile(schema_path, self.content_schema_path)
        else:
            root = ET.Element(constants.CONTENT_FOLDER_TAG_NAME, 
                              {constants.XMLNS_ATTRIBUTE_NAME : constants.CONTENT_SCHEMA_NAMESPACE})
            tree = ET.ElementTree(root)
            tree.write(self.content_schema_path, encoding="UTF-8", xml_declaration=True)
        
        # TODO: Add copy of README file to root folder explaining the folder is catalog and should not be messed with
    
    def load_file_associations(self):
        
        tree = ET.parse(self.content_schema_path)
        root = tree.getroot()
            
        return self.get_file_associations(root)
    
    def get_file_associations(self, parent, file_destination=None):
        
        file_associations = {}
        
        for child in parent:
            if child.tag == constants.FOLDER_TAG_NAME:
                child_destination = os.path.join(file_destination, child.get(constants.NAME_ATTRIBUTE_NAME))

                file_associations.update(self.get_file_associations(child, child_destination))
        
        if parent.tag == constants.FOLDER_TAG_NAME:
            for extension in parent.findall(constants.EXTENSIONS_TAG_NAME + '/' + constants.EXTENSION_TAG_NAME):
                file_associations[extension.get(constants.ID_ATTRIBUTE_NAME)] = file_destination
        
        return file_associations
    
    def destroy(self):

        content_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
        templates_path = os.path.join(self.path, constants.TEMPLATES_FOLDER_NAME)
        hooks_path = os.path.join(self.path, constants.HOOKS_FOLDER_NAME)
        log_path = os.path.join(self.path, constants.LOG_FOLDER_NAME)
        
        shutil.rmtree(content_path)
        shutil.rmtree(templates_path)
        shutil.rmtree(hooks_path)     
        shutil.rmtree(log_path)
        
        os.remove(self.content_schema_path)
        
        self.db.destroy()
        
    def checkin(self, file_path):

        file_associations = self.load_file_associations()
        file_extension = os.path.splitext(file_path)[1][1:].strip().lower()
        destination_path = file_associations[file_extension]
        
        # TODO: Add destination path creation if does not exist
        # TODO: Move file to destination path
                        
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