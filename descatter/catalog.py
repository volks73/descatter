from lxml import etree

import os
import sqlite3
import tempfile
import shutil
import constants

def create_folder_structure(catalog_path):        
    
    for folder_name in constants.CATALOG_FOLDER_NAMES:
        folder_path = os.path.join(catalog_path, folder_name)
        os.mkdir(folder_path)
            
    create_hook_folders(catalog_path)

def create_hook_folders(catalog_path):    
        
    hooks_folder_path = os.path.join(catalog_path, constants.HOOKS_FOLDER_NAME)
        
    for hook_folder_name in constants.HOOK_NAMES:
        hook_path = os.path.join(hooks_folder_path, hook_folder_name)
        os.mkdir(hook_path)
            
        for trigger_name in constants.TRIGGER_NAMES:
            trigger_path = os.path.join(hook_path, trigger_name)
            os.mkdir(trigger_path)

def establish(catalog_path, schema_path=None):

    if not os.path.isdir(catalog_path):
        os.mkdir(catalog_path)

    data_path = os.path.join(os.getcwd(), constants.APPLICATION_NAME)
    data_path = os.path.join(data_path, constants.DATA_FOLDER_NAME)

    src_readme_file_path = os.path.join(data_path, constants.DEFAULT_README_FILE_NAME)
    dst_readme_file_path = os.path.join(catalog_path, constants.CATALOG_README_FILE_NAME)
    shutil.copyfile(src_readme_file_path, dst_readme_file_path)

    dst_db_path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
    src_db_path = os.path.join(data_path, constants.DEFAULT_TAGS_DB_NAME)
    shutil.copyfile(src_db_path, dst_db_path)
    
    dst_content_schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
    
    if schema_path is None:
        schema_path = os.path.join(data_path, constants.DEFAULT_CONTENT_SCHEMA_FILE_NAME)
    
    src_content_schema_path = schema_path
    shutil.copyfile(src_content_schema_path, dst_content_schema_path)
    
    create_folder_structure(catalog_path)
    
    return Catalog(catalog_path)
    
def destroy(catalog_path, content=True):

    if content:
        content_path = os.path.join(catalog_path, constants.CONTENT_FOLDER_NAME)
        shutil.rmtree(content_path)
    
    templates_path = os.path.join(catalog_path, constants.TEMPLATES_FOLDER_NAME)
    shutil.rmtree(templates_path)
    
    hooks_path = os.path.join(catalog_path, constants.HOOKS_FOLDER_NAME)
    shutil.rmtree(hooks_path)
    
    log_path = os.path.join(catalog_path, constants.LOG_FOLDER_NAME) 
    shutil.rmtree(log_path)
    
    db_path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
    os.remove(db_path) 
    
    content_schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
    os.remove(content_schema_path)
    
    readme_path = os.path.join(catalog_path, constants.CATALOG_README_FILE_NAME)
    os.remove(readme_path)

def is_catalog(catalog_path):
    
    if catalog_path is None:
        return False
    else: 
        folder_structure_exists = True
        for folder_name in constants.CATALOG_FOLDER_NAMES:
            folder_path = os.path.join(catalog_path, folder_name)
            
            folder_structure_exists = folder_structure_exists and os.path.isdir(folder_path)
        
        content_schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
        content_schema_file_exists = os.path.isfile(content_schema_path)
        
        tags_db_path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
        # TODO: Add check if tags db has the appropriate schema and tables
        tags_db_exists = os.path.isfile(tags_db_path)
        
        return folder_structure_exists and content_schema_file_exists and tags_db_exists

