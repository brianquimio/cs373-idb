# -------
# Imports
# -------

from flask import Flask, render_template, request, redirect, url_for, send_file
import flask.ext.sqlalchemy
# from flask.ext.app.builder

# -----------
# DB models
# -----------

app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class State(db.Model):
    """
    state_id is a unique identifier for the state
    date is a record of when the data was inserted to the db
    state_name is a 2 digit postal code for the state
    property_type is a string that describes the number of bedrooms a property has
    num_properties are the number of properties listed given the parameters above
    avg_listing_price is the average listing price during the given time period
    """
    __tablename__ = 'State'

	# Dimensions
    state_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    state_name = db.Column(db.String(256), unique=True)
    property_type = db.Column(db.String(256))

    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)

    	
    def __repr__(self):
        return "[State: state_id={}, state_name={}]".format(self.state_id, self.state_name)

class City(db.Model):
    """
    city_id is a unique identifier for the city, state combination
    state_id is a unique identifier for the state
    date is a record of when the data was inserted to the db
    city_name is the name of a city as a string
    property_type is a string that describes the number of bedrooms a property has
    num_properties are the number of properties listed given the parameters above
    avg_listing_price is the average listing price during the given time period
    """
    __tablename__ = 'City'

    # Dimensions
    city_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    city_name = db.Column(db.String(256), nullable=False)
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)

    # Relationships
    state_id = db.Column(db.Integer, db.ForeignKey('State.state_id'))


    def __repr__(self):
        return "[City: city_id={}, city_name={}, state_name={}]".format(self.city_id, self.city_name, self.state_name)

class Neighborhood(db.Model):
    """
    neighbordhood_id is a unique identifier (pk) for a neighborhood
    city_id is a unique identifier for the city, state combination
    state_id is a unique identifier for the state
    date is a record of when the data was inserted to the db
    neighborhood_name is the name of a neighborhood as a string
    property_type is a string that describes the number of bedrooms a property has
    num_properties are the number of properties listed given the parameters above
    avg_listing_price is the average listing price during the given time period
    """
    __tablename__ = 'Neighborhood'

	# Dimensions
    neighborhood_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    neighborhood_name = db.Column(db.Integer, nullable=False)

	# Measures
    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)

    # Relationships
    state_id = db.Column(db.Integer, db.ForeignKey('State.state_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('City.city_id'))


    def __repr__(self):
        return "[Neighborhood: neighborhood_id={}, neighborhood_name={}".format(self.neighborhood_id, self.neighborhood_name)
