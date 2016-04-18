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
    state_name = db.Column(db.String(256))
    latitude = db.Column(db.String(256))
    longitude = db.Column(db.String(256))

    def serialize(self):
        # logger.debug('Serializing state: ' + str(self.state_code))
        return dict(state_code=self.state_code, state_name=self.state_name, latitude=self.latitude, longitude=self.longitude)

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
    week_of = db.Column(db.String(256))
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.String(256))
    med_listing_price = db.Column(db.String(256))
    avg_listing_price = db.Column(db.String(256))


    # Relationships
    state_code = db.Column(db.String(256))

    def serialize(self):
        # logger.debug('Serializing state stats: ' + str(self.state_code))
        return dict(id=self.id, week_of=self.week_of, property_type=self.property_type, 
            num_properties=self.num_properties, med_listing_price=self.med_listing_price, 
            avg_listing_price=self.avg_listing_price, state_code=self.state_code)


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
    latitude = db.Column(db.String(256))
    longitude = db.Column(db.String(256))

    # Relationships
    state_code = db.Column(db.String(256))

    def serialize(self):
        # logger.debug('Serializing city: ' + str(self.city_name))
        return dict(city_id=self.city_id, city_name=self.city_name, latitude=self.latitude, longitude=self.longitude, state_code=self.state_code)

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
    week_of = db.Column(db.String(256))
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.String(256))
    avg_listing_price = db.Column(db.String(256))
    med_listing_price = db.Column(db.String(256))

    # Relationships
    city_id = db.Column(db.String(256))

    def serialize(self):
        # logger.debug('Serializing city stats: ' + str(self.city_id))
        return dict(id=self.id, week_of=self.week_of, property_type=self.property_type, 
            num_properties=self.num_properties, med_listing_price=self.med_listing_price, 
            avg_listing_price=self.avg_listing_price, city_id=self.city_id)



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
    neighborhood_name = db.Column(db.String(256))

    # Relationships
    state_code = db.Column(db.String(256))
    city_id = db.Column(db.String(256))

    def serialize(self):
        # logger.info('Serializing neighborhood: ' + str(self.neighborhood_name))
        return dict(neighborhood_id=self.neighborhood_id, neighborhood_name=self.neighborhood_name, state_code=self.state_code, city_id=self.city_id)

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
    week_of = db.Column(db.String(256))
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.String(256))
    avg_listing_price = db.Column(db.String(256))
    med_listing_price = db.Column(db.String(256))

    # Relationships
    neighborhood_id = db.Column(db.String(256))

    def serialize(self):
        # logger.debug('Serializing neighborhood stats: ' + str(self.neighborhood_id))
        return dict(id=self.id, week_of=self.week_of, property_type=self.property_type, 
            num_properties=self.num_properties, med_listing_price=self.med_listing_price, 
            avg_listing_price=self.avg_listing_price, neighborhood_id=self.city_id)

def init_states(states_json):
    """
    Insert data for states pulled from trulia API
    for each state in the json file, a new tuple is added to the table
    after a tuple is added, the session is committed to the server
    """


    for state in states_json["states"]:
        s = State(state_code=state['stateCode'], state_name=state['name'], 
            latitude=state['latitude'], longitude=state['longitude'])
        db.session.add(s)
        db.session.commit()


def init_cities(cities_json):
    """
    Insert data for cities pulled from trulia API
    for each neighborhood in the json file, a new tuple is added to the table
    after a tuple is added, the session is committed to the server
    """

    for city in cities_json["cities"]:
      s = City(city_id=city['cityId'], city_name=city['name'], 
        state_code=city['stateCode'], latitude=city['latitude'], 
        longitude=city['longitude'])
      db.session.add(s)
      db.session.commit()

def init_neighborhoods(neighborhoods_json):
    """
    Insert data for neighborhoods pulled from trulia API
    for each neighborhood in the json file, a new tuple is added to the table
    after a tuple is added, the session is committed to the server
    TODO: figure out if the neighborhoods are being inserted to the DB or not.
    """
    logger.info('init neighborhoods called')


    for neighborhood in neighborhoods_json["neighborhoods"]:
      s = Neighborhood(neighborhood_id=neighborhood['id'], neighborhood_name=neighborhood['name'], 
        state_code=neighborhood['stateCode'], city_id=neighborhood['city'])
      
      db.session.add(s)
      db.session.commit()


