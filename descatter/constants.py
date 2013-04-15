# Application Structure
APPLICATION_NAME = 'descatter'
DATA_FOLDER_NAME = 'data'

# Database constants
SQLITE_EXTENSION = '.sqlite'
TAGS_TABLE_NAME = 'tags'
TAG_HIERARCHY_TABLE_NAME = 'tag_hierarchy'
FILES_TABLE_NAME = 'files'
FILES_TAGS_TABLE_NAME = 'files_tags'
CONTENT_TYPES_TABLE_NAME = 'content_types'
FILE_EXTENSIONS_TABLE_NAME = 'files_extensions'
FILE_ASSOCIATIONS_TABLE_NAME = 'file_associations'
DEFAULT_CATALOG_DB_NAME = 'default_catalog_db' + SQLITE_EXTENSION

# Tests constants
TEST_CATALOG_NAME = 'Test_Catalog'
TESTS_FOLDER_NAME = 'tests'

# Command line constants
INTERACTIVE_MODE_PROMPT = 'descatter$: '
COMMAND_SHORT_PREFIX = '-'
COMMAND_LONG_PREFIX = '--'
CATALOG_ARGUMENT_SHORT_NAME = 'c'
CATALOG_ARGUMENT_LONG_NAME = 'catalog'
ESTABLISH_ARGUMENT_SHORT_NAME = 'e'
ESTABLISH_ARGUMENT_LONG_NAME = 'establish'
CWC_ARGUMENT_SHORT_NAME = 'cwc'
CWF_ARGUMENT_SHORT_NAME = 'cwf'
FILE_ARGUMENT_SHORT_NAME = 'f'
FILE_ARGUMENT_LONG_NAME = 'file'
CHECKIN_ARGUMENT_SHORT_NAME = 'in'
CHECKIN_ARGUMENT_LONG_NAME = 'checkin'
INTERACTIVE_ARGUMENT_SHORT_NAME = 'i'
INTERACTIVE_ARGUMENT_LONG_NAME = 'interactive'
EXIT_ARGUMENT_SHORT_NAME = 'x'
EXIT_ARGUMENT_LONG_NAME = 'exit'

# Catalog folder structure constants
CONTENT_FOLDER_NAME = 'content'
TEMPLATES_FOLDER_NAME = 'templates'
HOOKS_FOLDER_NAME = 'hooks'
LOG_FOLDER_NAME = 'log'

CATALOG_FOLDER_NAMES = [CONTENT_FOLDER_NAME, 
                        TEMPLATES_FOLDER_NAME, 
                        HOOKS_FOLDER_NAME,
                        LOG_FOLDER_NAME]

HOOK_NAMES = ['establish']

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
DEFAULT_CONTENT_TYPES = {'msword' : APPLICATION_MEDIA_TYPE_NAME,
                         'vnd.ms-excel' : APPLICATION_MEDIA_TYPE_NAME,
                         'vnd.ms-powerpoint' : APPLICATION_MEDIA_TYPE_NAME,
                         'csv' : TEXT_MEDIA_TYPE_NAME,
                         'xml' : TEXT_MEDIA_TYPE_NAME,
                         'plain' : TEXT_MEDIA_TYPE_NAME,
                         'html' : TEXT_MEDIA_TYPE_NAME,
                         'jpeg' : IMAGE_MEDIA_TYPE_NAME,
                         'tiff' : IMAGE_MEDIA_TYPE_NAME,
                         'png' : IMAGE_MEDIA_TYPE_NAME}
                             
# Files are associated with a content type by their extension to their appropriate Media Subtype.
# The period has been removed
DEFAULT_FILE_ASSOCIATES = {'doc' : 'msword',
                           'docx' : 'msword',
                           'xls' : 'vnd.ms-excel',
                           'xlsx' : 'vnd.ms-excel',
                           'ppt' : 'vnd.ms-powerpoint',
                           'pptx' : 'vnd.ms-powerpoint',
                           'csv' : 'csv',
                           'xml' : 'xml',
                           'txt' : 'plain',
                           'html' : 'html',
                           'htm' : 'html',
                           'jpg' : 'jpeg',
                           'jpeg' : 'jpeg',
                           'tif' : 'tiff',
                           'tiff' : 'tiff',
                           'png' : 'pin'}
