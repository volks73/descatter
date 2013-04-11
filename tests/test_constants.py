import constants

def test_sqlite_extension():
    assert(constants.SQLITE_EXTENSION == '.sqlite', "SQLITE_EXTENSION not equal to '.sqlite'")

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
    
# TODO: add rest of tests for constants