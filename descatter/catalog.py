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
    
def destroy(catalog, content=True):

    catalog.db.disconnect()

    if content:
        content_path = os.path.join(catalog.path, constants.CONTENT_FOLDER_NAME)
        shutil.rmtree(content_path)

    templates_path = os.path.join(catalog.path, constants.TEMPLATES_FOLDER_NAME)
    shutil.rmtree(templates_path)
        
    hooks_path = os.path.join(catalog.path, constants.HOOKS_FOLDER_NAME)
    shutil.rmtree(hooks_path)
        
    log_path = os.path.join(catalog.path, constants.LOG_FOLDER_NAME) 
    shutil.rmtree(log_path)
        
    db_path = os.path.join(catalog.path, constants.TAGS_DB_NAME)
    os.remove(db_path) 
        
    content_schema_path = os.path.join(catalog.path, constants.CONTENT_SCHEMA_FILE_NAME)
    os.remove(content_schema_path)
        
    readme_path = os.path.join(catalog.path, constants.CATALOG_README_FILE_NAME)
    os.remove(readme_path)
    
    try:
        os.rmdir(catalog.path)
    except IOError:
        pass

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
           
    def checkin(self, file_path, title=None):

        catalog_file = CatalogFile(file_path, title)
        destination = self.content_map.get_destination(catalog_file.get_extension())
        
        if destination:
            abs_content_folder_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
            dst_content_folder_path = os.path.join(abs_content_folder_path, destination)
            
            if not os.path.isdir(dst_content_folder_path):
                os.makedirs(dst_content_folder_path)
            
            abs_content_folder_path = tempfile.mkdtemp(suffix='', prefix='', dir=dst_content_folder_path)
            temp_folder_name = os.path.basename(abs_content_folder_path)
            content_folder_path = os.path.join(destination, temp_folder_name)
            
            # TODO: Add schema setting to use original file name, generic name, or random name
            content_file_name = catalog_file.get_original_name().replace(' ', '_')
            catalog_file.content_path = os.path.join(content_folder_path, content_file_name)
            
            dst_file_path = os.path.join(abs_content_folder_path, content_file_name) 
            
            shutil.copyfile(catalog_file.original_path, dst_file_path)
            
            # TODO: Update file checkin log. The checkin log will be a csv file with checkin date/time, original path, and content path located in the logs folder of the catalog.
            # TODO: Add metadata file creation
        else:
            raise KeyError("Mapping does not exist")
                        
        self.db.add_file(catalog_file)
        
        return catalog_file
    
    def get_file(self, content_path):
        
        return self.db.get_file_by_content_path(content_path)
    
    def remove_file(self, content_path):
        
        file = self.db.get_file_by_content_path(content_path)
        abs_content_folder_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
        abs_folder_path = os.path.join(abs_content_folder_path, file.get_content_path())
        
        shutil.rmtree(abs_folder_path)
        
        self.db.remove_file(file)
        
    def tag(self, catalog_file, tag):
        
        self.db.tag(catalog_file, tag)

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

class CatalogFile(object):
    
    def __init__(self, original_path, title=None, content_path=None, db_id=None):
        self.db_id = db_id
        self.original_path = original_path
        self.content_path = content_path
        
        if title is None:
            self.title = os.path.splitext(self.get_original_name())[0]
        else:
            self.title = title
    
    def get_content_path(self):
        
        if self.content_path is None:
            return self.content_path
        else:
            return os.path.dirname(self.content_path)
    
    def get_content_name(self):
        
        if self.content_path is None:
            return None
        else:
            return os.path.basename(self.content_path)
    
    def get_original_path(self):
        
        return os.path.dirname(self.original_path)
    
    def get_original_name(self):
        
        return os.path.basename(self.original_path)
    
    def get_extension(self):
        
        return os.path.splitext(self.original_path)[1][1:].strip().lower()
    
    def get_title(self):
        
        return self.title

