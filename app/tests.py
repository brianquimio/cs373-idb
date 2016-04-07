#!/usr/bin/env python3

# -------------------------------
# Copyright (C) 2016
# Virtual_Address IDB
# -------------------------------

# -------
# Imports
# -------

from app            import db, app
from io             import StringIO
from urllib.request import urlopen
from unittest       import main, TestCase
from models         import *
import json


TEST_DB_URI = "sqlite://"

# -----
# State
# -----

class TestState (TestCase):

    def make_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        return app

    def setUp(self):
        db.create_all()
        state1 = State(1, '3-23-2016', 'TX', 'All Properties', 29876, 500000)
        state2 = State(2, '3-23-2016', 'CA', 'All Properties', 36309, 759071)
        state3 = State(3, '3-23-2016', 'NY', 'All Properties', 765432, 1203843)
        db.session.add(state1)
        db.session.add(state2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_state_1(self):
        states = State.query.all()
        self.assertTrue(len(states) == 3)

    def test_state_2(self):
        states = State.query.filter_by(state_id > 1)
        self.assertTrue(len(states) == 2)

    def test_state_3(self):
        state = State.query.filter_by(state_id = 2)
        self.assertEqual('CA', state.state_name)

    def test_state_4(self):
        state = State.query.filter_by(state_name = 'TX')
        self.assertEqual(1, state.state_id)

    def test_state_5(self):
        state = State.query.filter_by(date = '3-23-2016', avg_listing_price = 500000)
        self.assertTrue(state.state_id == 1 and state.num_properties == 29876)


# ----
# City
# ----

class TestCity (TestCase):

    def make_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        return app

    def setUp(self):
        db.create_all()
        city1 = City(4, '3-23-2016', 'Austin', 'All Properties', 1234, 500000, 1)
        city2 = City(5, '3-23-2016', 'San Antonio', 'All Properties', 2345, 400000, 1)
        city3 = City(6, '3-23-2016', 'San Francisco', 'All Properties', 4321, 1600000, 2)
        db.session.add(city1)
        db.session.add(city2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_city_1(self):
        cities = City.query.all()
        self.assertTrue(len(cities) == 3)

    def test_city_2(self):
        cities = City.query.filter_by(state_id == 1)
        self.assertTrue(len(cities) == 2)

    def test_city_3(self):
        cities = City.query.filter_by(state_id == 1)
        self.assertEqual('Austin', cities[0].city_name)

    def test_city_4(self):
        city = City.query.filter_by(city_id == 3)
        self.assertTrue(city is None)


# -------------
# Neightborhood
# -------------

class TestNeighborhood (TestCase):

    def make_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        return app

    def setUp(self):
        db.create_all()
        neighborhood1 = Neighborhood(6, '3-23-2016', 'West University', 'All Properties', 500, 700000, 4, 1)
        neighborhood2 = Neighborhood(7, '3-23-2016', 'Twin Peaks', 'All Properties', 1110, 2000000, 6, 2)
        db.session.add(neighborhood1)
        db.session.add(neighborhood2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_neighborhood_1(self):
        nb = Neighborhood.query.all()
        self.assertTrue(len(nb) == 2)

    def test_neighborhood_2(self):
        nb = Neighborhood.query.filter_by(neighborhood_name = 'West University')
        self.assertEqual('West University', nb.neighborhood_name)

    def test_neighborhood_3(self):
        nb = Neighborhood.query.filter_by(neighborhood_id = 7)
        self.assertEqual('Twin Peaks', nb.neighborhood_name)

    def test_neighborhood_4(self):
        nb = Neighborhood.query.filter_by(city_id = 4)
        self.assertEqual('West University', nb.neighborhood_name)

# -------------
# State Parks
# -------------

# class TestStateParks (TestCase):

#     def make_app(self):
#         app.config['TESTING'] = True
#         app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
#         return app

#     def setUp(self):
#         db.create_all()
#         park1 = Neighborhood(CA)
#         park2 = Neighborhood(CO)
#         db.session.add(neighborhood1)
#         db.session.add(neighborhood2)
#         db.session.commit()


# ----
# Main
# ----

if __name__ == '__main__' :
    main()