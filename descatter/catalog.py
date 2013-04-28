from lxml import etree

import os
import shutil
import constants

class Catalog(object):
    
    def __init__(self, path):
        
        self.db = TagsDatabase(path)
        self.path = path
        self.name = None
        
        self.content_map = ContentMap(path)
                    
        while not self.name:
            self.name = os.path.basename(path)
            path = os.path.dirname(path)
                               
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
        self.db.create()
        
        if schema_path is None:
            self.content_map.write_schema()            
        else:
            # TODO: check schema path exists prior to creating structure
            shutil.copyfile(schema_path, self.content_map.schema_path)
        
        data_path = os.path.join(os.getcwd(), constants.APPLICATION_NAME)
        data_path = os.path.join(data_path, constants.DATA_FOLDER_NAME)
        src_readme_file_path = os.path.join(data_path, constants.DEFAULT_README_FILE_NAME)
        dst_readme_file_path = os.path.join(self.path, constants.CATALOG_README_FILE_NAME)
        
        shutil.copyfile(src_readme_file_path, dst_readme_file_path)
    
    def destroy(self):

        content_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
        templates_path = os.path.join(self.path, constants.TEMPLATES_FOLDER_NAME)
        hooks_path = os.path.join(self.path, constants.HOOKS_FOLDER_NAME)
        log_path = os.path.join(self.path, constants.LOG_FOLDER_NAME)
        readme_path = os.path.join(self.path, constants.CATALOG_README_FILE_NAME)
        
        shutil.rmtree(content_path)
        shutil.rmtree(templates_path)
        shutil.rmtree(hooks_path)     
        shutil.rmtree(log_path)
        
        os.remove(readme_path)
        
        self.content_map.destroy()
        self.db.destroy()
        
    def checkin(self, file_path):

        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_path)[1][1:].strip().lower()
        destination = self.content_map.get_destination(file_extension)
        
        if destination:
            content_folder_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME)
            dst_folder_path = os.path.join(content_folder_path, destination)
            
            if not os.path.isdir(dst_folder_path):
                os.makedirs(dst_folder_path)
        
            # TODO: Use tmp file module to create unique file name instead of using original name
            dst_file_path = os.path.join(dst_folder_path, file_name)
            
            shutil.copyfile(file_path, dst_file_path)    
        else:
            raise KeyError("Mapping does not exist")

class ContentMap(object):
    
    def __init__(self, catalog_path):
                
        self.schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
        self.map = None
    
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
        
        if self.map is not None:
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
        
        if self.map is None:
            self.load()
        
        self.map[file_extension] = destination
        
        self.write_schema()
    
    def remove(self, file_extension):
        
        if self.map is None:
            self.load()
        
        if file_extension in self.map:    
            self.map.pop(file_extension, None)
        else:
            print("File extension not mapped. Nothing to remove.")
        
        self.write_schema()
    
    def get_destination(self, file_extension):
        
        if self.map is None:
            self.load()
        
        if file_extension in self.map:
            return self.map[file_extension]
        else:
            return None    
    
    def destroy(self):
        
        self.map = {}
        os.remove(self.schema_path)
                        
class TagsDatabase(object):
    
    def __init__(self, catalog_path):
        
        self.path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
        self.name = None
        self.connection = None
    
    def copy_default(self, dst_path=None):
        
        if dst_path is None:
            dst_path = self.path
        
        data_path = os.path.join(os.getcwd(), constants.APPLICATION_NAME)
        data_path = os.path.join(data_path, constants.DATA_FOLDER_NAME)
        default_catalog_db_path = os.path.join(data_path, constants.DEFAULT_TAGS_DB_NAME)
        
        shutil.copyfile(default_catalog_db_path, dst_path)
    
    def destroy(self):
        
        if self.connection is not None:
            self.connection.close()
        
        os.remove(self.path)
        
    def create(self, dst_path=None):
        
        if dst_path is None:
            dst_path = self.path
        
        self.copy_default(dst_path)