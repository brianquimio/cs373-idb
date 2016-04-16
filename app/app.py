#!/usr/local/bin/python

# -------
# Imports
# -------

import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask.ext.script import Manager, Server
from flask.ext.sqlalchemy import SQLAlchemy
import json
import logging


# ------------------------------
# Configure logger for debugging
# ------------------------------

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Welcome to Virtual Address Space")

# -------------
# Configure app
# -------------


SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username='guestbook-admin',
        password='my-random-password',
        hostname='pythonwebapp_db',
        database='guestbook'
        )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True))
db = SQLAlchemy(app)

# ---------
# DB models
# ---------


class State(db.Model):
    """
    state_code is a 2 digit postal code for the state
    state_name is the full name of the state 
    latitude is a string representing the lat of state
    longitude is a string representing the long of state
    """
    __tablename__ = 'State'

    # Dimensions
    state_code = db.Column(db.String(256), primary_key=True)
    state_name = db.Column(db.String(256), unique=True)
    latitude = db.Column(db.String(256))
    longitude = db.Column(db.String(256))

    def serialize(self):
        logger.debug('Serializing state: ' + str(self.state_code))

        return dict(state_code=self.state_code, state_name=self.state_name, latitude=self.latitude, longitude=self.longitude)

    def __init__(self, state_code, state_name, latitude, longitude):
        self.state_code = state_code
        self.state_name = state_name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "[State: state_id={}, state_name={}]".format(self.state_id, self.state_code)

class City(db.Model):
    """
    city_id is a unique identifier for the city, state combination
    state_code is a unique identifier for the state
    city_name is the name of a city as a string
    """
    __tablename__ = 'City'

    # Dimensions
    city_id = db.Column(db.String(256), primary_key=True)
    city_name = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.String(256), nullable=True)
    longitude = db.Column(db.String(256), nullable=True)

    # Relationships
    state_code = db.Column(db.String(256), nullable=False)

    def serialize(self):
        return dict(city_id=self.city_id, city_name=self.city_name, latitude=self.latitude, longitude=self.longitude, state_code=self.state_code)

    def __init__(self, city_id, city_name, state_code, latitude, longitude):
        self.city_id = city_id
        self.city_name = city_name
        self.state_code = state_code
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "[City: city_id={}, city_name={}, state_name={}]".format(self.city_id, self.city_name, self.state_code, self.latitude, self.longitude)


class Neighborhood(db.Model):
    """
    neighbordhood_id is a unique identifier (pk) for a neighborhood
    city_id is a unique identifier for the city, state combination
    state_id is a unique identifier for the state
    neighborhood_name is the name of a neighborhood as a string
    """
    __tablename__ = 'Neighborhood'

  # Dimensions
    neighborhood_id = db.Column(db.String(256), primary_key=True)
    neighborhood_name = db.Column(db.String(256), nullable=False)

    # Relationships
    state_code = db.Column(db.String(256), nullable=False)
    city_id = db.Column(db.String(256), nullable=False)

    def serialize(self):
        logger.debug('Serializing neighborhoods: ' + str(self.neighborhood_name))
        return dict(neighborhood_id=self.neighborhood_id, neighborhood_name=self.neighborhood_name, state_code=self.state_code, city_id=self.city_id)

    def __init__(self, neighborhood_id, neighborhood_name, state_code, city_id):
        self.neighborhood_id = str(neighborhood_id)
        self.neighborhood_name = neighborhood_name
        self.state_code = state_code
        self.city_id = str(city_id)

    def __repr__(self):
        return "[Neighborhood: neighborhood_id={}, neighborhood_name={}".format(self.neighborhood_id, self.neighborhood_name)



def init_states(states_json):
    """
    Insert data for states pulled from trulia API
    for each state in the json file, a new tuple is added to the table
    after a tuple is added, the session is committed to the server
    """


    for state in states_json["states"]:
        s = State(state['stateCode'], state['name'], state['latitude'], state['longitude'])
        db.session.add(s)
        db.session.commit()


