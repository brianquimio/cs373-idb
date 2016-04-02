

# -------
# Imports
# -------

import logging
import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from models import *


# ------------------------------
# Configure logger for debugging
# ------------------------------

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Welcome to Carina Guestbook")

# -------------
# Configure app
# -------------

SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        hostname=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DATABASE'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
db = SQLAlchemy(app)


# -----------
# URL Routing
# -----------


@app.route('/index.html')
@app.route('/')
def index():
    # logger.debug("index")
    return send_file('templates/index.html')

@app.route('/about.html')
def about():
    # logger.debug("about")
    return send_file('templates/about.html')

@app.route('/static-cities.html')
def cities():
    # logger.debug("cities")
    return send_file('templates/static-cities.html')

@app.route('/static-neighborhoods.html')
def neighborhoods():
    # logger.debug("neighborhoods")
    return send_file('templates/static-neighborhoods.html')

@app.route('/static-state-california.html')
def california():
    # logger.debug("california")
    return send_file('templates/static-state-california.html')

@app.route('/static-state-texas.html')
def texas():
    # logger.debug("texas")
    return send_file('templates/static-state-texas.html')

@app.route('/static-states.html')
def states():
    # logger.debug("states")
    return send_file('templates/static-states.html')

@app.route('/static-city-austin-tx.html')
def austin():
    # logger.debug("splash")
    return send_file('templates/static-city-austin-tx.html')

@app.route('/static-city-dallas-tx.html')
def dallas():
    # logger.debug("cities")
    return send_file('templates/static-city-dallas-tx.html')

@app.route('/static-city-houston-tx.html')
def houston():
    # logger.debug("neighborhoods")
    return send_file('templates/static-city-houston-tx.html')

@app.route('/static-neighborhood-hyde-park-austin-tx.html')
def hyde_park():
    # logger.debug("california")
    return send_file('templates/static-neighborhood-hyde-park-austin-tx.html')

@app.route('/static-neighborhood-north-university-austin-tx.html')
def north_university():
    # logger.debug("texas")
    return send_file('templates/static-neighborhood-north-university-austin-tx.html')

@app.route('/static-neighborhood-west-campus-austin-tx.html')
def west_campus():
    # logger.debug("texas")
    return send_file('templates/static-neighborhood-west-campus-austin-tx.html')

@app.route('/static-state-new-york.html')
def new_york():
    # logger.debug("texas")
    return send_file('templates/static-state-new-york.html')


# ----------------
# Manager Commands
# ----------------

@manager.command
def create_db():
    # logger.debug("create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.create_all()

@manager.command
def drop_db():
    logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()

# -------
# Run App
# -------

if __name__ == '__main__':
    manager.run()
