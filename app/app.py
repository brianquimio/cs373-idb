#!/usr/local/bin/python

# -------
# Imports
# -------

import os
import subprocess
from db import app, db, manager, logger
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from models import State, StateStats, City, CityStats, Neighborhood, NeighborhoodStats
from create_db import *


# -----------
# URL Routing
# -----------

@app.route('/')
def splash():
    logger.debug("splash")
    return send_file('templates/index.html')

@app.route('/about.html')
def about():
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
                            }
        return jsonify(data)


@app.route('/api/state/')
def api_state_all():
    jsonData = {}
    for data in State.query:
        jsonData[data.name] = data.serialize()
    return jsonify(jsonData)

@app.route('/api/state/<statecode>')
def api_state_spec(statecode):
    statedata = State.query.get(statecode)
    return jsonify(statedata.serialize())


@app.route('/api/cities/')
def api_cities_all():
    jsonData = {}
    for data in City.query:
        jsonData[data.name] = data.serialize()
    return jsonify(jsonData)

@app.route('/api/cities/<cityID>')
def api_state_spec(cityID):
    citydata = City.query.get(cityID)
    return jsonify(citydata.serialize())

@app.route('/api/neighborhoods/')
def api_cities_all():
    jsonData = {}
    for data in Neighborhood.query:
        jsonData[data.name] = data.serialize()
    return jsonify(jsonData)

@app.route('/api/cities/<nID>')
def api_state_spec(cityID):
    nData = Neighborhood.query.get(nID)
    return jsonify(nData.serialize())


#------
# Tests
#------

@app.route('/tests')
def render_tests():
    # logger.debug("create_db")
    test_results = subprocess.getoutput("python3 tests.py")
    return json.dumps({'test_results': str(test_results)})


# ----------------
# Manager Commands
# ----------------

@manager.command
def create_db():
    # logger.debug("create_db")
    app.config['SQLALCHEMY_ECHO'] = True
    init_db()

@manager.command
def drop_db():
    # logger.debug("drop_db")
    app.config['SQLALCHEMY_ECHO'] = True
    db.drop_all()

# -------
# Run App
# -------

if __name__ == '__main__':
    manager.run()
    manager.create_db()

