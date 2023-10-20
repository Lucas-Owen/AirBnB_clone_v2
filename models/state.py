#!/usr/bin/python3
""" State Module for HBNB project """
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """ State class """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(
            String(128),
            nullable=False
        )
        cities = relationship(
            'City',
            cascade='all, delete, delete-orphan',
            backref='state'
        )
    else:
        name = ''
        
        @property
        def cities(self):
            """Returns cities in this State's instance"""
            from models import storage
            cities_in_state = []
            for value in storage.all(City).values():
                if value.state_id == self.id:
                    cities_in_state.append(value)
            return cities_in_state
