from flask import Flask
import logging
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Server
import os

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

print("===================================================")
print(os.getenv('MYSQL_DATABASE'))
print(os.getenv('MYSQL_PASSWORD'))
print(os.getenv('MYSQL_USER'))
print(os.getenv('MYSQL_HOST'))
SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        # engine='mysql+pymysql',
        username=os.getenv('MYSQL_USER'),
        # username='vas_admin',
        password=os.getenv('MYSQL_PASSWORD'),
        # password='my-random-password',
        hostname=os.getenv('MYSQL_HOST'),
        # hostname='cs373-idb_db',
        database=os.getenv('MYSQL_DATABASE')
        # database='guestbook'
        )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True))
db = SQLAlchemy(app)