#!/usr/bin/env python3
"""
Contains class BaseModel
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """ The BaseModel class from which future classes will be derived"""

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs) -> None:
        """ Initialization of the BaseModel"""
        # Set default values for id and created_at
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        # Iterate over keyword arguments and set attributes
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
            # Parse created_at if it's a string
            if 'created_at' in kwargs and isinstance(kwargs['created_at'], str):
                self.created_at = datetime.fromisoformat(kwargs['created_at'])

    def __str__(self) -> str:
        """String representation of the BaseModel class"""
        return f'[{self.__class__.__name__}] {self.id} {self.to_dict()}'

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()

        if 'created_at' in new_dict:
            new_dict['created_at'] = new_dict['created_at'].isoformat()
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        return new_dict
