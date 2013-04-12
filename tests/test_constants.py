from nose.tools import *

import constants

def test_application_name():
    assert(constants.APPLICATION_NAME == 'descatter', "APPLICATION_NAME not equal to 'descatter'")

def test_data_folder_name():
    assert(constants.DATA_FOLDER_NAME == 'data', "DATA_FOLDER_NAME not equal to 'data'")

def test_sqlite_extension():
    assert(constants.SQLITE_EXTENSION == '.sqlite', "SQLITE_EXTENSION not equal to '.sqlite'")

def test_tags_table_name():
    assert(constants.TAGS_TABLE_NAME == 'tags', "TAGS_TABLE_NAME not equal to 'tags'")

def test_tag_hierarchy_table_name():
    assert(constants.TAG_HIERARCHY_TABLE_NAME == 'tag_hierarchy', "TAG_HIERARCHY_TABLE_NAME not equal to 'tag_hierarchy'")
    
def test_files_table_name():
    assert(constants.FILES_TABLE_NAME == 'files', "FILES_TABLE_NAME not equal to 'files'")
    
def test_files_tags_table_name():
    assert(constants.FILES_TAGS_TABLE_NAME == 'files_tags', "FILES_TAGS_TABLE_NAME not equal to 'files_tags'")

def test_content_types_table_name():
    assert(constants.CONTENT_TYPES_TABLE_NAME == 'content_types', "CONTENT_TYPES_TABLE_NAME not equal to 'content_types'")

def test_file_extensions_table_name():
    assert(constants.FILE_EXTENSIONS_TABLE_NAME == 'file_extensions', "FILE_EXTENSIONS_TABLE_NAME not equal to 'file_extensions'")

def test_file_assocations_table_name():
    assert(constants.FILE_ASSOCIATIONS_TABLE_NAME == 'file_associations', "FILE_ASSOCIATIONS_TABLE_NAME not equal to 'file_associations'")
    
def test_default_catalog_db_name():
    assert(constants.DEFAULT_CATALOG_DB_NAME == 'default_catalog_db.sqlite', "DEFAULT_CATALOG_DB_NAME not equal to 'default_catalog_db.sqlite'")

def test_test_catalog_name():
    assert(constants.TEST_CATALOG_NAME == 'Test_Catalog', "TEST_CATALOG_NAME not equal to 'Test_Catalog'")

def test_test_folder_name():
    assert(constants.TESTS_FOLDER_NAME == 'tests', "TESTS_FOLDER_NAME not equal to 'tests'")

def test_create_subcommand_name():
    assert(constants.CREATE_SUBCOMMAND_NAME == 'create', "CREATE_SUBCOMMAND_NAME not equal to 'create'")
    
def test_subcommand_names():
    assert(constants.SUBCOMMAND_NAMES[0] == constants.CREATE_SUBCOMMAND_NAME, "CREATE_SUBCOMMAND_NAME not 0 element in CREATE_SUBCOMMAND_NAME")

def test_content_folder_name():
    assert(constants.CONTENT_FOLDER_NAME == 'content', "CONTENT_FOLDER_NAME not equal to 'content'")

def test_templates_folder_name():
    assert(constants.TEMPLATES_FOLDER_NAME == 'templates', "TEMPLATES_FOLDER_NAME not equal to 'templates'")
    
def test_hooks_folder_name():
    assert(constants.HOOKS_FOLDER_NAME == 'hooks', "HOOKS_FOLDER_NAME not equal to 'hooks'")

def test_log_folder_name():
    assert(constants.LOG_FOLDER_NAME == 'log', "LOG_FOLDER_NAME not equal to 'log'")

def test_catalog_folder_names():
    assert(constants.CATALOG_FOLDER_NAMES[0] == constants.CONTENT_FOLDER_NAME, "CONTENT_FOLDER_NAME not 0 element in CATALOG_FOLDER_NAMES")
    assert(constants.CATALOG_FOLDER_NAMES[1] == constants.TEMPLATES_FOLDER_NAME, "TEMPLATES_FOLDER_NAME not 1 element in CATALOG_FOLDER_NAMES")
    assert(constants.CATALOG_FOLDER_NAMES[2] == constants.HOOKS_FOLDER_NAME, "HOOKS_FOLDER_NAME not 2 element in CATALOG_FOLDER_NAMES")
    assert(constants.CATALOG_FOLDER_NAMES[3] == constants.LOG_FOLDER_NAME, "LOG_FOLDER_NAME not 3 element in CATALOG_FOLDER_NAMES")
    