class Tag(object):
    
    def __init__(self, name, db_id=None):
        self.name = name.lower()
        self.db_id = db_id
    
    def get_name(self):
        
        return self.name.title()
    
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
        
    def add_tag(self, tag):
        
        cursor = self.connection.cursor()
        
        values = { constants.NAME_COLUMN_NAME : tag.name }
        sql = ("insert into " + 
               constants.TAGS_TABLE_NAME + 
               "(" +
                constants.NAME_COLUMN_NAME + 
                ")  values (:" +
                constants.NAME_COLUMN_NAME +
                ")")
        
        cursor.execute(sql, values)
        self.connection.commit()
        
        tag.db_id = cursor.lastrowid
        
        cursor.close()
        
        return tag
    
    def add_file(self, catalog_file):
        
        cursor = self.connection.cursor()
        
        sql = ("insert into " + 
               constants.FILES_TABLE_NAME +
               "(" + 
               constants.CONTENT_PATH_COLUMN_NAME + 
               ", " + 
               constants.ORIGINAL_PATH_COLUMN_NAME + 
               ", " + 
               constants.TITLE_COLUMN_NAME + 
               ", " +
               constants.DATE_ADDED_COLUMN_NAME + 
               ") values (" + 
               ":" + 
               constants.CONTENT_PATH_COLUMN_NAME + 
               ", :" + 
               constants.ORIGINAL_PATH_COLUMN_NAME +  
               ", :" + 
               constants.TITLE_COLUMN_NAME + 
               ", datetime('now'))")
        
        db_catalog_file = {constants.CONTENT_PATH_COLUMN_NAME : catalog_file.content_path,
                           constants.ORIGINAL_PATH_COLUMN_NAME : catalog_file.original_path,
                           constants.TITLE_COLUMN_NAME : catalog_file.title}
        
        cursor.execute(sql, db_catalog_file)
        self.connection.commit()
        
        catalog_file.db_id = cursor.lastrowid
        
        cursor.close()
        
        return catalog_file
    
    def remove_tag(self, file_tag):
        
        cursor = self.connection.cursor()
        
        # TODO: Remove from all tables
        values = { constants.NAME_COLUMN_NAME : file_tag.name }
        sql = ("delete from " + 
               constants.TAGS_TABLE_NAME + 
               " where " + 
               constants.NAME_COLUMN_NAME + 
               " = :" + 
               constants.NAME_COLUMN_NAME)
        
        cursor.execute(sql, values)
        self.connection.commit()
        
        cursor.close()        
    
    def remove_file(self, catalog_file):
        
        cursor = self.connection.cursor()
        
        # TODO: Remove from all tables
        values = { constants.FILES_ID_COLUMN_NAME : catalog_file.db_id }
        sql = ("delete from " + 
               constants.FILES_TABLE_NAME +
               " where " + 
               constants.FILES_ID_COLUMN_NAME +
               " = :" +
               constants.FILES_ID_COLUMN_NAME)
    
        cursor.execute(sql, values)
                
        self.connection.commit()    
        
        cursor.close()
    
    def rename_tag(self, old_name, new_name):
        
        pass
    
    def tag(self, catalog_file, tag):
        
        db_tag = None
        if tag.db_id is None:
            db_tag = self.get_tag_by_name(tag.name)
        
            if db_tag is None:
                db_tag = self.add_tag(tag)
        
        db_catalog_file = None
        if catalog_file.db_id is None:    
            db_catalog_file = self.get_file_by_content_path(catalog_file.get_content_path())
        else:
            db_catalog_file = catalog_file
        
        if not self.is_file_tagged(db_catalog_file, db_tag):
            cursor = self.connection.cursor()
            
            values = {constants.FILES_ID_COLUMN_NAME : db_catalog_file.db_id,
                      constants.TAGS_ID_COLUMN_NAME : db_tag.db_id}
            sql = ("insert into " +
                   constants.FILES_TAGS_TABLE_NAME +
                   "(" +
                   constants.FILES_ID_COLUMN_NAME +
                   ", " +
                   constants.TAGS_ID_COLUMN_NAME +
                   ") values (" +
                   ":" +
                   constants.FILES_ID_COLUMN_NAME +
                   ", :" + 
                   constants.TAGS_ID_COLUMN_NAME +
                   ")")
            
            cursor.execute(sql, values)
            
            self.connection.commit()
            
            cursor.close()
    
    def detag(self, catalog_file, tag):
        
        # TODO: Add detag ability
        pass
    
    def get_all_tags(self):
        
        cursor = self.connection.cursor()
        
        sql = ("select " +
               constants.TAGS_ID_COLUMN_NAME +
               ", " +
               constants.NAME_COLUMN_NAME +
               " from " + 
               constants.TAGS_TABLE_NAME + 
               " order by " + 
               constants.NAME_COLUMN_NAME)
        
        cursor.execute(sql)
        tags = []
        for row in cursor:
            tag = Tag(row[constants.NAME_COLUMN_NAME],
                               row[constants.TAGS_ID_COLUMN_NAME])
            tags.append(tag)
            
        cursor.close()
        
        return tags
    
    def get_all_files(self):
        
        cursor = self.connection.cursor()
        
        sql = ("select " +
               constants.FILES_ID_COLUMN_NAME +
               ", " +
               constants.TITLE_COLUMN_NAME + 
               ", " +
               constants.CONTENT_PATH_COLUMN_NAME + 
               ", " +
               constants.ORIGINAL_PATH_COLUMN_NAME +
               " from " + 
               constants.FILES_TABLE_NAME +
               " order by " + 
               constants.TITLE_COLUMN_NAME)
        
        cursor.execute(sql)
        files = []
        for row in cursor:
            catalog_file = CatalogFile(row[constants.ORIGINAL_PATH_COLUMN_NAME],                                
                                       row[constants.TITLE_COLUMN_NAME],
                                       row[constants.CONTENT_PATH_COLUMN_NAME],
                                       row[constants.FILES_ID_COLUMN_NAME])
            files.append(catalog_file)
            
        cursor.close()
        
        return files
    
    def get_tag_by_name(self, tag_name):
        
        cursor = self.connection.cursor()
        
        values = {constants.NAME_COLUMN_NAME : tag_name}
        sql = ("select " +
               constants.TAGS_ID_COLUMN_NAME +
               ", " +
               constants.NAME_COLUMN_NAME +
               " from " +
               constants.TAGS_TABLE_NAME +
               " where " +
               constants.NAME_COLUMN_NAME +
               " = :" +
               constants.NAME_COLUMN_NAME)
        
        cursor.execute(sql, values)
        row = cursor.fetchone()
        tag = None
        
        if row is not None:
            tag = Tag(row[constants.NAME_COLUMN_NAME],
                      row[constants.TAGS_ID_COLUMN_NAME])
        
        cursor.close()
        
        return tag
    
    def get_file_by_content_path(self, content_path):
        
        cursor = self.connection.cursor()
        
        values = (content_path + '%', )
        sql = ("select " +
               constants.FILES_ID_COLUMN_NAME +
               ", " +
               constants.TITLE_COLUMN_NAME + 
               ", " +
               constants.CONTENT_PATH_COLUMN_NAME + 
               ", " +
               constants.ORIGINAL_PATH_COLUMN_NAME +
               " from " + 
               constants.FILES_TABLE_NAME +
               " where " + 
               constants.CONTENT_PATH_COLUMN_NAME +
               " like ?")
        
        cursor.execute(sql, values)
        row = cursor.fetchone()
        catalog_file = None
        
        if row is not None:
            catalog_file = CatalogFile(row[constants.ORIGINAL_PATH_COLUMN_NAME],                                       
                                       row[constants.TITLE_COLUMN_NAME],
                                       row[constants.CONTENT_PATH_COLUMN_NAME],
                                       row[constants.FILES_ID_COLUMN_NAME])
        
        cursor.close()
        
        return catalog_file
    
    def is_file_tagged(self, catalog_file, tag):
        
        cursor = self.connection.cursor()
        
        values = {constants.FILES_ID_COLUMN_NAME : catalog_file.db_id,
                  constants.TAGS_ID_COLUMN_NAME : tag.db_id}
        sql = ("select " +
               constants.FILES_TAGS_ID_COLUMN_NAME +
               " from " +
               constants.FILES_TAGS_TABLE_NAME +
               " where " +
               constants.FILES_ID_COLUMN_NAME +
               " = :" +
               constants.FILES_ID_COLUMN_NAME +
               " and " +
               constants.TAGS_ID_COLUMN_NAME + 
               " = :" +
               constants.TAGS_ID_COLUMN_NAME +
               " limit 1")
        
        cursor.execute(sql, values)
        row = cursor.fetchone()
        
        return row is not None