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
    """
    def make_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
        self.app = app.test_client()
        return app
    """
    #def create_app():
    #    app = Flask(__name__)
    #    db.init_app(app)
    #    return app

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DB_URI
      #  self.app = app.test_client()
  
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    # --------------------
    # State and StateStats
    # --------------------
    def test_add_delete_state(self):
        state1 = State(state_code='TX', state_name='Texas', latitude='31.497160', longitude='-99.358380')
        state2 = State(state_code='CA', state_name='California', latitude='37.261463', longitude='-119.61164')
        state3 = State(state_code='NY', state_name='New York', latitude='42.946097', longitude='-75.507057')
        db.session.add(state1)
        db.session.add(state2)
        db.session.add(state3)
        db.session.commit()

        self.assertEqual(len(State.query.all()), 3)
        db.session.delete(state1)
        db.session.delete(state2)
        db.session.delete(state3)
        db.session.commit()


    
    
    def test_get_all_states(self):
        state1 = State(state_code='TX', state_name='Texas', latitude='31.497160', longitude='-99.358380')
        state2 = State(state_code='CA', state_name='California', latitude='37.261463', longitude='-119.61164')
        state3 = State(state_code='NY', state_name='New York', latitude='42.946097', longitude='-75.507057')
        db.session.add(state1)
        db.session.add(state2)
        db.session.add(state3)
        db.session.commit()
        states = State.query.all()
        self.assertEqual(len(states), 3)
        db.session.delete(state1)
        db.session.delete(state2)
        db.session.delete(state3)
        db.session.commit()



    
    def test_filter_by_latitude(self):
        state1 = State(state_code='TX', state_name='Texas', latitude='31.497160', longitude='-99.358380')
        state2 = State(state_code='CA', state_name='California', latitude='37.261463', longitude='-119.61164')
        state3 = State(state_code='NY', state_name='New York', latitude='42.946097', longitude='-75.507057')
        db.session.add(state1)
        db.session.add(state2)
        db.session.add(state3)
        db.session.commit()
        states = State.query.filter(State.latitude >= 35.0).all()
        assert len(states) == 2
        db.session.delete(state1)
        db.session.delete(state2)
        db.session.delete(state3)
        db.session.commit()


    def test_get_one_state(self):
        state1 = State(state_code='TX', state_name='Texas', latitude='31.497160', longitude='-99.358380')
        state2 = State(state_code='CA', state_name='California', latitude='37.261463', longitude='-119.61164')
        state3 = State(state_code='NY', state_name='New York', latitude='42.946097', longitude='-75.507057')
        db.session.add(state1)
        db.session.add(state2)
        db.session.add(state3)
        db.session.commit()        
        state = State.query.filter_by(state_code = 'CA').all()
        self.assertEqual('California', state[0].state_name)
        db.session.delete(state1)
        db.session.delete(state2)
        db.session.delete(state3)
        db.session.commit()



    
    def test_add_delete_state_stats(self):
        state_stat1 = StateStats(week_of="2016-03-12", property_type="All Properties", num_properties="39109", med_listing_price="277473", avg_listing_price ="389681", state_code='TX')
        state_stat2 = StateStats(week_of="2016-03-12", property_type="1 Bedroom Properties", num_properties="588", med_listing_price="137555", avg_listing_price ="399421", state_code='TX')
        state_stat3 = StateStats(week_of="2016-03-19", property_type="6 Bedroom Properties", num_properties="210", med_listing_price="897450", avg_listing_price ="1752797", state_code='TX')
        state_stat4 = StateStats(week_of="2016-03-19", property_type="13 Bedroom Properties", num_properties="1", med_listing_price="695000", avg_listing_price ="695000", state_code='NY')
        db.session.add(state_stat1)
        db.session.add(state_stat2)
        db.session.add(state_stat3)
        db.session.add(state_stat4)
        db.session.commit()
        assert(len(StateStats.query.all())) == 4
        db.session.delete(state_stat1)
        db.session.delete(state_stat2)
        db.session.delete(state_stat3)
        db.session.delete(state_stat4)
        db.session.commit()

    
    def test_get_one_state_stats(self):
        state_stat1 = StateStats(week_of="2016-03-12", property_type="All Properties", num_properties="39109", med_listing_price="277473", avg_listing_price ="389681", state_code='TX')
        state_stat2 = StateStats(week_of="2016-03-12", property_type="1 Bedroom Properties", num_properties="588", med_listing_price="137555", avg_listing_price ="399421", state_code='TX')
        state_stat3 = StateStats(week_of="2016-03-19", property_type="6 Bedroom Properties", num_properties="210", med_listing_price="897450", avg_listing_price ="1752797", state_code='TX')
        state_stat4 = StateStats(week_of="2016-03-19", property_type="13 Bedroom Properties", num_properties="1", med_listing_price="695000", avg_listing_price ="695000", state_code='NY')
        db.session.add(state_stat1)
        db.session.add(state_stat2)
        db.session.add(state_stat3)
        db.session.add(state_stat4)
        db.session.commit()
        stats = StateStats.query.filter_by(state_code = 'TX').all()
        assert len(stats) == 3
        db.session.delete(state_stat1)
        db.session.delete(state_stat2)
        db.session.delete(state_stat3)
        db.session.delete(state_stat4)
        db.session.commit()

    
    def test_state_stat_filter(self):
        state_stat1 = StateStats(week_of="2016-03-12", property_type="All Properties", num_properties="39109", med_listing_price="277473", avg_listing_price ="389681", state_code='TX')
        state_stat2 = StateStats(week_of="2016-03-12", property_type="1 Bedroom Properties", num_properties="588", med_listing_price="137555", avg_listing_price ="399421", state_code='TX')
        state_stat3 = StateStats(week_of="2016-03-19", property_type="6 Bedroom Properties", num_properties="210", med_listing_price="897450", avg_listing_price ="1752797", state_code='TX')
        state_stat4 = StateStats(week_of="2016-03-19", property_type="13 Bedroom Properties", num_properties="1", med_listing_price="695000", avg_listing_price ="695000", state_code='NY')
        db.session.add(state_stat1)
        db.session.add(state_stat2)
        db.session.add(state_stat3)
        db.session.add(state_stat4)
        db.session.commit()
        stats = StateStats.query.filter_by(property_type = 'All Properties').all()
        assert len(stats) == 1
        db.session.delete(state_stat1)
        db.session.delete(state_stat2)
        db.session.delete(state_stat3)
        db.session.delete(state_stat4)
        db.session.commit()


    

    # ------------------
    # City and CityStats
    # ------------------


    

    def test_add_delete_cities(self):
        city1 = City(city_id="05000", city_name='Austin', state_code='TX', latitude="30.265887", longitude="-97.745876")
        city2 = City(city_id="33805", city_name="Issaquah", state_code="WA", latitude="47.5491680040152", longitude="-122.041373510301")
        city3 = City(city_id="60102", city_name="Redwood City", state_code='CA', latitude="37.4843929647298", longitude="-122.256960646405")
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        db.session.commit()
        assert len(City.query.all()) == 3
        db.session.delete(city1)
        db.session.delete(city2)
        db.session.delete(city3)
        db.session.commit()    



    def test_get_all_cities(self):
        city1 = City(city_id="05000", city_name='Austin', state_code='TX', latitude="30.265887", longitude="-97.745876")
        city2 = City(city_id="33805", city_name="Issaquah", state_code="WA", latitude="47.5491680040152", longitude="-122.041373510301")
        city3 = City(city_id="60102", city_name="Redwood City", state_code='CA', latitude="37.4843929647298", longitude="-122.256960646405")
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        db.session.commit()
        cities = City.query.all()
        assert len(cities) == 3
        db.session.delete(city1)
        db.session.delete(city2)
        db.session.delete(city3)
        db.session.commit()    

    
    def test_get_all_cities_in_state_filter(self):
        city1 = City(city_id="05000", city_name='Austin', state_code='TX', latitude="30.265887", longitude="-97.745876")
        city2 = City(city_id="33805", city_name="Issaquah", state_code="WA", latitude="47.5491680040152", longitude="-122.041373510301")
        city3 = City(city_id="60102", city_name="Redwood City", state_code='CA', latitude="37.4843929647298", longitude="-122.256960646405")
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        db.session.commit()
        cities = City.query.filter_by(state_code = 'TX').all()
        assert len(cities) == 1
        db.session.delete(city1)
        db.session.delete(city2)
        db.session.delete(city3)
        db.session.commit()            

    def test_filter_for_one_city(self):
        city1 = City(city_id="05000", city_name='Austin', state_code='TX', latitude="30.265887", longitude="-97.745876")
        city2 = City(city_id="33805", city_name="Issaquah", state_code="WA", latitude="47.5491680040152", longitude="-122.041373510301")
        city3 = City(city_id="60102", city_name="Redwood City", state_code='CA', latitude="37.4843929647298", longitude="-122.256960646405")
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        db.session.commit()
        cities = City.query.filter_by(city_name = 'Redwood City').all()
        self.assertEqual('Redwood City', cities[0].city_name)
        self.assertEqual('37.4843929647298', cities[0].latitude)
        db.session.delete(city1)
        db.session.delete(city2)
        db.session.delete(city3)
        db.session.commit()            


    def test_wrong_city_input_(self):
        city1 = City(city_id="05000", city_name='Austin', state_code='TX', latitude="30.265887", longitude="-97.745876")
        city2 = City(city_id="33805", city_name="Issaquah", state_code="WA", latitude="47.5491680040152", longitude="-122.041373510301")
        city3 = City(city_id="60102", city_name="Redwood City", state_code='CA', latitude="37.4843929647298", longitude="-122.256960646405")
        db.session.add(city1)
        db.session.add(city2)
        db.session.add(city3)
        db.session.commit()
        city = City.query.filter_by(city_name = 'CA').all()
        self.assertEqual(len(city), 0)
        db.session.delete(city1)
        db.session.delete(city2)
        db.session.delete(city3)
        db.session.commit()            



    
    def test_add_delete_city_stats(self):
        city_stat1 = CityStats(week_of="2016-03-12", property_type="2 Bedroom Properties", num_properties="24", avg_listing_price="1060724", med_listing_price="836857", city_id="60102")
        city_stat2 = CityStats(week_of="2016-03-19", property_type="2 Bedroom Properties", num_properties="5", avg_listing_price="820167", med_listing_price="820000", city_id="60102")
        city_stat3 = CityStats(week_of="2016-03-19", property_type="1 Bedroom Properties", num_properties="93", avg_listing_price="641876", med_listing_price="557450" , city_id="63000")
        city_stat4 = CityStats(week_of="2016-03-12", property_type="6 Bedroom Properties", num_properties="8", avg_listing_price="1430799", med_listing_price="749475",city_id="63000")
        db.session.add(city_stat1)
        db.session.add(city_stat2)
        db.session.add(city_stat3)
        db.session.add(city_stat4)
        db.session.commit()
        assert len(CityStats.query.all()) == 4
        db.session.delete(city_stat1)
        db.session.delete(city_stat2)
        db.session.delete(city_stat3)
        db.session.delete(city_stat4)
        db.session.commit()


    def test_filter_stats_by_date(self):
        city_stat1 = CityStats(week_of="2016-03-12", property_type="2 Bedroom Properties", num_properties="24", avg_listing_price="1060724", med_listing_price="836857", city_id="60102")
        city_stat2 = CityStats(week_of="2016-03-19", property_type="2 Bedroom Properties", num_properties="5", avg_listing_price="820167", med_listing_price="820000", city_id="60102")
        city_stat3 = CityStats(week_of="2016-03-19", property_type="1 Bedroom Properties", num_properties="93", avg_listing_price="641876", med_listing_price="557450" , city_id="63000")
        city_stat4 = CityStats(week_of="2016-03-12", property_type="6 Bedroom Properties", num_properties="8", avg_listing_price="1430799", med_listing_price="749475",city_id="63000")
        db.session.add(city_stat1)
        db.session.add(city_stat2)
        db.session.add(city_stat3)
        db.session.add(city_stat4)
        db.session.commit()
        cityStats = CityStats.query.filter_by(week_of = '2016-03-12').all()
        assert len(cityStats) == 2
        db.session.delete(city_stat1)
        db.session.delete(city_stat2)
        db.session.delete(city_stat3)
        db.session.delete(city_stat4)
        db.session.commit()

    def test_city_stats_filter_by_property_type(self):
        city_stat1 = CityStats(week_of="2016-03-12", property_type="2 Bedroom Properties", num_properties="24", avg_listing_price="1060724", med_listing_price="836857", city_id="60102")
        city_stat2 = CityStats(week_of="2016-03-19", property_type="2 Bedroom Properties", num_properties="5", avg_listing_price="820167", med_listing_price="820000", city_id="60102")
        city_stat3 = CityStats(week_of="2016-03-19", property_type="1 Bedroom Properties", num_properties="93", avg_listing_price="641876", med_listing_price="557450" , city_id="63000")
        city_stat4 = CityStats(week_of="2016-03-12", property_type="6 Bedroom Properties", num_properties="8", avg_listing_price="1430799", med_listing_price="749475",city_id="63000")
        db.session.add(city_stat1)
        db.session.add(city_stat2)
        db.session.add(city_stat3)
        db.session.add(city_stat4)
        db.session.commit()        
        stats = CityStats.query.filter_by(property_type = '2 Bedroom Properties').all()
        assert len(stats) == 2
        db.session.delete(city_stat1)
        db.session.delete(city_stat2)
        db.session.delete(city_stat3)
        db.session.delete(city_stat4)
        db.session.commit()



    # -----------------------------------
    # Neightborhood and NeighborhoodStats
    # -----------------------------------

    def test_add_delete_neighborhood(self):
        neighborhood1 = Neighborhood(neighborhood_id="6146", neighborhood_name='West University', state_code='TX', city_id="05000")
        neighborhood2 = Neighborhood(neighborhood_id="7", neighborhood_name='Twin Peaks', state_code='TX', city_id="0040")
        db.session.add(neighborhood1)
        db.session.add(neighborhood2)
        db.session.commit()
        assert len(Neighborhood.query.all()) == 2
        db.session.delete(neighborhood1)
        db.session.delete(neighborhood2)
        db.session.commit()

    
    def test_get_all_neighborhoods(self):
        neighborhood1 = Neighborhood(neighborhood_id="6146", neighborhood_name='West University', state_code='TX', city_id="05000")
        neighborhood2 = Neighborhood(neighborhood_id="7", neighborhood_name='Twin Peaks', state_code='TX', city_id="0040")
        db.session.add(neighborhood1)
        db.session.add(neighborhood2)
        db.session.commit()
        nb = Neighborhood.query.all()
        self.assertTrue(len(nb) == 2)
        db.session.delete(neighborhood1)
        db.session.delete(neighborhood2)
        db.session.commit()


        
    def test_get_one_neighborhood(self):
        neighborhood1 = Neighborhood(neighborhood_id="6146", neighborhood_name='West University', state_code='TX', city_id="05000")
        neighborhood2 = Neighborhood(neighborhood_id="7", neighborhood_name='Twin Peaks', state_code='TX', city_id="0040")
        db.session.add(neighborhood1)
        db.session.add(neighborhood2)
        db.session.commit()
        nb = Neighborhood.query.filter_by(neighborhood_name = 'West University').all()
        self.assertEqual('West University', nb[0].neighborhood_name)
        db.session.delete(neighborhood1)
        db.session.delete(neighborhood2)
        db.session.commit()



    def test_add_delete_neighborhood_stats(self):
        neighborhood_stat1 = NeighborhoodStats(week_of="2016-03-12", property_type="All Properties", num_properties="1", avg_listing_price="1060724", med_listing_price="1060724", neighborhood_id="7")
        neighborhood_stat2 = NeighborhoodStats(week_of="2016-03-12", property_type="All Properties", num_properties="2", avg_listing_price="1060724", med_listing_price="1000724", neighborhood_id="6146")
        db.session.add(neighborhood_stat1)
        db.session.add(neighborhood_stat2)
        db.session.commit()
        self.assertEqual(len(NeighborhoodStats.query.all()), 2)        
        db.session.delete(neighborhood_stat1)
        db.session.delete(neighborhood_stat2)
        db.session.commit()


    
    def test_filter_get_one_neighborhood_stats(self):
        neighborhood_stat1 = NeighborhoodStats(week_of="2016-03-12", property_type="All Properties", num_properties="1", avg_listing_price="1060724", med_listing_price="1060724", neighborhood_id="7")
        neighborhood_stat2 = NeighborhoodStats(week_of="2016-03-12", property_type="All Properties", num_properties="2", avg_listing_price="1060724", med_listing_price="1000724", neighborhood_id="6146")
        db.session.add(neighborhood_stat1)
        db.session.add(neighborhood_stat2)
        db.session.commit()
        nbs = NeighborhoodStats.query.filter_by(neighborhood_id = 7).all()
        self.assertTrue(len(nbs) == 1)
        db.session.delete(neighborhood_stat1)
        db.session.delete(neighborhood_stat2)
        db.session.commit()


    
    def test_remove_neighborhood_stats(self):
        neighborhood_stat1 = NeighborhoodStats(week_of="2016-03-12", property_type="All Properties", num_properties="1", avg_listing_price="1060724", med_listing_price="1060724", neighborhood_id="7")
        neighborhood_stat2 = NeighborhoodStats(week_of="2016-03-12", property_type="All Properties", num_properties="2", avg_listing_price="1060724", med_listing_price="1000724", neighborhood_id="6146")
        db.session.add(neighborhood_stat1)
        db.session.add(neighborhood_stat2)
        db.session.commit()
        NeighborhoodStats.query.filter_by(neighborhood_id = 7).delete()
        db.session.commit()
        assert len( NeighborhoodStats.query.all()) == 1
        db.session.delete(neighborhood_stat2)
        db.session.commit()
        
    



# ----
# Main
# ----

if __name__ == '__main__' :
    main()