class Catalog(object):
    
    def __init__(self, path):
        
        self.db = TagsDatabase(path)
        self.content_map = ContentMap(path)
        
        self.path = path
        self.name = None
                    
        while not self.name:
            self.name = os.path.basename(path)
            path = os.path.dirname(path)
           
    def checkin(self, file_path):

        original_file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_path)[1][1:].strip().lower()
        destination = self.content_map.get_destination(file_extension)
        
        # TODO: refactor code to clean up folder creation and path determination
        if destination:
            abs_content_folder_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
            dst_content_folder_path = os.path.join(abs_content_folder_path, destination)
            
            if not os.path.isdir(dst_content_folder_path):
                os.makedirs(dst_content_folder_path)
            
            # Create a folder with a unique name in a safe manner
            abs_content_folder_path = tempfile.mkdtemp(suffix='', prefix='', dir=dst_content_folder_path)
            temp_folder_name = os.path.basename(abs_content_folder_path)
            content_folder_path = os.path.join(destination, temp_folder_name)
            
            # TODO: Add schema setting to use original file name, generic name, or random name
#             catalog_file_name = constants.CONTENT_FILE_NAME + '.' + file_extension
            # TODO: Replace spaces in file name with underscores
            content_file_name = original_file_name
            
            dst_file_path = os.path.join(abs_content_folder_path, content_file_name) 
            
            shutil.copyfile(file_path, dst_file_path)
            
            # TODO: Add metadata file creation
        else:
            raise KeyError("Mapping does not exist")
        
        # TODO: Allow user to specify a title for the file
        title = os.path.splitext(original_file_name)[0].strip().lower()
        
        catalog_file = {constants.ORIGINAL_FILE_NAME_COLUMN_NAME : original_file_name,
                        constants.CONTENT_FILE_NAME_COLUMN_NAME : content_file_name,
                        constants.CONTENT_PATH_COLUMN_NAME : content_folder_path,
                        constants.TITLE_COLUMN_NAME : title}
                        
        self.db.add_file(catalog_file)
        
        return destination

class ContentMap(object):
    
    def __init__(self, catalog_path):   
                
        self.schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
        self.map = {}
        self.load()
    
    def _load(self, parent, file_destination=None):
                
        for child in parent:
            if child.tag == constants.FOLDER_TAG_NAME:
                child_destination = os.path.join(file_destination, child.get(constants.NAME_ATTRIBUTE_NAME))
                self._load(child, child_destination)
        
        if parent.tag == constants.FOLDER_TAG_NAME:
            for extension in parent.findall(constants.EXTENSIONS_TAG_NAME + '/' + constants.EXTENSION_TAG_NAME):
                self.map[extension.get(constants.ID_ATTRIBUTE_NAME)] = file_destination
        
    def write_schema(self, schema_path=None):      
                
        root = self.create_schema()
        tree = etree.ElementTree(root)
        
        if schema_path is None:
            schema_path = self.schema_path
        
        tree.write(schema_path, pretty_print=True, xml_declaration=True, encoding=constants.XML_ENCODING)
    
    def create_schema(self):
                
        root = etree.Element(constants.CONTENT_FOLDER_TAG_NAME, nsmap=constants.NAMESPACE_MAP)
        
        for file_extension, destination in self.map.items():      
            parent = root
            folder_names = []
            head, tail = os.path.split(destination)
            folder_names.append(tail)
                
            while head:
                head, tail = os.path.split(head)
                if tail:
                    folder_names.append(tail)
                
            for folder_name in reversed(folder_names):
                xpath = constants.FOLDER_TAG_NAME + "[@" + constants.NAME_ATTRIBUTE_NAME + "='%s']" % folder_name
                folder_element = parent.find(xpath)         
            
                if folder_element is None:
                    folder_element = etree.SubElement(parent,
                                                      constants.FOLDER_TAG_NAME,
                                                      {constants.NAME_ATTRIBUTE_NAME : folder_name})
                    
                parent = folder_element
            
            extensions_element = parent.find(constants.EXTENSIONS_TAG_NAME)
                
            if extensions_element is None:
                extensions_element = etree.SubElement(parent, constants.EXTENSIONS_TAG_NAME)
            
            etree.SubElement(extensions_element, 
                             constants.EXTENSION_TAG_NAME,
                             {constants.ID_ATTRIBUTE_NAME : file_extension})
        
        return root
        
    def load(self):
                        
        self.map = {}
        
        tree = etree.parse(self.schema_path)
        
        self._load(tree.getroot())
                            
    def add(self, file_extension, destination):    
               
        self.map[file_extension] = destination
        
        self.write_schema()
    
    def remove(self, file_extension):
                
        if file_extension in self.map:    
            self.map.pop(file_extension, None)
        else:
            raise KeyError("File extension not recognized")
        
        self.write_schema()
    
    def get_destination(self, file_extension):
                      
        if file_extension in self.map:
            return self.map[file_extension]
        else:
            return None
                        
