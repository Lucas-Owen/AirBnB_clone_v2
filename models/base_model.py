#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DATETIME, nullable=False, default=datetime.utcnow())
    updated_at = Column(DATETIME, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            if kwargs.get('__class__', None):
                del kwargs['__class__']
            if not hasattr(kwargs, 'id'):
                self.id = str(uuid.uuid4())
            if not hasattr(kwargs, 'created_at'):
                self.created_at = datetime.now()
            else:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            if not hasattr(kwargs, 'updated_at'):
                self.updated_at = datetime.now()
            else:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        items = dict(self.__dict__)
        if items.get('_sa_instance_state', None):
            del items['_sa_instance_state']
        return '[{}] ({}) {}'.format(cls, self.id, items)

    def delete(self):
        """Deletes this BaseModel instance from the storage"""
        from models import storage
        storage.delete(self)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        result = {}
        for key, value in self.__dict__.items():
            if key != '_sa_instance_state':
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        result['__class__'] = self.__class__.__name__
        return result
