

# -------
# Imports
# -------

import logging
import os
import Models

from flask import Flask, render_template, request, redirect, url_for
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy


# ------------------------------
# Configure logger for debugging
# ------------------------------

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(levelname)s: %(message)s')
# logger = logging.getLogger(__name__)
# logger.debug("Welcome to the Virtual Address Space")


# -------------------------------------------
# Configure MySQL Database and SQLAlchemy URI
# -------------------------------------------

SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@hostname}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        hostname=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DATABASE'))


# -------------
# Configure app
# -------------

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
# db = SQLAlchemy(app)


# -----------
# URL Routing
# -----------

@app.route('/')
def index():
    # logger.debug("index")
    return render_template('index.html')

@app.route('/showCities')
def showCities():
    # logger.debug("cities")
    return render_template('cities.html')

@app.route('/showStates')
def showCities():
    # logger.debug("cities")
    return render_template('states.html')

@app.route('/showNeighborhoods')
def showCities():
    # logger.debug("cities")
    return render_template('neighborhoods.html')


# ---------------------
# Commands for database
# ---------------------

# @manager.command
# def create_db():
#     logger.debug("create_db")
#     app.config['SQLALCHEMY_ECHO'] = True
#     db.create_all()

# @manager.command
# def create_dummy_data():
#     logger.debug("create_test_data")
#     app.config['SQLALCHEMY_ECHO'] = True
#     guest = Guest(name='Steve')
#     db.session.add(guest)
#     db.session.commit()

# @manager.command
# def drop_db():
#     logger.debug("drop_db")
#     app.config['SQLALCHEMY_ECHO'] = True
#     db.drop_all()



# -------
# Run App
# -------

if __name__ == '__main__':
    manager.run()
