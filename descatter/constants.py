# Application Structure
APPLICATION_NAME = 'descatter'
APPLICATION_DESCRIPTION = "A cross-platform desktop application for cataloging, organizing, and tagging files"
DATA_FOLDER_NAME = 'data'

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

# Catalog folder structure constants
CONTENT_FOLDER_NAME = 'content'
TEMPLATES_FOLDER_NAME = 'templates'
HOOKS_FOLDER_NAME = 'hooks'
LOG_FOLDER_NAME = 'log'

CATALOG_FOLDER_NAMES = [CONTENT_FOLDER_NAME, 
                        TEMPLATES_FOLDER_NAME, 
                        HOOKS_FOLDER_NAME,
                        LOG_FOLDER_NAME]

HOOK_NAMES = [CHECKIN_ARGUMENT_LONG_NAME]

BEFORE_TRIGGER_NAME = 'before'
AFTER_TRIGGER_NAME = 'after'

TRIGGER_NAMES = [BEFORE_TRIGGER_NAME,
                 AFTER_TRIGGER_NAME]

APPLICATION_MEDIA_TYPE_NAME = 'application'
AUDIO_MEDIA_TYPE_NAME = 'audio'
IMAGE_MEDIA_TYPE_NAME = 'image'
MESSAGE_MEDIA_TYPE_NAME = 'message'
MODEL_MEDIA_TYPE_NAME = 'model'
MULTIPART_MEDIA_TYPE_NAME = 'multipart'
TEXT_MEDIA_TYPE_NAME = 'text'
VIDEO_MEDIA_TYPE_NAME = 'video'

MEDIA_TYPE_NAMES =[APPLICATION_MEDIA_TYPE_NAME,
                   AUDIO_MEDIA_TYPE_NAME,
                   IMAGE_MEDIA_TYPE_NAME,
                   MESSAGE_MEDIA_TYPE_NAME,
                   MODEL_MEDIA_TYPE_NAME,
                   MULTIPART_MEDIA_TYPE_NAME,
                   TEXT_MEDIA_TYPE_NAME,
                   VIDEO_MEDIA_TYPE_NAME]

# TODO: add complete list of Media Types according to the IANA register
# Defaults
DEFAULT_CONTENT_TYPES = [(APPLICATION_MEDIA_TYPE_NAME, 'msword'),
                         (APPLICATION_MEDIA_TYPE_NAME, 'vnd.ms-excel'),
                         (APPLICATION_MEDIA_TYPE_NAME, 'vnd.ms-powerpoint'),
                         (TEXT_MEDIA_TYPE_NAME, 'csv'),
                         (TEXT_MEDIA_TYPE_NAME, 'xml'),
                         (TEXT_MEDIA_TYPE_NAME, 'plain'),
                         (TEXT_MEDIA_TYPE_NAME, 'html'),
                         (IMAGE_MEDIA_TYPE_NAME, 'jpeg'),
                         (IMAGE_MEDIA_TYPE_NAME, 'tiff'),
                         (IMAGE_MEDIA_TYPE_NAME, 'png')]

DEFAULT_FILE_EXTENSIONS = [('doc', "A Microsoft Word document"),
                           ('docx', "A Microsoft Word document"),
                           ('xls', "A Microsoft Excel spreadsheet"),
                           ('xlsx', "A Microsoft Excel spreadsheet"),
                           ('ppt', "A Microsoft PowerPoint Presentation"),
                           ('pptx', "A Microsoft PowerPoint Presentation"),
                           ('csv', "A comma-separated values file"),
                           ('xml', "An eXtensible Markup Language file"),
                           ('txt', "A plain text file"),
                           ('html', "A HyperText Markup Language file"),
                           ('htm', "A HyperText Markup Language file"),
                           ('jpg', "A Join Photographic Experts Group image file"),
                           ('jpeg', "A Join Photographic Experts Group image file"),
                           ('tif', "A Tagged Image File Format image file"),
                           ('tiff', "A Tagged Image File Format image file"),
                           ('png', "A Portable Network Graphic image file")] 
                             
# Files are associated with a content type by their extension to their appropriate Media Subtype.
# The period has been removed
DEFAULT_FILE_ASSOCIATIONS = {'doc' : 'application/msword',
                           'docx' : 'application/msword',
                           'xls' : 'application/vnd.ms-excel',
                           'xlsx' : 'application/vnd.ms-excel',
                           'ppt' : 'application/vnd.ms-powerpoint',
                           'pptx' : 'application/vnd.ms-powerpoint',
                           'csv' : 'text/csv',
                           'xml' : 'text/xml',
                           'txt' : 'text/plain',
                           'html' : 'text/html',
                           'htm' : 'text/html',
                           'jpg' : 'image/jpeg',
                           'jpeg' : 'image/jpeg',
                           'tif' : 'image/tiff',
                           'tiff' : 'image/tiff',
                           'png' : 'image/png'}
