# Application Structure
APPLICATION_NAME = 'descatter'
APPLICATION_DESCRIPTION = "A cross-platform desktop application for cataloging, organizing, and tagging files"
DATA_FOLDER_NAME = 'data'

# Database
DIALECT = 'sqlite'
SQLITE_EXTENSION = '.sqlite'
TAGS_DB_NAME = 'tags' + SQLITE_EXTENSION
DEBUG_DATABASE = False

# Database table names
TAGS_TABLE_NAME = 'tags'
FILES_TABLE_NAME = 'files'
FILE_TAGS_TABLE_NAME = 'file_tags'

# Database column names
ID_COLUMN_NAME = '_id'
FILES_ID_COLUMN_NAME = FILES_TABLE_NAME + ID_COLUMN_NAME
ORIGINAL_PATH_COLUMN_NAME = 'original_path'
ORIGINAL_NAME_COLUMN_NAME = 'original_name'
CONTENT_PATH_COLUMN_NAME = 'content_path'
CONTENT_NAME_COLUMN_NAME = 'content_name'
TITLE_COLUMN_NAME = 'title'
TAGS_ID_COLUMN_NAME = TAGS_TABLE_NAME + ID_COLUMN_NAME
NAME_COLUMN_NAME = 'name'

# Command line
COMMAND_SHORT_PREFIX = '-'
COMMAND_LONG_PREFIX = '--'
LIST_SEPARATOR = ','
FIRST_ARGUMENT_LONG_NAME = 'first'
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
SCHEMA_ARGUMENT_SHORT_NAME = 's'
SCHEMA_ARGUMENT_LONG_NAME = 'schema'
SCHEMA_ARGUMENT_HELP = "Define the initial content folder structure and file associations"
VERBOSE_ARGUMENT_SHORT_NAME = 'v'
VERBOSE_ARGUMENT_LONG_NAME = 'verbose'
VERBOSE_ARGUMENT_HELP = "Display additional information during execution of a command"

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
ID_HEADER_NAME = 'ID'
TITLE_HEADER_NAME = 'Title'
TITLE_HEADER_ALIGNMENT = 'l'
CONTENT_PATH_HEADER_NAME = 'Content Path'
CONTENT_PATH_HEADER_ALIGNMENT = 'l'
CONTENT_NAME_HEADER_NAME = 'Content Name'
ORIGINAL_PATH_HEADER_NAME = 'Original Path'
ORIGINAL_NAME_HEADER_NAME = 'Original Name'

# XML
CONTENT_SCHEMA_FILE_NAME = 'content_schema.xml'
DEFAULT_CONTENT_SCHEMA_FILE_NAME = 'content_type_schema.xml'
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

CATALOG_FOLDER_NAMES = (
                        CONTENT_FOLDER_NAME, 
                        TEMPLATES_FOLDER_NAME, 
                        HOOKS_FOLDER_NAME,
                        LOG_FOLDER_NAME
                        )

HOOK_NAMES = (
              CHECKIN_ARGUMENT_LONG_NAME,
              TAG_ARGUMENT_LONG_NAME
              )

BEFORE_TRIGGER_NAME = 'before'
AFTER_TRIGGER_NAME = 'after'

TRIGGER_NAMES = (
                 BEFORE_TRIGGER_NAME,
                 AFTER_TRIGGER_NAME
                 )