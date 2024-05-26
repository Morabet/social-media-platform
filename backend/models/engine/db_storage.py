#!/usr/bin/env python3
""" Contains the class DBStorage"""

import os
from models.base_model import Base
from models.user import User
from models.post import Post
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {"User": User, "Post": Post}


class DBStorage:
    """ Database Storage Engine for SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self) -> None:
        """ Initialize the database storage engine"""
        username = os.getenv("SG_DB_USER")
        pwd = os.getenv("SG_DB_PWD")
        host = os.getenv("SG_DB_HOST")
        data = os.getenv("SG_DB_NAME")

        if not all([username, pwd, host, data]):
            raise ValueError(
                "Database connection details are not properly set in environment variables.")

        # Create the database connection string
        connection_string = f'postgresql+psycopg2://{username}:{pwd}@{host}:5432/{data}'
        try:
            self.__engine = create_engine(connection_string)
            Base.metadata.drop_all(self.__engine)
            self.reload()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the database: {e}")

    def reload(self):
        """ create  current db session from engine using a sessionmaker"""

        # creates all the tables defined in the Base class
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def new(self, obj):
        """ add the object to the current db session"""
        self.__session.add(obj)

    def save(self):
        """ commit all change of the current db session"""
        self.__session.commit()

    def all(self, cls=None):
        """Query on the current database session."""
        new_dict = {}

        if cls and cls in classes:
            classes_to_query = [cls]
        else:
            classes_to_query = classes.values()
            # This becomes dict_values([User, Post, Comment])

        for c in classes_to_query:
            objs = self.__session.query(c).all()
            for obj in objs:
                key = f"{obj.__class__.__name__}.{obj.id}"
                new_dict[key] = obj

        return new_dict

    def delete(self, obj):
        """ delete from the current db session obj if not none"""
        self.__session.delete(obj)

    def close(self):
        """Close the current SQLAlchemy session"""
        self.__session.close()

    def remove(self):
        """Remove the current SQLAlchemy session"""
        self.__session.remove()
