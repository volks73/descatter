import os
import sqlite3

databaseConnection = None
sqliteExtension = '.sqlite'      
      
def create(rootPath):
    
    if os.path.isdir(rootPath):
        # TODO: check if files and folders already exist in rootPath
        # TODO: prompt user if files and folders already exist in rootPath
        
        rootFolderPath = os.path.dirname(rootPath) # The path minus the folder name
        rootFolderName = os.path.basename(rootPath) # Just the folder name, no path information
        
        # If the path contains a terminating '\' or '/', then the rootFolderName will be
        # empty and the rootFolderPath will be the path minus the terminating '\' or '/' and
        # not the root folder path.
        if rootFolderName:
            pass
        else:
            rootFolderPath = os.path.dirname(rootPath)
            rootFolderName = os.path.basename(rootFolderPath)
    
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