def init_state_stats(state_stats):
    """
    takes a JSON object in
    parses the json into StateStats objects that can then be added and committed to the DB
    TODO: confirm that this is parsing correctly
    TODO: validate output as well-formed JSON
    """

    logger.debug('in the init_state_stats method')
    state_codes = state_stats['stateStats'][0]
    state_keys = state_codes.keys()


    for code in state_keys:
        for week in state_codes[code]['listingStat']:
            week_of = week['weekEndingDate']
            for subcat in week['listingPrice']['subcategory']:
                num_properties = subcat['numberOfProperties']
                med_listing_price = subcat['medianListingPrice']
                avg_listing_price = subcat['averageListingPrice']
                property_type = subcat['type']

                stats = StateStats(week_of=week_of, property_type=property_type, 
                    num_properties=num_properties, med_listing_price=med_listing_price, 
                    avg_listing_price=avg_listing_price, state_code=code)
                
                db.session.add(stats)
                db.session.commit()

def init_city_stats(city_stats):
    """
    takes a JSON object in
    parses the json into CityStats objects that can then be added and committed to the DB
    TODO: confirm that this is parsing correctly
    TODO: validate output as well-formed JSON
    """


    city_codes = city_stats['cityStats'][0]
    city_keys = city_codes.keys()


    for code in city_keys:
        for week in city_codes[code]['listingStat']:
            week_of = week['weekEndingDate']
            for subcat in week['listingPrice']['subcategory']:
                num_properties = subcat['numberOfProperties']
                med_listing_price = subcat['medianListingPrice']
                avg_listing_price = subcat['averageListingPrice']
                property_type = subcat['type']

                stats = CityStats(week_of=week_of, property_type=property_type, num_properties=num_properties, 
                    avg_listing_price=avg_listing_price, med_listing_price=med_listing_price, city_id=code)
                
                db.session.add(stats)
                db.session.commit()


def init_neighborhood_stats(neighborhood_stats):
    """
    takes a JSON object in
    parses the json into NeighborhoodStats objects that can then be added and committed to the DB
    TODO: confirm that this is parsing correctly
    TODO: validate output as well-formed JSON
    """

    neighborhood_codes = neighborhood_stats['neighborhoodStats'][0]
    neighborhood_keys = neighborhood_codes.keys()


    for code in neighborhood_keys:
        for week in neighborhood_codes[code]['listingStat']:
            week_of = week['weekEndingDate']
            for subcat in week['listingPrice']['subcategory']:
                num_properties = subcat['numberOfProperties']
                med_listing_price = subcat['medianListingPrice']
                avg_listing_price = subcat['averageListingPrice']
                property_type = subcat['type']

                stats = NeighborhoodStats(week_of=week_of, property_type=property_type, 
                    num_properties=num_properties, avg_listing_price=avg_listing_price, 
                    med_listing_price=med_listing_price, neighborhood_id=code)
                
                db.session.add(stats)
                db.session.commit()

@manager.command
def init_db():
    """
    initialize the database
    drops all tables in the DB in case a table required already exists
    creates all tables (based on the model classes)
    inserts the data from scraped JSON files into each of the tables created from models
    TODO: add in stats JSON parsers. These haven't been validated and are currently commented out.
    """


    db.drop_all()
    db.configure_mappers()
    logger.info('create all being called')
    db.create_all()
    db.session.commit()


    # # Init states
    logger.debug("init states called")
    with open('json_data/states.json') as states:
        init_states(json.load(states))

    # # Init cities
    logger.debug("init cities called")
    with open('json_data/cities.json') as cities:
        init_cities(json.load(cities))

    # Init neighborhoods
    logger.info("init db called: neighborhoods")
    with open('json_data/neighborhoods.json') as neighborhoods:
        init_neighborhoods(json.load(neighborhoods))

    # Init state stats
    logger.debug("init state stats being called")
    with open('json_data/state_stats.json') as state_stats:
        init_state_stats(json.load(state_stats))

    # Init city stats
    with open('json_data/city_stats.json') as city_stats:
        init_city_stats(json.load(city_stats))

    # # Init neighborhood stats
    with open('json_data/neighborhood_stats.json') as neighborhood_stats:
        init_neighborhood_stats(json.load(neighborhood_stats))


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


