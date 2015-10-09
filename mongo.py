__author__ = 'gj'

from pymongo import MongoClient


class FplManager(object):
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

    def close_connection(self):
        self.client.close()
