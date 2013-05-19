# Application Structure
APPLICATION_NAME = 'descatter'
APPLICATION_DESCRIPTION = "A cross-platform desktop application for cataloging, organizing, and tagging files"
DATA_FOLDER_NAME = 'data'
FILE_NAME_KEY = 'name'
FILE_PATH_KEY = 'path'
FILE_EXT_KEY = 'ext'

# Database
SQLITE_EXTENSION = '.sqlite'
TAGS_DB_NAME = 'tags' + SQLITE_EXTENSION
DEFAULT_TAGS_DB_NAME = 'default_' + TAGS_DB_NAME

# Database table names
TAGS_TABLE_NAME = 'tags'
TAGS_HIERARCHY_TABLE_NAME = 'tags_hierarchy'
FILES_TABLE_NAME = 'files'
FILES_TAGS_TABLE_NAME = 'files_tags'
VIRTUAL_FOLDERS_TABLE_NAME = 'virutal_folders'
VIRTUAL_FOLDERS_TAGS_TABLE_NAME = 'virtual_folders_tags'

# Database column names
ID_COLUMN_NAME = '_id'
FILES_ID_COLUMN_NAME = FILES_TABLE_NAME + ID_COLUMN_NAME
FILES_PATH_COLUM_NAME = 'file_path'
ORIGINAL_FILE_NAME_COLUMN_NAME = 'original_file_name'
FILES_TAGS_ID_COLUMN_NAME = FILES_TAGS_TABLE_NAME + ID_COLUMN_NAME
CONTENT_PATH_COLUMN_NAME = 'content_path'
ORIGINAL_FILE_NAME_COLUMN_NAME = 'original_file_name'
CONTENT_FILE_NAME_COLUMN_NAME = 'content_file_name'
TITLE_COLUMN_NAME = 'title'
TAGS_ID_COLUMN_NAME = TAGS_TABLE_NAME + ID_COLUMN_NAME
NAME_COLUMN_NAME = 'name'
TAGS_HIERARCHY_ID_COLUMN_NAME = TAGS_HIERARCHY_TABLE_NAME + ID_COLUMN_NAME
TAGS_ID_CHILD_COLUMN_NAME = TAGS_ID_COLUMN_NAME + '_child'
TAGS_ID_PARENT_COLUMN_NAME = TAGS_ID_COLUMN_NAME + '_parent'
VIRTUAL_FOLDERS_ID_COLUMN_NAME = VIRTUAL_FOLDERS_TABLE_NAME + ID_COLUMN_NAME
VIRTUAL_FOLDERS_TAGS_ID_COLUMN_NAME = VIRTUAL_FOLDERS_TAGS_TABLE_NAME + ID_COLUMN_NAME

# Tests
TEST_CATALOG_NAME = 'Test_Catalog'
TESTS_FOLDER_NAME = 'tests'

# Command line
COMMAND_SHORT_PREFIX = '-'
COMMAND_LONG_PREFIX = '--'
CATALOG_ARGUMENT_SHORT_NAME = 'c'
CATALOG_ARGUMENT_LONG_NAME = 'catalog'
CATALOG_ARGUMENT_HELP = "Specify the catalog"
CREATE_ARGUMENT_LONG_NAME = 'create'
CREATE_ARGUMENT_HELP = "Creates a catalog"
FILE_ARGUMENT_SHORT_NAME = 'f'
FILE_ARGUMENT_LONG_NAME = 'file'
FILE_ARGUMENT_HELP = "Specify the file"
CHECKIN_ARGUMENT_SHORT_NAME = 'in'
CHECKIN_ARGUMENT_LONG_NAME = 'checkin'
CHECKIN_ARGUMENT_HELP = "Check in the specified file into the specified catalog"
INTERACTIVE_ARGUMENT_SHORT_NAME = 'i'
INTERACTIVE_ARGUMENT_LONG_NAME = 'interactive'
INTERACTIVE_ARGUMENT_HELP = "Start a console or interactive mode to execute a series of commands within the descatter application"
MAP_ARGUMENT_SHORT_NAME = 'm'
MAP_ARGUMENT_LONG_NAME = 'map'
MAP_ARGUMENT_HELP = "Perform an action related to maps"
TAG_ARGUMENT_SHORT_NAME = 't'
TAG_ARGUMENT_LONG_NAME = 'tag'
TAG_ARGUMENT_HELP = "Perform an action related to tags"
NAME_ARGUMENT_SHORT_NAME = 'n'
NAME_ARGUMENT_LONG_NAME = 'name'
NAME_ARGUMENT_HELP = "The name of a tag"
EXTENSION_ARGUMENT_SHORT_NAME = 'e'
EXTENSION_ARGUMENT_LONG_NAME = 'extension'
EXTENSION_ARGUMENT_HELP = "List the mapping for only the specified file extension"
DESTINATION_ARGUMENT_SHORT_NAME = 'd'
DESTINATION_ARGUMENT_LONG_NAME = 'destination'
DESTINATION_ARGUMENT_HELP = "Specifies the destination for a file extension relative to the content folder of the specified catalog"
ABSOLUTE_ARGUMENT_SHORT_NAME = 'a'
ABSOLUTE_ARGUMENT_LONG_NAME = 'absolute'
ABSOLUTE_ARGUMENT_HELP = "Display the absolute path instead of the relative path"
SCHEMA_ARGUMENT_SHORT_NAME = 's'
SCHEMA_ARGUMENT_LONG_NAME = 'schema'
SCHEMA_ARGUMENT_HELP = "Define the initial content folder structure and file associations"

