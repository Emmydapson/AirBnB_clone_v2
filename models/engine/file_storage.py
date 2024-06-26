#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls:
            cls_name = cls.__name__ if type(cls) == type else cls
            return {k: v for k, v in
                    FileStorage.__objects.items() if str(cls_name) in k}
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""

        if obj:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            if obj_key in FileStorage.__objects:
                del FileStorage.__objects[obj_key]

    def close(self):
        """Close the file storage by reloading the JSON file"""

        self.reload()
