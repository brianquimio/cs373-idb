#!/usr/local/bin/python

# -------
# Imports
# -------

from flask import Flask, render_template, request, redirect, url_for, send_file
from flask.ext.sqlalchemy import SQLAlchemy
from db import db
# from flask.ext.app.builder

# ---------
# DB models
# ---------


class State(db.Model):
    """
    state_id is a unique identifier for the state
    state_code is a 2 digit postal code for the state
    state_name is the full name of the state 
    """
    __tablename__ = 'State'

	# Dimensions
    state_id = db.Column(db.Integer, unique=True)
    state_code = db.Column(db.String(256), primary_key=True)
    state_name = db.Column(db.String(256), unique=True)
    latitude = db.Column(db.String(256))
    longitude = db.Column(db.String(256))

    def __init__(self, state_id, state_code, state_name, latitude, longitude):
        self.state_id = state_id
        self.state_code = state_code
        self.state_name = state_name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "[State: state_id={}, state_name={}]".format(self.state_id, self.state_code)


class StateStats(db.Model):
    """
    week_of is the interval over which the data is aggregated
    state_code is a 2 digit postal code for the state
    property_type is a string that describes the number of bedrooms a property has
    num_properties are the number of properties listed given the parameters above
    avg_listing_price is the average listing price during the given time period
    med_listing_price is the median listing price during the given time period
    """

    __tablename__ = 'StateStats'


    # Dimensions
    id = db.Column(db.Integer, primary_key=True)
    week_of = db.Column(db.Date)
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.Integer)
    med_listing_price = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)


    # Relationships
    state_code = db.Column(db.String(256), db.ForeignKey('State.state_code'))

    def __init__(self, week_of, property_type, num_properties, med_listing_price, avg_listing_price, state_code):
        self.week_of = week_of
        self.property_type = property_type
        self.num_properties = num_properties
        self.avg_listing_price = avg_listing_price
        self.med_listing_price = med_listing_price
        self.state_code = state_code


class City(db.Model):
    """
    city_id is a unique identifier for the city, state combination
    state_code is a unique identifier for the state
    city_name is the name of a city as a string
    """
    __tablename__ = 'City'

    # Dimensions
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(256), nullable=False)

    # Relationships
    state_code = db.Column(db.String(256), db.ForeignKey('State.state_code'))

    def __init__(self, city_id, city_name, state_code, latitude, longitude):
        self.city_id = city_id
        self.city_name = city_name
        self.state_code = state_code
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "[City: city_id={}, city_name={}, state_name={}]".format(self.city_id, self.city_name, self.state_code, self.latitude, self.longitude)


class CityStats(db.Model):
    """
    week_of is the interval over which the data is aggregated
    state_code is a 2 digit postal code for the state
    property_type is a string that describes the number of bedrooms a property has
    num_properties are the number of properties listed given the parameters above
    avg_listing_price is the average listing price during the given time period
    med_listing_price is the median listing price during the given time period
    city_id is the foreign_key to uniquely identify which city the information belongs to
    """

    __tablename__ = 'CityStats'

    # Dimensions
    id = db.Column(db.Integer, primary_key=True)
    week_of = db.Column(db.Date)
    state_code = db.Column(db.String(256), unique=True)
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)
    med_listing_price = db.Column(db.Integer)

    # Relationships
    city_id = db.Column(db.Integer, db.ForeignKey('City.city_id'))

    def __init__(self, week_of, state_code, property_type, num_properties, avg_listing_price, med_listing_price, city_id):
        self.week_of = week_of
        self.state_code = state_code
        self.property_type = property_type
        self.num_properties = num_properties
        self.avg_listing_price = avg_listing_price
        self.med_listing_price = med_listing_price
        self.city_id = city_id


class Neighborhood(db.Model):
    """
    neighbordhood_id is a unique identifier (pk) for a neighborhood
    city_id is a unique identifier for the city, state combination
    state_id is a unique identifier for the state
    neighborhood_name is the name of a neighborhood as a string
    """
    __tablename__ = 'Neighborhood'

	# Dimensions
    neighborhood_id = db.Column(db.Integer, primary_key=True)
    neighborhood_name = db.Column(db.Integer, nullable=False)

    # Relationships
    state_code = db.Column(db.String(256), db.ForeignKey('State.state_code'))
    city_id = db.Column(db.Integer, db.ForeignKey('City.city_id'))

    def __init__(self, neighborhood_id, neighborhood_name, state_code, city_id):
        self.neighborhood_id = neighborhood_id
        self.neighborhood_name = neighborhood_name
        self.state_code = state_code
        self.city_id = city_id

    def __repr__(self):
        return "[Neighborhood: neighborhood_id={}, neighborhood_name={}".format(self.neighborhood_id, self.neighborhood_name)


class NeighborhoodStats(db.Model):
    """
    week_of is the interval over which the data is aggregated
    property_type is a string that describes the number of bedrooms a property has
    num_properties are the number of properties listed given the parameters above
    avg_listing_price is the average listing price during the given time period
    med_listing_price is the median listing price during the given time period
    neighborhood_id is the foreign key that maps the statistics of a neighborhood to itself
    """

    # Dimensions
    id = db.Column(db.Integer, primary_key=True)
    week_of = db.Column(db.Date)
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)
    med_listing_price = db.Column(db.Integer)

    # Relationships
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('Neighborhood.neighborhood_id'))

    def __init__(self, week_of, neighborhood_id, property_type, num_properties, med_listing_price, avg_listing_price):
        self.week_of = week_of
        self.property_type = property_type
        self.num_properties = num_properties
        self.avg_listing_price = avg_listing_price
        self.med_listing_price = med_listing_price
        self.neighborhood_id = neighborhood_id
