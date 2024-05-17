#!/usr/bin/python3
"""
Module for serializing and deserializing data.
"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City

class FileStorage:
    """
    FileStorage class for storing, serializing, and deserializing data.
    """
    __file_path = "file.json"
    __objects = {}

    def new(self, obj):
        """
        Sets an object in the __objects dictionary with a key of <obj class name>.id.
        """
        obj_cls_name = obj.__class__.__name__
        key = f"{obj_cls_name}.{obj.id}"
        FileStorage.__objects[key] = obj

    def all(self):
        """
        Returns the __objects dictionary. It provides access to all the stored objects.
        """
        return FileStorage.__objects

    def save(self):
        """
        Serializes the __objects dictionary into JSON format and saves it to the file specified by __file_path.
        """
        obj_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects if the file exists.
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
                try:
                    obj_dict = json.load(file)
                    for key, value in obj_dict.items():
                        class_name = value["__class__"]
                        cls = eval(class_name)
                        instance = cls(**value)
                        FileStorage.__objects[key] = instance
                except json.JSONDecodeError:
                    pass