def init_cities(cities_json):
    """
    Insert data for cities pulled from trulia API
    for each neighborhood in the json file, a new tuple is added to the table
    after a tuple is added, the session is committed to the server
    """

    for city in cities_json["cities"]:
      s = City(city['cityId'], city['name'], city['stateCode'], city['latitude'], city['longitude'])
      db.session.add(s)
      db.session.commit()

def init_neighborhoods(neighborhood_json):
    """
    Insert data for neighborhoods pulled from trulia API
    for each neighborhood in the json file, a new tuple is added to the table
    after a tuple is added, the session is committed to the server
    TODO: figure out if the neighborhoods are being inserted to the DB or not.
    """

    for neighborhood in neighborhoods_json["neighborhoods"]:
      s = Neighborhood(neighborhood['id'], neighborhood['name'], neighborhood['stateCode'], neighborhood['city'])
      db.session.add(s)
      db.session.commit()


def init_state_stats(state_stats):
    """
    takes a JSON object in
    parses the json into StateStats objects that can then be added and committed to the DB
    TODO: confirm that this is parsing correctly
    TODO: validate output as well-formed JSON
    """

    state_codes = state_stats['stateStats'].keys()

    for code in state_codes:
        for week in state_stats['stateStats'][code]['listingStat']:
            week_of = week['weekEndingDate']
            for subcat in state_stats['stateStats'][code]['listingStat']['listingPrice']['subcategory']:
                num_properties = subcat['numberOfProperties']
                med_listing_price = int(subcat['medianListingPrice'])
                avg_listing_price = int(subcat['averageListingPrice'])
                property_type = subcat['type']

                stats = StateStats(week_of, property_type, num_properties, med_listing_price, avg_listing_price, code)
                
                db.session.add(stats)
                db.session.commit()

def init_city_stats(city_stats):
    """
    takes a JSON object in
    parses the json into CityStats objects that can then be added and committed to the DB
    TODO: confirm that this is parsing correctly
    TODO: validate output as well-formed JSON
    """

    city_codes = city_stats['cityStats'].keys()

    for code in city_codes:
        for week in city_stats['cityStats'][code]['listingStat']:
            week_of = week['weekEndingDate']
            for subcat in city_stats['cityStats'][code]['listingStat']['listingPrice']['subcategory']:
                num_properties = subcat['numberOfProperties']
                med_listing_price = int(subcat['medianListingPrice'])
                avg_listing_price = int(subcat['averageListingPrice'])
                property_type = subcat['type']

                stats = CityStats(week_of, code, property_type, num_properties, avg_listing_price, med_listing_price)
                
                db.session.add(stats)
                db.session.commit()

def init_neighborhood_stats(neighborhood_stats):
    """
    takes a JSON object in
    parses the json into NeighborhoodStats objects that can then be added and committed to the DB
    TODO: confirm that this is parsing correctly
    TODO: validate output as well-formed JSON
    """

    neighborhood_codes = neighborhood_stats['neighborhoodStats'].keys()

    for code in neighborhood_codes:
        for week in neighborhood_stats['neighborhoodStats'][code]['listingStat']:
            week_of = week['weekEndingDate']
            for subcat in neighborhood_stats['cityStats'][code]['listingStat']['listingPrice']['subcategory']:
                num_properties = subcat['numberOfProperties']
                med_listing_price = int(subcat['medianListingPrice'])
                avg_listing_price = int(subcat['averageListingPrice'])
                property_type = subcat['type']

                stats = NeighborhoodStats(week_of, code, property_type, num_properties, med_listing_price, avg_listing_price)
                
                db.session.add(stats)
                db.session.commit()

