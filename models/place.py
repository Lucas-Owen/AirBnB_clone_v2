#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity


place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        nullable=False,
        primary_key=True
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        nullable=False,
        primary_key=True
    )
)
"""Represents the many to many relationship table
between Place and Amenity records.
"""


class Place(BaseModel, Base):
    """ A place to stay """
    amenity_ids = []
    __tablename__ = 'places'
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(
            String(60),
            ForeignKey('cities.id'),
            nullable=False
        )
        user_id = Column(
            String(60),
            ForeignKey('users.id'),
            nullable=False
        )
        name = Column(
            String(128),
            nullable=False
        )
        description = Column(
            String(1024),
            nullable=True
        )
        number_rooms = Column(
            Integer,
            nullable=False,
            default=0
        )
        number_bathrooms = Column(
            Integer,
            nullable=False,
            default=0
        )
        max_guest = Column(
            Integer,
            nullable=False,
            default=0
        )
        price_by_night = Column(
            Integer,
            nullable=False,
            default=0
        )
        latitude = Column(
            Float,
            nullable=True
        )
        longitude = Column(
            Float,
            nullable=True
        )
        reviews = relationship(
            'Review',
            cascade="all, delete, delete-orphan",
            backref='place'
        )
        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            viewonly=False,
            backref='place_amenities'
        )
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        reviews = None

        @property
        def amenities(self):
            """Returns the amenities of this Place"""
            from models import storage
            amenities_of_place = []
            for value in storage.all(Amenity).values():
                if value.id in self.amenity_ids:
                    amenities_of_place.append(value)
            return amenities_of_place

        @amenities.setter
        def amenities(self, value):
            """Adds an amenity to this Place"""
            if type(value) is Amenity:
                if value.id not in self.amenity_ids:
                    self.amenity_ids.append(value.id)

        @property
        def reviews(self):
            """Returns the reviews of this Place"""
            from models import storage
            reviews_of_place = []
            for value in storage.all(Review).values():
                if value.place_id == self.id:
                    reviews_of_place.append(value)
            return reviews_of_place
