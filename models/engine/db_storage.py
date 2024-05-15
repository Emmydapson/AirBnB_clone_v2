#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """This class manages storage of hbnb models in mysql"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiation method"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        conStr = f'mysql+mysqldb://{user}:{password}@{host}/{database}'

        self.__engine = create_engine(conStr, pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        my_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.session.query(cls)
            for element in query:
                key = "{type(element).__name__}.{element.id})"
                my_dict[key] = element
        else:
            listModel = [State, City, User, Place, Review, Amenity]
            for mod in listModel:
                query = self.__session.query(mod)
                for element in query:
                    key = "{type(element).__name__}.{element.id})"
                    my_dict[key] = element
        return (my_dict)

    def new(self, obj):
        """adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commits  all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload storage into __session"""
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """CLose the database storage by removing or closing the session"""

        self.__session.close()
