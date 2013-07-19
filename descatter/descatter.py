APPLICATION_NAME = 'descatter'

class TaggerError(Exception): pass

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