# Console
CONSOLE_PROMPT_TERMINATOR = ': '
CONSOLE_PROMPT = APPLICATION_NAME + CONSOLE_PROMPT_TERMINATOR
CONSOLE_PROMPT_PREFIX = '['
CONSOLE_PROMPT_SUFFIX = ']'
CONSOLE_DESCRIPTION = APPLICATION_NAME + " Interactive Console"

# Console ASCII tables
FILE_EXTENSION_HEADER_NAME = 'Extension'
CONTENT_FOLDER_HEADER_NAME = 'Content Folder'
CONTENT_FOLDER_HEADER_ALIGNMENT = 'l'
TAG_HEADER_NAME = 'Tag'
TITLE_HEADER_NAME = 'Title'
CONTENT_PATH_HEADER_NAME = 'Content Path'
CONTENT_FILE_NAME_HEADER_NAME = 'Content File Name'
ORIGINAL_FILE_NAME_HEADER_NAME = 'Original File Name'

# XML
CONTENT_SCHEMA_FILE_NAME = 'content_schema.xml'
DEFAULT_CONTENT_SCHEMA_FILE_NAME = 'default_' + CONTENT_SCHEMA_FILE_NAME
CONTENT_SCHEMA_NAMESPACE = APPLICATION_NAME + '/2013/content_schema'
CONTENT_SCHEMA = '{%s}' % CONTENT_SCHEMA_NAMESPACE
NAMESPACE_MAP = {None : CONTENT_SCHEMA_NAMESPACE}
XML_ENCODING = 'UTF-8'
CONTENT_FOLDER_TAG_NAME = CONTENT_SCHEMA + 'contentFolder'
FOLDER_TAG_NAME = CONTENT_SCHEMA + 'folder'
XMLNS_ATTRIBUTE_NAME = 'xmlns'
NAME_ATTRIBUTE_NAME = 'name'
ID_ATTRIBUTE_NAME = 'id'
EXTENSIONS_TAG_NAME = CONTENT_SCHEMA + 'extensions'
EXTENSION_TAG_NAME = CONTENT_SCHEMA + 'extension'

# Catalog folder structure
CONTENT_FOLDER_NAME = 'content'
TEMPLATES_FOLDER_NAME = 'templates'
HOOKS_FOLDER_NAME = 'hooks'
LOG_FOLDER_NAME = 'log'
CATALOG_README_FILE_NAME = 'README.txt'
DEFAULT_README_FILE_NAME = 'catalog_' + CATALOG_README_FILE_NAME

CATALOG_FOLDER_NAMES = [CONTENT_FOLDER_NAME, 
                        TEMPLATES_FOLDER_NAME, 
                        HOOKS_FOLDER_NAME,
                        LOG_FOLDER_NAME]

HOOK_NAMES = [CHECKIN_ARGUMENT_LONG_NAME]

BEFORE_TRIGGER_NAME = 'before'
AFTER_TRIGGER_NAME = 'after'

TRIGGER_NAMES = [BEFORE_TRIGGER_NAME,
                 AFTER_TRIGGER_NAME]