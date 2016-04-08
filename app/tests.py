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
        state1 = State(1, 'TX', 'Texas', '13.004', '17.112')
        state2 = State(2, 'CA', 'California', '12.006', '15.112')
        state3 = State(3, 'NY', 'New York ', '10.004', '19.112')
        db.session.add(state1)
        db.session.add(state2)
        db.session.add(state3)
        stat1 = StateStats('03-01-16', '1-bedroom', 9, 12345, 12000)
        stat2 = StateStats('03-01-16', '2-bedroom', 6, 11111, 12000)
        stat3 = StateStats('03-01-16', '3-bedroom', 3, 15678, 16000)
        db.session.add(stat1)
        db.session.add(stat2)
        db.session.add(stat3)
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
        self.assertEqual('California', state.state_name)

    def test_state_4(self):
        state = State.query.filter_by(state_name = 'TX')
        self.assertEqual(1, state.state_id)

    def test_state_5(self):
        state = State.query.filter_by(latitude = '10.004')
        self.assertTrue(state.state_id == 3 and state.state_name == 'New York')

    def test_state_stat_1(self):
        stat = StateStats.query.filter_by(property_type = '1-bedroom')
        self.assertEqual(9, stat.num_properties)



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
        city1 = City(4, 'Austin', 'TX', '12.34', '5.123')
        city2 = City(5, 'San Antonio', 'TX', '2.345', '4.000')
        city3 = City(6, 'San Francisco', 'TX', '4.321', '16.000')
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_city_1(self):
        cities = City.query.all()
        self.assertTrue(len(cities) == 3)

    def test_city_2(self):
        cities = City.query.filter_by(state_code == 'TX')
        self.assertTrue(len(cities) == 2)

    def test_city_3(self):
        cities = City.query.filter_by(state_code == 'TX')
        self.assertEqual('Austin', cities[0].city_name)

    def test_city_4(self):
        city = City.query.filter_by(city_code == 'NY')
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
        neighborhood1 = Neighborhood(6, 'West University', 'TX', 4)
        neighborhood2 = Neighborhood(7, 'Twin Peaks', 'TX', 4)
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


# ----
# Main
# ----

if __name__ == '__main__' :
    main()