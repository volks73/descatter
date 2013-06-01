from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Column, String, Integer, ForeignKey, create_engine

import os

import constants

Base = declarative_base()
Session = sessionmaker()

# Association Table between Files and Tags
file_tags = Table(
                  constants.FILE_TAGS_TABLE_NAME, 
                  Base.metadata,
                  Column(constants.FILES_ID_COLUMN_NAME, Integer, ForeignKey(constants.FILES_TABLE_NAME + '.' + constants.FILES_ID_COLUMN_NAME)),
                  Column(constants.TAGS_ID_COLUMN_NAME, Integer, ForeignKey(constants.TAGS_TABLE_NAME + '.' + constants.TAGS_ID_COLUMN_NAME))
                  )

class File(Base):
    __tablename__ = constants.FILES_TABLE_NAME
    
    id = Column(Integer, name=constants.FILES_ID_COLUMN_NAME, primary_key=True)
    content_path = Column(String, name=constants.CONTENT_PATH_COLUMN_NAME)
    content_name = Column(String, name=constants.CONTENT_NAME_COLUMN_NAME)
    original_path = Column(String, name=constants.ORIGINAL_PATH_COLUMN_NAME)
    original_name =  Column(String, name=constants.ORIGINAL_NAME_COLUMN_NAME)
    title = Column(String, name=constants.TITLE_COLUMN_NAME, nullable=False)
    # TODO: Add date_added column
    
    tags = relationship('Tag', secondary=file_tags, backref=constants.FILES_TABLE_NAME)
    
    def __init__(self, file_path, title):
        
        self.original_path = os.path.dirname(file_path)
        self.original_name = os.path.basename(file_path)
        self.extension = os.path.splitext(file_path)[1][1:].strip().lower() 
        self.title = title

class Tag(Base):
    __tablename__ = constants.TAGS_TABLE_NAME
    
    id = Column(Integer, name=constants.TAGS_ID_COLUMN_NAME, primary_key=True)
    name = Column(String, name=constants.NAME_COLUMN_NAME, nullable=False, unique=True)
    # TODO: Add date_added column
    
    def __init__(self, name):
        
        self.name = name

def connect(catalog_path):
    
    db_file_path = os.path.join(catalog_path, constants.TAGS_DB_NAME)
    engine_path = constants.DIALECT + ':///' + db_file_path
    engine = create_engine(engine_path)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)
    
    return Session()