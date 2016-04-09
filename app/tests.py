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


TEST_DB_URI = "sqlite://"

class TestModels (TestCase):

    #----------------------
    # DB setup and teardown
    #----------------------

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
        state_stat1 = StateStats('03-01-2016', '1-bedroom', 9, 12345, 12000, 'TX')
        state_stat2 = StateStats('03-01-2016', '2-bedroom', 6, 11111, 12000, 'TX')
        state_stat3 = StateStats('03-01-2016', '3-bedroom', 3, 15678, 16000, 'TX')
        state_stat4 = StateStats('03-01-2016', '1-bedroom', 11, 17698, 18000, 'NY')
        db.session.add(state_stat1)
        db.session.add(state_stat2)
        db.session.add(state_stat3)
        db.session.add(state_stat4)
        city1 = City(4, 'Austin', 'TX', '12.34', '5.123')
        city2 = City(5, 'San Antonio', 'TX', '2.345', '4.000')
        city3 = City(6, 'San Francisco', 'TX', '4.321', '16.000')
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        city_stat1 = CityStats('04-01-2016', 'TX', '1-bedroom', 10, 10000, 15000, 4)
        city_stat2 = CityStats('04-01-2016', 'TX', '2-bedroom', 11, 11000, 16000, 4)
        city_stat3 = CityStats('04-01-2016', 'TX', '3-bedroom', 9, 12000, 17000, 4)
        city_stat4 = CityStats('04-01-2016', 'TX', '1-bedroom', 5, 14900, 15000, 5)
        db.session.add(city_stat1)
        db.session.add(city_stat2)
        db.session.add(city_stat3)
        db.session.add(city_stat4)
        neighborhood1 = Neighborhood(6, 'West University', 'TX', 4)
        neighborhood2 = Neighborhood(7, 'Twin Peaks', 'TX', 4)
        db.session.add(neighborhood1)
        db.session.add(neighborhood2)
        neighborhood_stat1 = NeighborhoodStats('01-31-16', 6, '1-bedroom', 50, 11111, 10000)
        db.session.add(neighborhood_stat1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    # --------------------
    # State and StateStats
    # --------------------

    def test_state_1(self):
        states = State.query.all()
        self.assertTrue(len(states) == 4)

    def test_state_2(self):
        states = State.query.filter_by(state_id > 1)
        self.assertTrue(len(states) == 3)

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
        stats = StateStats.query.filter_by(property_type = '1-bedroom')
        self.assertEqual(11, stats[1].num_properties)

    def test_state_stat_2(self):
        stats = StateStats.query.filter_by(state_code = 'TX')
        self.assertEqual(3, len(stats))

    def test_state_stat_3(self):
        stats = StateStats.query.filter_by(state_code = 'TX')
        self.assertEqual(3, stats[2].num_properties)


    # ------------------
    # City and CityStats
    # ------------------

    def test_city_1(self):
        cities = City.query.all()
        self.assertTrue(len(cities) == 4)

    def test_city_2(self):
        cities = City.query.filter_by(state_code == 'TX')
        self.assertTrue(len(cities) == 3)

    def test_city_3(self):
        cities = City.query.filter_by(state_code == 'TX')
        self.assertEqual('Austin', cities[0].city_name)

    def test_city_4(self):
        city = City.query.filter_by(city_code == 'CA')
        self.assertTrue(city is None)

    def test_citystats_1(self):
        stats = CityStats.query.filter_by(state_code = 'TX')
        self.assertTrue(len(stats) == 4)

    def test_citystats_2(self):
        stats = CityStats.query.filter_by(state_code = 'TX')
        self.assertEqual(11, stats[1].num_properties)

    def test_citystats_3(self):
        stats = CityStats.query.filter_by(state_code = 'TX')
        self.assertEqual(12000, stats[2].avg_listing_price)


    # -----------------------------------
    # Neightborhood and NeighborhoodStats
    # -----------------------------------

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

    def test_neighborhood_stats_1(self):
        nbs = NeighborhoodStats.query.filter_by(neighborhood_id = 6)
        self.assertTrue(len(nbs) == 1)

    def test_neighborhood_stats_2(self):
        nbs = NeighborhoodStats.query.filter_by(neighborhood_id = 6)
        self.assertEqual(50, nbs.num_properties)

    def test_neighborhood_stats_3(self):
        nbs = NeighborhoodStats.query.filter_by(neighborhood_id = 6)
        self.assertEqual(10000, nbs.avg_listing_price)


# ----
# Main
# ----

if __name__ == '__main__' :
    main()