def init_db():
    """
    initialize the database
    drops all tables in the DB in case a table required already exists
    creates all tables (based on the model classes)
    inserts the data from scraped JSON files into each of the tables created from models
    TODO: add in stats JSON parsers. These haven't been validated and are currently commented out.
    """

    db.drop_all()
    db.create_all()

    # Init states
    with open('json_data/states.json') as states:
        init_states(json.load(states))

    # Init cities
    with open('json_data/cities.json') as cities:
        init_cities(json.load(cities))

    # Init neighborhoods
    with open('json_data/neighborhoods.json') as neighborhoods:
        logger.debug("neighborhoods.json is now open");
        init_neighborhoods(json.load(neighborhoods))

    # # Init states
    # with open('json_data/state_stats.json') as state_stats:
    #     init_state_stats(json.load(state_stats))

    # # Init cities
    # with open('json_data/city_stats.json') as city_stats:
    #     init_city_stats(json.load(city_stats))

    # # Init neighborhoods
    # with open('json_data/neighborhood_stats.json') as neighborhood_stats:
    #     init_neighborhood_stats(json.load(neighborhood_stats))


# -----------
# URL Routing
# -----------

@app.route('/')
def splash():
    """
    renders the home page (index.html in the templates subfolder)
    """
    logger.debug("splash")
    return send_file('templates/index.html')

@app.route('/about.html')
def about():
    """
    renders the about page (about.html in the templates subfolder)
    """
    logger.debug("about")
    return send_file('templates/about.html')

# ----------------
# API Routing
# ----------------

@app.route('/api/')
def api_root():
        data = {
                            'urls': {
                                                'state_url': '/state',
                                                'city_url': '/city',
                                                'neighborhood': '/neighborhood'
                            }}
        return jsonify(data)


@app.route('/api/state/')
def api_state_all():
    """
    requests all tuples from the State table
    constructs a json file from each of the State model instances contained in the DB
    returns a json that is then routed to the api/state/ URL
    """
    jsonData = {}
    for data in State.query:
        jsonData[data.state_code] = data.serialize()
    return jsonify(jsonData)

# @app.route('/api/state/<statecode>')
# def api_state_spec(statecode):
#     statedata = State.query.get(statecode)
#     return jsonify(statedata.serialize())


@app.route('/api/city/')
def api_cities_all():
    """
    requests all tuples from the City table
    constructs a json file from each of the City model instances contained in the DB
    returns a json that is then routed to the api/city/ URL
    """
    jsonData = {}
    for data in City.query:
        jsonData[data.city_id] = data.serialize()
    return jsonify(jsonData)

# @app.route('/api/cities/<cityID>')
# def api_city_spec(cityID):

#     with open('json_data/city_stats.json') as cities:
#         json_data = json.load(cities)

#     json_data = [x for x in json_data if ]


@app.route('/api/neighborhood/')
def api_neighborhood_all():
    """
    requests all tuples from the Neighborhood table
    constructs a json file from each of the Neighborhood model instances contained in the DB
    returns a json that is then routed to the /api/neighborhood URL
    TODO: figure out why this is returning an empty result set
    """

    return send_file('json_data/neighborhoods.json')
    # jsonData = {}

    # for data in Neighborhood.query:
    #     # logger.debug("Neighborhood: " + string(data.serialize()))
    #     jsonData[data.neighborhood_id] = data.serialize()
    # return jsonify(jsonData)

# @app.route('/api/neighborhood/<nID>')
# def api_neighborhood_spec(nID):
#     nData = Neighborhood.query.get(nID)
#     return jsonify(nData.serialize())


#------
# Tests
#------

@app.route('/tests')
def render_tests():
    """
    runs the tests.py file as a subprocess and saves the output to a test_results variable
    returns a json file containing the test results
    """
    # logger.debug("create_db")
    test_results = subprocess.getoutput("python3 tests.py")
    return json.dumps({'test_results': str(test_results)})


# ----------------
# Manager Commands
# ----------------

@manager.command
def create_db():
    """
    This command is used to initialize the database and insert the data scraped from Trulia
    TODO: look into refactoring init_db() and create_db()
    """
    # logger.debug("+++++++++++++++++++++ create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    init_db()

@manager.command
def drop_db():
    """
    This command can be called to drop all tables used for our models.
    """
    # logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()

# -------
# Run App
# -------

if __name__ == '__main__':
    manager.run()