@app.route('/api/states/', methods=['POST'])
def api_state_all():
    """
    requests all tuples from the State table
    constructs a json file from each of the State model instances contained in the DB
    returns a json that is then routed to the api/state/ URL
    """
    if request.method == "POST":

        jsonData = {}

        test = State.query.all()

        if len(test) is 0:
            init_states(json.load(open('json_data/states.json')))

        for data in test:
            jsonData[data.state_code] = data.serialize()


        return jsonify(jsonData)

    else:
        return """<html><body>
        Something went horribly wrong
        </body></html>"""

@app.route('/api/states/<statecode>')
def api_state_spec(statecode):
    jsonData = {}

    test = StateStats.query.filter_by(state_code=statecode).all()

    if len(test) is 0:
        init_state_stats(json.load(open('json_data/state_stats.json')))

    #-----------
    # Debug Code
    #-----------

    # test_str = str(test)
    # logger.info(test_str)

    # ttdb = db.session.execute("""
    #     SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='StateStats'
    #     """)
    # for i in ttdb:
    #     logger.debug("Column: " + str(i[0]))

    for data in test:
        jsonData[data.id] = data.serialize()
    return jsonify(jsonData)


@app.route('/api/cities/')
def api_cities_all():
    """
    requests all tuples from the City table
    constructs a json file from each of the City model instances contained in the DB
    returns a json that is then routed to the api/city/ URL
    """
    jsonData = {}

    test = City.query.all()

    if len(test) is 0:
        init_cities(json.load(open('json_data/cities.json')))

    for data in test:
        jsonData[data.city_id] = data.serialize()
    return jsonify(jsonData)

@app.route('/api/cities/<cityID>')
def api_city_spec(cityID):
    jsonData = {}

    test = CityStats.query.filter_by(city_id=cityID).all()

    if len(test) is 0:
        init_city_stats(json.load(open('json_data/city_stats.json')))

    #-----------
    # Debug Code
    #-----------

    # test_str = str(test)
    # logger.info(test_str)

    # ttdb = db.session.execute("""
    #     SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='StateStats'
    #     """)
    # for i in ttdb:
    #     logger.debug("Column: " + str(i[0]))

    for data in test:
        jsonData[data.id] = data.serialize()
    return jsonify(jsonData)


@app.route('/api/neighborhoods/')
def api_neighborhood_all():
    """
    requests all tuples from the Neighborhood table
    constructs a json file from each of the Neighborhood model instances contained in the DB
    returns a json that is then routed to the /api/neighborhood URL
    TODO: figure out why this is returning an empty result set
    """


    jsonData = {}

    test = Neighborhood.query.all()

    if len(test) is 0:
        init_neighborhoods(json.load(open('json_data/neighborhoods.json')))
    
    #-----------
    # Debug Code
    #-----------

    # test_str = str(test)
    # logger.info(test_str)

    # ttdb = db.session.execute("""
    #     SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='Neighborhood'
    #     """)
    # for i in ttdb:
    #     logger.debug("Column: " + str(i[0]))

    for data in test:
        jsonData[data.neighborhood_id] = data.serialize()
    return jsonify(jsonData)

@app.route('/api/neighborhoods/<nID>')
def api_neighborhood_spec(nID):
    jsonData = {}

    test = NeighborhoodStats.query.filter_by(neighborhood_id=nID).all()

    if len(test) is 0:
        init_neighborhood_stats(json.load(open('json_data/neighborhood_stats.json')))

    #-----------
    # Debug Code
    #-----------

    # test_str = str(test)
    # logger.info(test_str)

    # ttdb = db.session.execute("""
    #     SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='StateStats'
    #     """)
    # for i in ttdb:
    #     logger.debug("Column: " + str(i[0]))

    for data in test:
        jsonData[data.id] = data.serialize()
    return jsonify(jsonData)


#------
# Tests
#------

@app.route('/tests')
def render_tests():
    """
    runs the tests.py file as a subprocess and saves the output to a test_results variable
    returns a json file containing the test results
    """
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

    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()
    db.create_all()
    init_db()
    db.session.commit()

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
