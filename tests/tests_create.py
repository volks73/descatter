from nose.tools import *
from dani import main    
import os
import shutil

testExampleRootFolderName = 'Test_Example'
testExampleRootPath = os.path.join(os.getcwd(), testExampleRootFolderName)
testExampleCatalogPath = os.path.join(testExampleRootPath, 'catalog')
testExampleTemplatesPath = os.path.join(testExampleRootPath, 'templates')
testExampleHooksPath = os.path.join(testExampleRootPath, 'hooks')
testExampleDatabaseFile = os.path.join(testExampleRootPath, testExampleRootFolderName + '.sqlite')

def setup():
    os.mkdir(testExampleRootPath)

def teardown():
    shutil.rmtree(testExampleRootPath)

def test_create():
    main.create(testExampleRootPath)
    
    assert os.path.isdir(testExampleCatalogPath), "Catalog folder not created"
    assert os.path.isdir(testExampleTemplatesPath), "Templates folder not created"
    assert os.path.isdir(testExampleHooksPath), "Hooks folder not created"
    assert os.path.isfile(testExampleDatabaseFile), "Database file not created"