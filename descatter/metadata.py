# descatter/metadata.py
# Copyright (C) 2013 the Descatter authors and contributers <see AUTHORS file>
#
# This module is part of Descatter.
#
# Descatter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Descatter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Descatter.  If not, see <http://www.gnu.org/licenses/>.

import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import NullPool
from sqlalchemy import Table, Column, String, Integer, ForeignKey, create_engine

class MetadataError(Exception): pass

ENTITIES_TABLE_NAME = 'entities'
ENTITIES_ID_COLUMN_NAME = ENTITIES_TABLE_NAME + '_id'
PATH_COLUMN_NAME = 'path'
TAGS_TABLE_NAME = 'tags'
TAGS_ID_COLUMN_NAME = TAGS_TABLE_NAME + '_id'
NAME_COLUMN_NAME = 'name'
ENTITY_TAGS_TABLE_NAME = 'entity_tags'

Base = declarative_base()
Session = sessionmaker()

entity_tags = Table(ENTITY_TAGS_TABLE_NAME,
                  Base.metadata,
                  Column(ENTITIES_ID_COLUMN_NAME, Integer, ForeignKey(ENTITIES_TABLE_NAME + '.' + ENTITIES_ID_COLUMN_NAME)),
                  Column(TAGS_ID_COLUMN_NAME, Integer, ForeignKey(TAGS_TABLE_NAME + '.' + TAGS_ID_COLUMN_NAME)))

class Entity(Base):
    __tablename__ = ENTITIES_TABLE_NAME
    
    id = Column(Integer, name=ENTITIES_ID_COLUMN_NAME, primary_key=True)
    path = Column(String, name=PATH_COLUMN_NAME, nullable=False, unique=True)

    tags = relationship('Tag', secondary=ENTITY_TAGS_TABLE_NAME, backref=ENTITIES_TABLE_NAME)

    def __init__(self, path):
        """Constructor for the :class:`.Entity` object."""
        
        self.path = os.path.abspath(path)

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, name=TAGS_ID_COLUMN_NAME, primary_key=True)
    name = Column(String, name=NAME_COLUMN_NAME, nullable=False, unique=True)
    # TODO: Add value column
    
    def __init__(self, name):
        """Constructor for the :class:`.Tag` object."""
        
        self.name = name

def init(path):
    """Initializes the metadata engine.
    
    :param path: A path. The path to the SQLite database file.
    
    """
    
    engine_path = 'sqlite:///' + path
    engine = create_engine(engine_path, echo=False, poolclass=NullPool)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

def entities():
    """Returns a list of all entities in the database."""
    
    session = Session()
    entities = session.query(Entity).order_by(Entity.id)
    session.close()
    
    return entities

def tags():
    """Returns a list of all tags in the database."""
    
    session = Session()
    tags = session.query(Tag).order_by(Tag.id)
    session.close()
    
    return tags

def tag(path, tags):
    """Tags a path.
    
    :param path: A path. A path to a file or folder.
    :param ts: A list of strings. The tags to apply to the path.
    
    """
    
    if not path:
        raise MetadataError("Path is empty")
    
    if not tags:
        raise MetadataError("No tags")
    
    session = Session()    
    path = os.path.abspath(path)
        
    if os.path.exists(path):        
        db_entity = session.query(Entity).filter_by(path=path).first()

        if not db_entity:
            db_entity = Entity(path)
            session.add(db_entity)
        
        for tag_name in tags:
            db_tag = session.query(Tag).filter_by(name=tag_name).first()
        
            if not db_tag:
                db_tag = Tag(tag_name)
        
            db_entity.tags.append(db_tag)
                
        session.commit()
        tag_names = []
        
        for tag in db_entity.tags:
            tag_names.append(tag.name)
        
        session.close()
        
        return path, tag_names
    else:
        session.close()
        raise MetadataError("Path does not exist")

def detag(path, tags):
    """Removes a tag from a path.
    
    :param path: A path. The path to a file or folder.
    :param tags: A list of strings. A list of tags to remove from the file or folder.
    
    """
    
    session = Session()
    entity = session.query(Entity).filter_by(path=path).first()
    
    if entity:
        for tag_name in tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            entity.tags.remove(tag)
    else:
        session.close()
        raise MetadataError("There is no tagged entity with the given path")
        
    session.commit()
    session.close()    

def find(tags):
    """Finds a path based on tags.
    
    :param tags: A list of strings. A list of tags.
    
    """
    
    session = Session()
    query = session.query(Entity)
    
    for tag in tags:
        query = query.filter(Entity.tags.any(Tag.name == tag))
    
    entities = query.all()
    session.close()
    
    return entities