from lxml import etree
from datetime import datetime

import os
import tempfile
import shutil

import constants
import database

class CatalogError(Exception): pass

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

def create(catalog_path, schema_path=None):

    if os.path.exists(catalog_path):
        if os.path.isdir(catalog_path):
            if os.listdir(catalog_path):
                raise CatalogError("Folder must be empty to establish catalog")
        else:
            raise CatalogError("Catalog path is not a folder")
    else:
        os.mkdir(catalog_path)

    data_path = os.path.join(os.getcwd(), constants.APPLICATION_NAME)
    data_path = os.path.join(data_path, constants.DATA_FOLDER_NAME)

    src_readme_file_path = os.path.join(data_path, constants.DEFAULT_README_FILE_NAME)
    dst_readme_file_path = os.path.join(catalog_path, constants.CATALOG_README_FILE_NAME)
    shutil.copyfile(src_readme_file_path, dst_readme_file_path)
       
    if schema_path is None:
        schema_path = os.path.join(data_path, constants.DEFAULT_CONTENT_SCHEMA_FILE_NAME)
    
    src_content_schema_path = schema_path
    dst_content_schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
    shutil.copyfile(src_content_schema_path, dst_content_schema_path)
    
    create_folder_structure(catalog_path)
    
    return Catalog(catalog_path)

def destroy(catalog_path, remove_content=True):

    destroy_catalog = Catalog(catalog_path)
    destroy_catalog.session.close_all()
    destroy_catalog.session.bind.dispose()

    if remove_content:
        shutil.rmtree(catalog_path)
    else:
        templates_path = os.path.join(catalog_path, constants.TEMPLATES_FOLDER_NAME)
        shutil.rmtree(templates_path)
        
        hooks_path = os.path.join(catalog_path, constants.HOOKS_FOLDER_NAME)
        shutil.rmtree(hooks_path)
        
        log_path = os.path.join(catalog_path, constants.LOG_FOLDER_NAME) 
        shutil.rmtree(log_path) 
        
        content_schema_path = os.path.join(catalog_path, constants.CONTENT_SCHEMA_FILE_NAME)
        os.remove(content_schema_path)
        
        readme_path = os.path.join(catalog_path, constants.CATALOG_README_FILE_NAME)
        os.remove(readme_path)
     
        db_path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
        os.remove(db_path)
            
        os.rmdir(catalog_path)    

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

def create_checkin_file(os_file_path, title=None):
    
    file_name, file_extension = os.path.splitext(os_file_path)
    file_name = os.path.basename(file_name)
    file_extension = file_extension[1:].strip().lower() 
    
    return {'file-path': os.path.dirname(os_file_path),
            'file-name': file_name,
            'file-extension': file_extension,
            'file-size': os.path.getsize(os_file_path),
            'file-date-created': os.path.getctime(os_file_path),
            'file-date-modified': os.path.getmtime(os_file_path),
            'file-date-accessed': os.path.getatime(os_file_path),
            'file-date-added': datetime.now(),
            'file-title': title,
            'file-index': 1,
            'file-count': 1}
    
