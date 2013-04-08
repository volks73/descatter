import os
import sqlite3

# TODO: Add logging

databaseConnection = None
sqliteExtension = '.sqlite'      
      
def create(rootPath):
    
    if os.path.isdir(rootPath):
        # TODO: check if files and folders already exist in rootPath
        # TODO: prompt user if files and folders already exist in rootPath
        
        # If the path contains a terminating '\' or '/', then the rootFolderName will be
        # empty and the rootFolderPath will be rootPath minus the terminating '\' or '/'.
        # Continue removing the tail of the path until rootFolderPath is actually 
        # a folder name. 
        rootFolderPath = rootPath
        rootFolderName = None
               
        while not rootFolderName:
            rootFolderName = os.path.basename(rootFolderPath)
            rootFolderPath = os.path.dirname(rootFolderPath)
    
        catalogPath = os.path.join(rootPath, "catalog")
        templatesPath = os.path.join(rootPath, "templates")
        hooksPath = os.path.join(rootPath, "hooks")
          
        os.mkdir(catalogPath)
        os.mkdir(templatesPath)
        os.mkdir(hooksPath)
                    
        databaseFileName = rootFolderName + sqliteExtension
        databaseFilePath = os.path.join(rootPath, databaseFileName)
               
        databaseConnection = sqlite3.connect(databaseFilePath)
        
        # TODO: SQL table structure creation here
        
        databaseConnection.close() 
        
    else:
        raise Exception("create path not a folder/directory")