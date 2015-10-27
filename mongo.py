__author__ = 'gj'

from pymongo import MongoClient

from urls import MONGODB_URL
from global_variables import GW_DB, RESULTS_DB

from crawlers.players_crawler import insert_player_stats_in_db
from crawlers.teams_crawler import insert_team_stats_in_db
from crawlers.results_crawler import insert_results_in_db
from crawlers.injuries_crawler import insert_injuries_in_db
from crawlers.gw_results_and_fixtures_crawler import insert_gameweek_fixtures_and_results_in_db


class DbManager(object):
    def __init__(self, uri):
        self.client = MongoClient(uri)

    def create_db(self, db_name):
        _ = self.client[db_name]

    def create_dbs(self, db_names):
        for name in db_names:
            _ = self.client[name]

    def create_collection(self, db_name, collection_name):
        _ = self.client[db_name][collection_name]

    def create_collections(self, db_name, collection_names):
        for name in collection_names:
            _ = self.client[db_name][name]

    def drop_db(self, db_name):
        self.client.drop_database(db_name)

    def insert(self, db_name, collection_name, data):
        self.client[db_name][collection_name].insert(data)

    def find(self, db_name, collection_name, query):
        return self.client[db_name][collection_name].find(query)

    def find_one(self, db_name, collection_name, query):
        return self.client[db_name][collection_name].find_one(query)

    def close_connection(self):
        self.client.close()


if __name__ == "__main__":
    db_manager = DbManager(MONGODB_URL)

    # db_manager.drop_db(GW_DB)
    # db_manager.drop_db(RESULTS_DB)
    #
    # db_manager.create_db(GW_DB)
    # db_manager.create_db(RESULTS_DB)
    #
    # insert_player_stats_in_db(db_manager)
    # insert_team_stats_in_db(db_manager)
    # insert_results_in_db(db_manager)
    # insert_injuries_in_db(db_manager)
    # insert_gameweek_fixtures_and_results_in_db(db_manager)

    print db_manager.client.database_names()
    print db_manager.find_one(GW_DB, 'goalkeepers', {'name': 'Cech'})
    print db_manager.find_one(GW_DB, 'teams', {'team': 'ARS'})
    print db_manager.find_one(RESULTS_DB, 'Arsenal', {'opposition': 'Everton'})
    print db_manager.find_one(GW_DB, 'injuries', {'team': 'LIV'})
    print db_manager.find_one(GW_DB, 'gw_results', {})
    print db_manager.find_one(GW_DB, 'gw_fixtures', {})
