#!/usr/bin/env python


"""
Use this file if using PostgreSQL for the application.

Note: the default database for the project is SQLite. If using
PostgreSQL, either (a) the name of this file will need to be changed
to database_setup.py (and therefore the original database_setup.py file
will need to be renamed, moved to another directory, or deleted) or
(b) the import lines for the database_setup file in application.py and
populator.py will need to be changed to database_setup_postgres.

Another change is also required to run Nuevo México with PostgreSQL.
Replace line 38 in application.py, line 85 in database_setup_postgres.py,
and line 7 in populator.py with the following:

engine = create_engine('postgresql://catalog:INSERT_PASSWORD_FOR_DATABASE_HERE@localhost/catalog')

"""


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import backref

Base = declarative_base()


class User(Base):
    """Create a Users table"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    placeTypes = relationship('PlaceType', backref="user")
    places = relationship('Place', backref="user")


class PlaceType(Base):
    """Create a PlaceType table"""
    __tablename__ = 'placeType'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    places = relationship('Place', backref="placeType", cascade="all, delete-orphan")

    # Set up the related JSON API endpoints
    @property
    def serialize(self):
        """Return object data in an easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


class Place(Base):
    """Create a Place table"""
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(850))
    location = Column(String(250), nullable=False)
    price = Column(String(10))
    link = Column(String(300))
    placeType_id = Column(Integer, ForeignKey('placeType.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    # Set up the related JSON API endpoints
    @property
    def serialize(self):
        """Return object data in an easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'location': self.location,
            'price': self.price,
            'link': self.link
        }


# Create a database engine
engine = create_engine('sqlite:///nuevomexico.db')

Base.metadata.create_all(engine)
