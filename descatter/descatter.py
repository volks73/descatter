import os
import tempfile
import shutil

import schema

class FilerError(Exception): pass
class TaggerError(Exception): pass

class Filer(object):
    # Responsible for placing files into folders based on direction from the PathFinder
    # Needs to create a ".descatter" hidden folder in the base folder. This hidden
    # folder contains the tags SQLite database, templates for metadata, and schema definition.
    
    def __init__(self, base_folder_path, schema_file_path):
        self.base_folder_path = base_folder_path
        self.path_finder = schema.PathFinder(schema_file_path)
    
    def split_path(self, path):
        head, tail = os.path.split(path)
        return (self.split_path(head) if len(head) and len(tail) else []) + [tail]
    
    def file(self, source_file_path, delete_source=False):
        destination_path = self.path_finder.find_path(source_file_path, schema.create_variables(source_file_path, 1, 1))
        folder_names = self.split_path(os.path.dirname(destination_path))
        
        current_path = self.base_folder_path
        for folder_name in folder_names:
            if folder_name == schema.RANDOM_PLACEHOLDER:
                current_path = tempfile.mkdtemp(suffix='', prefix='', dir=current_path)
            else:
                current_path = os.path.join(current_path, folder_name)
                os.makedirs(current_path, exist_ok=True)
        
        destination_file_path = os.path.basename(destination_path)
        random_placeholder_index = destination_file_path.find(schema.RANDOM_PLACEHOLDER) 
        
        if random_placeholder_index == -1:
            destination_file_path = os.path.join(current_path, destination_file_path)
        else:
            prefix = destination_file_path[:random_placeholder_index]
            suffix = destination_file_path[random_placeholder_index+1:]

            temp_file_handle, destination_file_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=current_path, text=False)
            
            # Ensure the race condition, thread-safe created temporary file has been closed and is not used by another
            # process so that it can be replaced by the source file.
            os.fdopen(temp_file_handle, 'w').close()
        
        shutil.copy2(source_file_path, destination_file_path)
        
        if delete_source:
            os.remove(source_file_path)
    
    def batch_file(self, os_folder_path):
        # TODO: Add filing of all files in the folder
        pass
    
    def recursive_batch_file(self, os_folder_path):
        # TODO: Add filing of all files in the folder and every subfolder. 
        pass

class ReFiler(object): pass
    # Responsible for searching the base folder and ensuring all files conform to the schema
    # or changing the structure if a new schema is selected.
    
class Tagger(object): pass
    # Responsible for tagging files and managing the database
    # Creates a hidden folder named ".descatter" in a folder and places a SQLite
    # database in the hidden folder. This stores the tags for all files in the
    # sub-folder of the base folder.
    
    # TODO: Check if .descatter folder exists
    # TODO: Create .descatter hidden folder
    # TODO: Copy schema definition file to hidden folder

class Viewer(object): pass # Or maybe rename to Organizer
    # Graphical User Interface (GUI) to view a folder that has been descattered
    # A descattered folder has a hidden folder ".descatter" that contains
    # the tags database, templates for metadata, and schema definition and has all files
    # filed and organized according to a schema.
    
    # The viewer has four panes that can be re-sized and hidden as needed.
    # Left-most pane, or pane 1, is a file manager/explorer similar to Windows Explorer
    # with files and folders listed in various user selected views. Advanced features for
    # navigation will exist. Center pane, or pane 2, shows the tags database. This includes
    # a listing of all tags and virtual folders which the user can select and deselect
    # to show files and metadata in the right most pane, or pane 3. A search bar above the tag
    # listing allows for searching of files by tags and metadata. Pane 3 shows a list
    # of files based on selected tags. The files can be clicked on to expand the node and
    # show the metadata for the file. An advanced search option is also available. GUI
    # commands include filing, batch filing, re-filing, tagging, detagging, creating virtual
    # folders, export to csv, etc. If the folder selected in pane 1 is has not been descatter, 
    # the remaining two panes are empty and hidden to maximize the viewing the of file system view.
