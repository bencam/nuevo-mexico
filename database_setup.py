#!/usr/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Create a Users table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# Create a PlaceType table
class PlaceType(Base):
    __tablename__ = 'placeType'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # Set up the related JSON API endpoints
    @property
    def serialize(self):
        """Return object data in an easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id
        }


# Createa a Place table
class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    location = Column(String(250), nullable=False)
    price = Column(String(10))
    link = Column(String(300))
    placeType_id = Column(Integer, ForeignKey('placeType.id'))
    placeType = relationship(PlaceType)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

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


# Create an SQLite database called nuevomexico.db
engine = create_engine('sqlite:///nuevomexico.db')

Base.metadata.create_all(engine)