class Catalog(object):
    
    def __init__(self, path):
        
        self.path = os.path.abspath(path)
        self.content_map = ContentMap(self.path)
        self.name = os.path.basename(self.path)
        self.content_path = os.path.join(self.path, constants.CONTENT_FOLDER_NAME) # <path to catalog>/content/
        self.session = database.connect(self.path)
           
    def checkin(self, file_path, title=None):
        
        # TODO: Change file_path to a tuple of file_paths for batch checkin
        # TODO: Add unit-of-work style checkin error check and rollback
        file_path = os.path.abspath(file_path)
        
        if title is None:
            title = os.path.splitext(file_path)[0].strip()
        
        catalog_file = database.File(file_path, title)
        destination = self.content_map.destination(catalog_file.extension)
        
        if destination:
            file_content_folder_path = os.path.join(self.content_path, destination) # <path to catalog>/content/<schema path>/
            
            if not os.path.isdir(file_content_folder_path):
                os.makedirs(file_content_folder_path)
            
            file_content_folder_path = tempfile.mkdtemp(suffix='', prefix='', dir=file_content_folder_path) # <path to catalog>/content/<schema path>/<temp folder>/
            temp_folder_name = os.path.basename(file_content_folder_path) # <temp folder>/
            catalog_file.content_path = os.path.join(destination, temp_folder_name) # <schema path>/<temp folder>/
            
            # original_name example = CHANGES LOG.txt
            # content_name example = Changes_Log.txt
            catalog_file.content_name = os.path.splitext(catalog_file.original_name)[0].title().strip().replace(' ', '_') + '.' + catalog_file.extension
            
            dst_file_path = os.path.join(file_content_folder_path, catalog_file.content_name) # <path to catalog>/content/<schema path>/<temp folder>/<content name>
            
            shutil.copyfile(file_path, dst_file_path)
            
            # TODO: Update file checkin log. The checkin log will be a csv file with checkin date/time, original path, and content path located in the logs folder of the catalog.
            # TODO: Add metadata file creation
        else:
            raise CatalogError("Unknown File extension, cannot checkin file")
        
        self.session.add(catalog_file) 
        self.session.commit()
        
        return catalog_file
    
    def checkout(self, catalog_file_id, dst_path=None):
        
        catalog_file = self.file(catalog_file_id)
        
        if catalog_file:
            if dst_path is None:
                dst_path = catalog_file.original_path
                
            checkout_path = os.path.join(dst_path, catalog_file.original_name)
            file_content_path = os.path.join(catalog_file.content_path, catalog_file.content_name)
            src_path = os.path.join(self.content_path, file_content_path)
            
            if not os.path.isdir(dst_path):
                os.makedirs(dst_path)
            
            shutil.copyfile(src_path, checkout_path)
            
            return catalog_file
        else:
            raise CatalogError("No file exists with the specified ID exists within the catalog")
    
    def files(self, order_by=database.File.id):
        
        files = tuple(self.session.query(database.File).order_by(order_by))
        
        return files
    
    def file(self, catalog_file_id):
        
        # TODO: Add finding file by ID, then by title, then by content_name, and then by content_path
        file = self.session.query(database.File).get(catalog_file_id)
        
        return file
    
    def remove_file(self, remove_file):
            
        self.session.delete(remove_file)
        self.session.commit()
            
        remove_path = os.path.join(self.content_path, remove_file.content_path)
        shutil.rmtree(remove_path)
        
        return remove_file
            
    def tags(self, order_by=database.Tag.name):
        
        tags = tuple(self.session.query(database.Tag).order_by(order_by))
        
        return tags
    
    def tag(self, catalog_file, tag_name):
        
        tag = self.session.query(database.Tag).filter_by(name=tag_name).first()
        
        if not tag:
            tag = database.Tag(tag_name)
        
        catalog_file.tags.append(tag)
        self.session.commit()
        
        return (catalog_file, tag)
    
    def detag(self, catalog_file, tag_name):
        
        tag = self.session.query(database.Tag).filter_by(name=tag_name).first()
        
        if tag:
            # TODO: Add check if file is tagged by tag_name before removal
            catalog_file.tags.remove(tag)
            self.session.commit()
        
        return (catalog_file, tag)
    
    def create_tag(self, tag_name):
        
        tag = database.Tag(tag_name)
        self.session.add(tag)
        self.session.commit()
        
        return tag
    
    def remove_tag(self, tag_name):
        
        remove_tag = self.session.query(database.Tag).filter_by(name=tag_name).one()
        self.session.delete(remove_tag)
        self.session.commit()
        
        return remove_tag
        
    def get_files_by_tags(self, tag_names):
        
        query = self.session.query(database.File)
        
        for tag_name in tag_names:
            query = query.filter(database.File.tags.any(database.Tag.name == tag_name))
        
        files = query.all()
        
        return tuple(files)
    
    # TODO: Add file_count method
    # TODO: Add tag_count method

