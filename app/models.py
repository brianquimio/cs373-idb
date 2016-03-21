# -------
# Imports
# -------

from flask.ext.sqlalchemy import SQLAlchemy


# -----------
# URL Routing
# -----------

class City(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(256), nullable=False)
    state_name = db.Column(db.String(256), nullable=False, foreign_key=True)

    def __repr__(self):
        return "[City: city_id={}, city_name={}, state_name={}]".format(self.city_id, self.city_name, self.state_name)

class State(db.Model):
	__tablename__ = 'states'

	 state_name = db.Column(db.String(256), primary_key=True)

	 def __repr__(self):
        return "[State: state_name={}]".format(self.state_name)

class Neighborhood(db.Model):
	__tablename__ = 'neighborhoods'

	neighborhood_id = db.Column(db.Integer, primary_key=True)
	neighborhood_name = db.Column(db.Integer, primary_key=True)

	def __repr__(self):
		return "[Neighborhood: neighborhood_id={}, neighborhood_name={}".format(self.neighborhood_id, self.neighborhood_name)