def test_before_trigger_name():
    assert(constants.BEFORE_TRIGGER_NAME == 'before', "BEFORE_TRIGGER_NAME not equal to 'before'")
    
def test_after_trigger_name():
    assert(constants.AFTER_TRIGGER_NAME == 'after', "AFTER_TRIGGER_NAME not equal to 'after'")

def test_trigger_names():
    assert(constants.TRIGGER_NAMES[0] == constants.BEFORE_TRIGGER_NAME, "BEFORE_TRIGGER_NAME not 0 element in TRIGGER_NAMES")
    assert(constants.TRIGGER_NAMES[1] == constants.AFTER_TRIGGER_NAME, "AFTER_TRIGGER_NAME not 1 element in TRIGGER_NAMES")

def test_application_media_type_name():
    assert(constants.APPLICATION_MEDIA_TYPE_NAME == 'application', "APPLICATION_MEDIA_TYPE_NAME not equal to 'application'")
    
def test_audio_media_type_name():
    assert(constants.AUDIO_MEDIA_TYPE_NAME == 'audio', "AUDIO_MEDIA_TYPE_NAME not equal to 'audio'")

def test_image_media_type_name():
    assert(constants.IMAGE_MEDIA_TYPE_NAME == 'image', "IMAGE_MEDIA_TYPE_NAME not equal to 'image'")

def test_message_media_type_name():
    assert(constants.MESSAGE_MEDIA_TYPE_NAME == 'message', "MESSAGE_MEDIA_TYPE_NAME not equal to 'message'")

def test_model_media_type_name():
    assert(constants.MODEL_MEDIA_TYPE_NAME == 'model', "MODEL_MEDIA_TYPE_NAME not equal to 'model'")

def test_multipart_media_type_name():
    assert(constants.MULTIPART_MEDIA_TYPE_NAME == 'multipart', "MULTIPART_MEDIA_TYPE_NAME not equal to 'multipart'")

def test_text_media_type_name():
    assert(constants.TEXT_MEDIA_TYPE_NAME == 'text', "TEXT_MEDIA_TYPE_NAME not equal to 'text'")
    
def test_video_media_type_name():
    assert(constants.VIDEO_MEDIA_TYPE_NAME == 'video', "VIDEO_MEDIA_TYPE_NAME not equal to 'video'")

def test_media_type_names():
    assert(constants.MEDIA_TYPE_NAMES[0] == constants.APPLICATION_MEDIA_TYPE_NAME, "APPLICATION_MEDIA_TYPE_NAME not 0 element in MEDIA_TYPE_NAMES")
    assert(constants.MEDIA_TYPE_NAMES[1] == constants.AUDIO_MEDIA_TYPE_NAME, "AUDIO_MEDIA_TYPE_NAME not 1 element in MEDIA_TYPE_NAMES")
    assert(constants.MEDIA_TYPE_NAMES[2] == constants.IMAGE_MEDIA_TYPE_NAME, "IMAGE_MEDIA_TYPE_NAME not 2 element in MEDIA_TYPE_NAMES")
    assert(constants.MEDIA_TYPE_NAMES[3] == constants.MESSAGE_MEDIA_TYPE_NAME, "MESSAGE_MEDIA_TYPE_NAME not 3 element in MEDIA_TYPE_NAMES")
    assert(constants.MEDIA_TYPE_NAMES[4] == constants.MODEL_MEDIA_TYPE_NAME, "MODEL_MEDIA_TYPE_NAME not 4 element in MEDIA_TYPE_NAMES")
    assert(constants.MEDIA_TYPE_NAMES[5] == constants.MULTIPART_MEDIA_TYPE_NAME, "MULTIPART_MEDIA_TYPE_NAME not 5 element in MEDIA_TYPE_NAMES")
    assert(constants.MEDIA_TYPE_NAMES[6] == constants.TEXT_MEDIA_TYPE_NAME, "TEXT_MEDIA_TYPE_NAME not 6 element in MEDIA_TYPE_NAMES")
    assert(constants.MEDIA_TYPE_NAMES[7] == constants.VIDEO_MEDIA_TYPE_NAME, "VIDEO_MEDIA_TYPE_NAME not 7 element in MEDIA_TYPE_NAMES")    