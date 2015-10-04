__author__ = 'gj'

import json
from pymongo import MongoClient


class FplDatabaseManager(object):
    def __init__(self, uri, db_name, collection_names):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        for name in collection_names:
            _ = self.db[name]

    def insert(self, collection_name, data):
        self.db[collection_name].insert(data)


with open('stats.json', 'r') as infile:
    data = json.load(infile)

db_manager = FplDatabaseManager(uri='mongodb://localhost:27017',
                                db_name='fpl',
                                collection_names=['goalkeepers', 'defenders',
                                                  'midfielders', 'forwards'])

for key, player_stats in data.items():
    db_manager.insert(collection_name=key, data=player_stats)

query = db_manager.db['goalkeepers'].find({'name': 'Adrian'})

for doc in query:
    print doc
