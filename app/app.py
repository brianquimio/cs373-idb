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
    # logger.debug("about")
    return send_file('templates/about.html')



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