class TagsDatabase(object):
    
    def __init__(self, catalog_path):
        
        self.path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
        self.name = None
        self.connect()
    
    def connect(self):
        
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
    
    def disconnect(self):
        
        self.connection.close()
        
    def add_tag(self, name):
        
        cursor = self.connection.cursor()
        
        values = { constants.NAME_COLUMN_NAME : name }
        sql = ("insert into " + constants.TAGS_TABLE_NAME + 
               "(" +
                constants.NAME_COLUMN_NAME + 
                ")  values (" +
                ":" + constants.NAME_COLUMN_NAME +
                ")")
        
        cursor.execute(sql, values)
        self.connection.commit()
        
        cursor.close()
    
    def add_file(self, catalog_file):
        
        cursor = self.connection.cursor()
        
        sql = ("insert into " + constants.FILES_TABLE_NAME +
               "(" + 
               constants.CONTENT_PATH_COLUMN_NAME + ", " + 
               constants.CONTENT_FILE_NAME_COLUMN_NAME + ", " + 
               constants.ORIGINAL_FILE_NAME_COLUMN_NAME + ", " + 
               constants.TITLE_COLUMN_NAME + 
               ") values (" + 
               ":" + constants.CONTENT_PATH_COLUMN_NAME + 
               ", :" + constants.CONTENT_FILE_NAME_COLUMN_NAME + 
               ", :" + constants.ORIGINAL_FILE_NAME_COLUMN_NAME + 
               ", :" + constants.TITLE_COLUMN_NAME + 
               ")")
        
        cursor.execute(sql, catalog_file)
        self.connection.commit()
        
        cursor.close()
    
    def remove_tag(self, name):
        
        cursor = self.connection.cursor()
        
        values = { constants.NAME_COLUMN_NAME : name }
        sql = ("delete from " + 
               constants.TAGS_TABLE_NAME + 
               " where " + 
               constants.NAME_COLUMN_NAME + " = :" + constants.NAME_COLUMN_NAME)
        
        cursor.execute(sql, values)
        self.connection.commit()
        
        cursor.close()        
    
    def rename_tag(self, old_name, new_name):
        
        pass
    
    def tag(self, file, name):
        
        pass
    
    def get_all_tags(self):
        
        cursor = self.connection.cursor()
        
        sql = ("select * from " + constants.TAGS_TABLE_NAME + 
               " order by " + constants.NAME_COLUMN_NAME)
        
        cursor.execute(sql)
        tags = []
        for row in cursor:
            tags.append(row[constants.NAME_COLUMN_NAME])
            
        cursor.close()
        
        return tags
    
    def get_all_files(self):
        
        cursor = self.connection.cursor()
        
        sql = ("select " +
               constants.TITLE_COLUMN_NAME + ", " +
               constants.CONTENT_PATH_COLUMN_NAME + ", " +
               constants.CONTENT_FILE_NAME_COLUMN_NAME + ", " +
               constants.ORIGINAL_FILE_NAME_COLUMN_NAME +
               " from " + constants.FILES_TABLE_NAME +
               " order by " + constants.TITLE_COLUMN_NAME)
        
        cursor.execute(sql)
        files = []
        for row in cursor:
            files.append(row)
            
        cursor.close()
        
        return files
        