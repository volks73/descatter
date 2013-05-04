from lxml import etree

import os
import shutil
import constants

def create_folder_structure(catalog_path):        
    """ Creates the catalog folder structure. """
    
    for folder_name in constants.CATALOG_FOLDER_NAMES:
        folder_path = os.path.join(catalog_path, folder_name)
        os.mkdir(folder_path)
            
    create_hook_folders(catalog_path)

def create_hook_folders(catalog_path):
    """ Creates the hook folder sub-structure. """    
        
    hooks_folder_path = os.path.join(catalog_path, constants.HOOKS_FOLDER_NAME)
        
    for hook_folder_name in constants.HOOK_NAMES:
        hook_path = os.path.join(hooks_folder_path, hook_folder_name)
        os.mkdir(hook_path)
            
        for trigger_name in constants.TRIGGER_NAMES:
            trigger_path = os.path.join(hook_path, trigger_name)
            os.mkdir(trigger_path)

def establish(catalog_path, schema_path=None):
    """ Establishes, or creates, a catalog at the specified path. The schema is optional. """

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
    """ Destroys, removes, or deletes a catalog at the specified path. All files and sub-folders will also be destroyed. """

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
    """ Checks if the path is to catalog by looking for the appropriate files and folder structure. """
    
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
        """ Initializes the catalog. """
        
        self.db = TagsDatabase(path)
        self.content_map = ContentMap(path)
        
        self.path = path
        self.name = None
                    
        while not self.name:
            self.name = os.path.basename(path)
            path = os.path.dirname(path)
        
    def checkin(self, file_path):
        """ Checks in a file. """

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
        
        return destination

class ContentMap(object):
    
    def __init__(self, catalog_path):
        """ Initializes the content map. 
        
            Keyword arguments:
                catalog_path -- The absolute path to the catalog
            
        """     
                
        self.schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
        self.map = {}
        self.load()
    
    def _load(self, parent, file_destination=None):
        """ Recursive call to load the map from the schema file. 
        
            Keyword arguments:
                parent -- The parent XML element
                file_destination -- The relative path to the content folder for a file. Optional
            
        """
        
        for child in parent:
            if child.tag == constants.FOLDER_TAG_NAME:
                child_destination = os.path.join(file_destination, child.get(constants.NAME_ATTRIBUTE_NAME))
                self._load(child, child_destination)
        
        if parent.tag == constants.FOLDER_TAG_NAME:
            for extension in parent.findall(constants.EXTENSIONS_TAG_NAME + '/' + constants.EXTENSION_TAG_NAME):
                self.map[extension.get(constants.ID_ATTRIBUTE_NAME)] = file_destination
        
    def write_schema(self, schema_path=None):
        """ Write the map to the schema file. 
        
            Keyword arguments:
                schema_path -- The file path to write the schema. Optional
            
        """        
                
        root = self.create_schema()
        tree = etree.ElementTree(root)
        
        if schema_path is None:
            schema_path = self.schema_path
        
        tree.write(schema_path, pretty_print=True, xml_declaration=True, encoding=constants.XML_ENCODING)
    
    def create_schema(self):
        """ Creates an XML document of the schema. 
        
            Return:
                The root element of the XML document
        """
        
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
        """ Loads the file extension maps from the schema file. """
                
        self.map = {}
        
        tree = etree.parse(self.schema_path)
        
        self._load(tree.getroot())
                            
    def add(self, file_extension, destination):
        """ Adds a file extension map to the mappings. 
        
            Keyword arguments:
                file_extension -- The file extension without a leading period
                destination -- The relative path to the content parent folder of a catalog for files with the given file_extension
        
        """       
               
        self.map[file_extension] = destination
        
        self.write_schema()
    
    def remove(self, file_extension):
        """ Removes a file extension from the mappings. 
        
            Keyword arguments:
                file_extension -- The file extension without a leading period
            
        """
        
        if file_extension in self.map:    
            self.map.pop(file_extension, None)
        else:
            raise KeyError("File extension not recognized")
        
        self.write_schema()
    
    def get_destination(self, file_extension):
        """ Gets the sub-folder relative to the content folder where files with the specified extension will be located. 
        
            Keyword arguments:
                file_extension -- The file extension without a leading period
            
        """ 
              
        if file_extension in self.map:
            return self.map[file_extension]
        else:
            return None
                        
class TagsDatabase(object):
    
    def __init__(self, catalog_path):
        
        self.path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
        self.name = None
        self.connection = None