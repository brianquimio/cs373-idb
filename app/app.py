

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




# -------
# Run App
# -------

if __name__ == '__main__':
    app.run('0.0.0.0')
