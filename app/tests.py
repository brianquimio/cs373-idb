#!/usr/bin/env python3

# -------------------------------
# Copyright (C) 2016
# Virtual_Address IDB
# -------------------------------

# -------
# Imports
# -------

from app            import *
from io             import StringIO
from urllib.request import urlopen
from unittest       import main, TestCase



TEST_DB_URI = "sqlite:////tmp/test.db"
# TEST_DB_URI = "mysql://guestbook-admin:my-guestbook-admin-password@localhost/testdb"

class TestModels (TestCase):

    #----------------------
    # DB setup and teardown
    #----------------------
    
    def make_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        self.app = app.test_client()
        return app
    
    def setUp(self):
        """
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        self.app = app.test_client()
        """

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    # --------------------
    # State and StateStats
    # --------------------

    def test_add_state(self):
        state1 = State(state_code='TX', state_name='Texas', latitude='31.497160', longitude='-99.358380')
        state2 = State(state_code='CA', state_name='California', latitude='37.261463', longitude='-119.61164')
        state3 = State(state_code='NY', state_name='New York', latitude='42.946097', longitude='-75.507057')
        db.session.add(state1)
        db.session.add(state2)
        db.session.add(state3)
        db.session.commit()
        assert(State.query.all()) == 3 


    def test_get_all_states(self):
        states = State.query.all()
        assert len(states) == 4

    def test_filter_by_latitude(self):
        states = State.query.filter_by(latitude > 35.0)
        assert len(states) == 3

    def test_get_one_state(self):
        state = State.query.filter_by(state_code = 'CA').all()
        self.assertEqual('California', state.state_name)

    """
    def test_state_4(self):
        state = State.query.filter_by(state_name = 'Texas').all()
        self.assertEqual("Texas", state.state_code)
    def test_state_5(self):
        state = State.query.filter_by(latitude = '42.946097').all()
        self.assertTrue(state.state_code == 'TX' and state.state_name == 'New York')
    """ 

    def test_add_state_stats(self):
        state_stat1 = StateStats("2016-03-12", "All Properties", "39109", "277473", "389681", 'TX')
        state_stat2 = StateStats("2016-03-12", "1 Bedroom Properties", "588", "137555", "399421", 'TX')
        state_stat3 = StateStats("2016-03-19", "6 Bedroom Properties", "210", "897450", "1752797", 'TX')
        state_stat4 = StateStats("2016-03-19", "13 Bedroom Properties", "1", "695000", "695000", 'NY')
        db.session.add(state_stat1)
        db.session.add(state_stat2)
        db.session.add(state_stat3)
        db.session.add(state_stat4)
        db.session.commit()
        assert(StateStats.query.all()) == 4

    def test_get_one_state_stats(self):
        stats = StateStats.query.filter_by(state_code = 'TX').all()
        assert len(stats) == 3

    def test_state_stat_filter(self):
        stats = StateStats.query.filter_by(property_type = 'All Properties')
        assert stats == 1

    def test_delete_state_stats(self):
        StateStats.query.filter_by(state_code = 'NY').delete()
        db.session.commit()
        assert len(StateStats.query.all()) == 3


    # ------------------
    # City and CityStats
    # ------------------

    def test_add_cities(self):
        city1 = City("05000", 'Austin', 'TX', "30.265887", "-97.745876")
        city2 = City("33805", "Issaquah", "WA", "47.5491680040152", "-122.041373510301")
        city3 = City("60102", "Redwood City", 'CA', "37.4843929647298", "-122.256960646405")
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        db.session.commit()
        assert len(City.query.all()) == 3

    def test_get_all_cities(self):
        cities = City.query.all()
        assert len(cities) == 3

    def test_get_all_cities_in_state_filter(self):
        cities = City.query.filter_by(state_code = 'TX').all()
        assert len(cities) == 1

    def test_filter_for_one_city(self):
        cities = City.query.filter_by(city_name = 'Redwood City').all()
        self.assertEqual('Redwood City', cities.city_name)
        self.assertEqal('37.4843929647298', cities.latitude)

    def test_wrong_city_input_(self):
        city = City.query.filter_by(city_name = 'CA').all()
        self.assertTrue(city is None)

    def test_add_city_stats(self):
        city_stat1 = CityStats("2016-03-12", "All Properties", "24", "1060724", "836857", "60102")
        city_stat2 = CityStats("2016-03-19", "2 Bedroom Properties", "5", "820167", "820000", "60102")
        city_stat3 = CityStats("2016-03-19", "1 Bedroom Properties", "93", "641876", "557450" , "63000")
        city_stat4 = CityStats("2016-03-12", "6 Bedroom Properties", "8", "1430799", "749475", "63000")
        db.session.add(city_stat1)
        db.session.add(city_stat2)
        db.session.add(city_stat3)
        db.session.add(city_stat4)
        db.session.commit()
        assert len(CityStats.query.all()) == 4

    def test_filter_stats_by_date(self):
        cityStats = City.query.filter_by(week_of = '2016-03-12').all()
        assert len(cityStats) == 2

    def test_delete_city_stats(self):
        CityStats.query.filter_by(property_type = '6 Bedroom Properties').delete()
        db.session.commit()
        assert len(CityStats.query.all()) == 3




    # -----------------------------------
    # Neightborhood and NeighborhoodStats
    # -----------------------------------

    def test_add_neighborhood(self):
        neighborhood1 = Neighborhood("6146", 'West University', 'TX', "05000")
        neighborhood2 = Neighborhood("7", 'Twin Peaks', 'TX', "0040")
        db.session.add(neighborhood1)
        db.session.add(neighborhood2)
        db.session.commit()
        assert len(Neighborhood.query.all()) == 2

    def test_get_all_neighborhoods(self):
        nb = Neighborhood.query.all()
        self.assertTrue(len(nb) == 2)

    def test_get_one_neighborhood(self):
        nb = Neighborhood.query.filter_by(neighborhood_name = 'West University')
        self.assertEqual('West University', nb.neighborhood_name)
    
    """
    def test_neighborhood_3(self):
        nb = Neighborhood.query.filter_by(neighborhood_id = 7)
        self.assertEqual('Twin Peaks', nb.neighborhood_name)
    def test_neighborhood_4(self):
        nb = Neighborhood.query.filter_by(city_id = 4)
        self.assertEqual('West University', nb.neighborhood_name)
    """

    def test_add_neighborhood_stats(self):
        neighborhood_stat1 = NeighborhoodStats("2016-03-12", "All Properties", "1", "1060724", "1060724", "7")
        neighborhood_stat2 = NeighborhoodStats("2016-03-12", "All Properties", "2", "1060724", "1000724", "6146")

        db.session.add(neighborhood_stat1)
        db.session.commit()
        assert len( NeighborhoodStats.query.all()) == 2        

    def test_filter_get_one_neighborhood(self):
        nbs = NeighborhoodStats.query.filter_by(neighborhood_id = 7)
        self.assertTrue(len(nbs) == 1)

    def test_remove_neighborhood(self):
        NeighborhoodStats.query.filter_by(neighborhood_id = 7).delete()
        db.session.commit()
        assert len( NeighborhoodStats.query.all()) == 1



# ----
# Main
# ----

if __name__ == '__main__' :
    main()