class ContentSchema(object):                       
    
    # XML    
    PREFIX = 'ds'
    NAMESPACE = 'descatter/2013/content_schema/1.0'
    XPATH_NAMESPACE = {PREFIX: NAMESPACE}
    
    # Tags
    INFO_TAG = 'info'
    TITLE_TAG = 'title'
    AUTHOR_TAG = 'author'
    NAME_TAG = 'name'
    EMAIL_TAG = 'email'
    DESCRIPTION_TAG = 'description'
    MACROS_TAG = 'macros'
    MACRO_TAG = 'macro'
    TEXT_TAG = 'text'
    GROUP_TAG = 'group'
    DESTINATIONS_TAG = 'destinations'
    DESTINATION_TAG = 'destination'
    FOLDER_TAG = 'folder'
    FILE_TAG = 'file'
    METADATA_TAG = 'metadata'
    
    # Attributes
    CASE_ATTRIBUTE = 'case'
    CASE_SENSITIVE_ATTRIBUTE = 'case-sensitive'
    CONDITION_ATTRIBUTE = 'conditions'
    MACRO_ATTRIBUTE = 'macro'
    MATCH_ATTRIBUTE = 'match'
    NAME_ATTRIBUTE = 'name'
    PREFIX_ATTRIBUTE = 'prefix'
    REPLACE_SPACES_WITH_ATTRIBUTE = 'replace-spaces-with'
    SUFFIX_ATTRIBUTE = 'suffix'
    TEMPLATE_ATTRIBUTE = 'template'
    USE_ATTRIBUTE = 'use'
    VALUE_ATTRIBUTE = 'value'
    
    ANY_WILDCARD = '*'
    
    # Conditions
    EQUALS_CONDITION = 'equals'
    GREATER_THAN_CONDITION = 'greater-than'
    LESS_THAN_CONDITION = 'less-than'
    
    
    
    CASES = ('lowercase', 'uppercase', 'capitalize-first', 'capitalize-all', 'sentence', 'title')
    VARIABLES = ('file-path',
                 'file-name',
                 'file-extension',
                 'file-size',
                 'file-date-created',
                 'file-date-modified',
                 'file-date-accessed',
                 'file-date-added',
                 'file-title',
                 'file-index',
                 'file-count',
                 'temp-folder',
                 'metadata-extension')
    
    def __init__(self, schema_file_path):
        
        self.schema_file_path = schema_file_path
        self.root = etree.parse(self.schema_file_path).getroot() 
               
        self.get_use_attribute = etree.XPath(("//" + 
                                              self.PREFIX + 
                                              ":" + 
                                              self.DESTINATIONS_TAG + 
                                              "/@" + 
                                              self.USE_ATTRIBUTE), 
                                             namespaces=self.XPATH_NAMESPACE)
        
        self.get_destination_elements = etree.XPath(("//" +
                                                     self.PREFIX +
                                                     ":" +
                                                     self.DESTINATIONS_TAG +
                                                     "/" +
                                                     self.PREFIX +
                                                     ":" +
                                                     self.DESINTATION_TAG),
                                                    namespaces=self.XPATH_NAMESPACE)
        
        self.get_destination_element = etree.XPath(("//" +
                                                    self.PREFIX +
                                                    ":" +
                                                    self.DESTINATIONS_TAG +
                                                    "/" +
                                                    self.PREFIX +
                                                    ":" +
                                                    self.DESTINATION_TAG +
                                                    "[@" +
                                                    self.MATCH_ATTRIBUTE +
                                                    "=$match]"), 
                                                   namespaces=self.XPATH_NAMESPACE)
        
        self.get_folder_names = etree.XPath(("//" +
                                             self.PREFIX +
                                             ":" +
                                             self.DESTINATIONS_TAG +
                                             "/" +
                                             self.PREFIX +
                                             ":" +
                                             self.DESTINATION_TAG +
                                             "[@" +
                                             self.MATCH_ATTRIBUTE +
                                             "=$match]//" +
                                             self.PREFIX +
                                             ":" +
                                             self.FOLDER_TAG +
                                             "/@" +
                                             self.NAME_ATTRIBUTE), 
                                            namespaces=self.XPATH_NAMESPACE)
            
    def matches(self, destination_element, checkin_file_value):
        match_value = destination_element.get(self.MATCH_ATTRIBUTE)
        match_condition = destination_element.get(self.CONDITION_ATTRIBUTE)
        conditions = {self.EQUALS_CONDITION: self.match_equals,
                      self.GREATER_THAN_CONDITION: self.match_greater_than,
                      self.LESS_THAN_CONDITION: self.match_less_than}
        
        return conditions[match_condition](match_value, checkin_file_value)
        
    def match_equals(self, match_value, checkin_file_value):
        # TODO: Add handling of any wildcard
        return match_value == checkin_file_value
    
    def match_greater_than(self, match_value, checkin_file_value):
        # TODO: Add handling of any wildcard
        return match_value > checkin_file_value
    
    def match_less_than(self, match_value, checkin_file_value):
        # TODO: Add handling of any wildcard
        return match_value < checkin_file_value
        
    def get_destination(self, checkin_file):
        
        use_variable = self.get_use_attribute(self.root)[0]
        checkin_file_value = checkin_file[use_variable]
        destination_elements = self.get_destination_elements(self.root)
        
        for destination_element in destination_elements:
            if self.matches(destination_element, checkin_file_value):
                break    
        
        if destination_element is None:
            raise CatalogError("A destination could not be found for the checkin file")
        else:
            destination_file_path = self.content_folder_path = os.path.join(os.path.dirname(self.schema_file_path), constants.CONTENT_FOLDER_NAME)
            folder_names = self.get_folder_names(self.root, match=match_value)
            
            for folder_name in folder_names:
                destination_file_path = os.path.join(destination_file_path, folder_name)
            
            # TODO: Add creation of unique, random folder name
            # TODO: Add 'unique-random' macro parsing
            
            return destination_file_path
    
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
    
    def destination(self, file_extension):
                      
        if file_extension in self.map:
            return self.map[file_extension]
        else:
            return None