

# -------
# Imports
# -------

import logging
import os
from flask import Flask, render_template, request, redirect, url_for, send_file


# ------------------------------
# Configure logger for debugging
# ------------------------------


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

# -------------
# Configure app
# -------------

app = Flask(__name__)



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


# -------
# Run App
# -------

if __name__ == '__main__':
    app.run('0.0.0.0')
