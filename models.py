# -------
# Imports
# -------

from flask.ext.sqlalchemy import SQLAlchemy


# -----------
# DB models
# -----------

class State(db.Model):
    __tablename__ = 'State'

	# Dimensions
    state_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    state_name = db.Column(db.String(256), unique=True)
    property_type = db.Column(db.String(256))

    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)

    	
    def __repr__(self):
        return "[State: state_id={}, state_name={}]".format(self.state_id, self.state_name)

class City(db.Model):
    __tablename__ = 'City'

    # Dimensions
    city_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    city_name = db.Column(db.String(256), nullable=False)
    property_type = db.Column(db.String(256))

    # Measures
    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)

    # Relationships
    state_id = db.Column(db.Integer, db.ForeignKey('State.state_id'))


    def __repr__(self):
        return "[City: city_id={}, city_name={}, state_name={}]".format(self.city_id, self.city_name, self.state_name)

class Neighborhood(db.Model):
    __tablename__ = 'Neighborhood'

	# Dimensions
    neighborhood_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    neighborhood_name = db.Column(db.Integer, nullable=False)

	# Measures
    num_properties = db.Column(db.Integer)
    avg_listing_price = db.Column(db.Integer)

    # Relationships
    state_id = db.Column(db.Integer, db.ForeignKey('State.state_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('City.city_id'))


    def __repr__(self):
        return "[Neighborhood: neighborhood_id={}, neighborhood_name={}".format(self.neighborhood_id, self.neighborhood_name)
