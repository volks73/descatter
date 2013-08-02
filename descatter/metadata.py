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

FILES_TABLE_NAME = 'files'
FILES_ID_COLUMN_NAME = FILES_TABLE_NAME + '_id'
PATH_COLUMN_NAME = 'path'
TAGS_TABLE_NAME = 'tags'
TAGS_ID_COLUMN_NAME = TAGS_TABLE_NAME + '_id'
NAME_COLUMN_NAME = 'name'
FILE_TAGS_TABLE_NAME = 'file_tags'

Base = declarative_base()
Session = sessionmaker()

def connect(path):
    """Connects to the database.
    
    :param path: A path. The path to the SQLite database file.
    
    """
    
    engine_path = 'sqlite:///' + path
    engine = create_engine(engine_path, echo=False, poolclass=NullPool)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

file_tags = Table(FILE_TAGS_TABLE_NAME,
                  Base.metadata,
                  Column(FILES_ID_COLUMN_NAME, Integer, ForeignKey(FILES_TABLE_NAME + '.' + FILES_ID_COLUMN_NAME)),
                  Column(TAGS_ID_COLUMN_NAME, Integer, ForeignKey(TAGS_TABLE_NAME + '.' + TAGS_ID_COLUMN_NAME)))

class File(Base):
    __tablename__ = FILES_TABLE_NAME
    
    id = Column(Integer, name=FILES_ID_COLUMN_NAME, primary_key=True)
    path = Column(String, name=PATH_COLUMN_NAME, nullable=False, unique=True)

    tags = relationship('Tag', secondary=file_tags, backref=FILES_TABLE_NAME)

    def __init__(self, path):
        
        self.path = os.path.abspath(path)

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, name=TAGS_ID_COLUMN_NAME, primary_key=True)
    name = Column(String, name=NAME_COLUMN_NAME, nullable=False, unique=True)
    # TODO: Add value column
    
    def __init__(self, name):
        
        self.name = name