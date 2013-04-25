# Application Structure
APPLICATION_NAME = 'descatter'
APPLICATION_DESCRIPTION = "A cross-platform desktop application for cataloging, organizing, and tagging files"
DATA_FOLDER_NAME = 'data'
FILE_NAME_KEY = 'name'
FILE_PATH_KEY = 'path'

# Database constants
SQLITE_EXTENSION = '.sqlite'
TAGS_TABLE_NAME = 'tags'
DATE_ADDED_COLUMN_NAME = 'date_added'
TAG_HIERARCHY_TABLE_NAME = 'tag_hierarchy'
FILES_TABLE_NAME = 'files'
FILES_TAGS_TABLE_NAME = 'files_tags'
CONTENT_TYPES_TABLE_NAME = 'content_types'
CONTENT_TYPES_ID_COLUMN_NAME = 'content_types_id'
MEDIA_TYPE_NAME_COLUMN_NAME = 'media_type_name'
MEDIA_SUBTYPE_NAME_COLUMN_NAME = 'media_subtype_name'
FILE_EXTENSIONS_TABLE_NAME = 'file_extensions'
FILE_EXTENSIONS_ID_COLUMN_NAME = 'file_extensions_id'
EXTENSION_COLUMN_NAME = 'extension'
DESCRIPTION_COLUMN_NAME = 'description'
FILE_ASSOCIATIONS_TABLE_NAME = 'file_associations'
FILE_ASSOCIATIONS_ID_COLUMN_NAME = 'file_associations_id'
DEFAULT_CATALOG_DB_NAME = 'default_catalog_db' + SQLITE_EXTENSION

# Tests constants
TEST_CATALOG_NAME = 'Test_Catalog'
TESTS_FOLDER_NAME = 'tests'

# Command line constants
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

# Console constants
CONSOLE_PROMPT = APPLICATION_NAME + ': '
CONSOLE_DESCRIPTION = APPLICATION_NAME + " Interactive Console"
ABSOLUTE_ARGUMENT_SHORT_NAME = 'a'
ABSOLUTE_ARGUMENT_LONG_NAME = 'absolute'
ABSOLUTE_ARGUMENT_HELP = "Display the absolute path instead of the relative path"
SCHEMA_ARGUMENT_SHORT_NAME = 's'
SCHEMA_ARGUMENT_LONG_NAME = 'schema'
SCHEMA_ARGUMENT_HELP = "Define the initial content folder structure and file associations"

# XML constants
CONTENT_SCHEMA_NAMESPACE = APPLICATION_NAME + '/2013/content_schema'
CONTENT_FOLDER_TAG_NAME = 'contentFolder'
FOLDER_TAG_NAME = '{' + CONTENT_SCHEMA_NAMESPACE + '}' + 'folder'
XMLNS_ATTRIBUTE_NAME = 'xmlns'
NAME_ATTRIBUTE_NAME = 'name'
ID_ATTRIBUTE_NAME = 'id'
EXTENSIONS_TAG_NAME = '{' + CONTENT_SCHEMA_NAMESPACE + '}' + 'extensions'
EXTENSION_TAG_NAME = '{' + CONTENT_SCHEMA_NAMESPACE + '}' + 'extension'

# Catalog folder structure constants
CONTENT_FOLDER_NAME = 'content'
TEMPLATES_FOLDER_NAME = 'templates'
HOOKS_FOLDER_NAME = 'hooks'
LOG_FOLDER_NAME = 'log'
CONTENT_SCHEMA_FILE_NAME = 'content_schema.xml'

CATALOG_FOLDER_NAMES = [CONTENT_FOLDER_NAME, 
                        TEMPLATES_FOLDER_NAME, 
                        HOOKS_FOLDER_NAME,
                        LOG_FOLDER_NAME]

HOOK_NAMES = [CHECKIN_ARGUMENT_LONG_NAME]

BEFORE_TRIGGER_NAME = 'before'
AFTER_TRIGGER_NAME = 'after'

TRIGGER_NAMES = [BEFORE_TRIGGER_NAME,
                 AFTER_TRIGGER_NAME]