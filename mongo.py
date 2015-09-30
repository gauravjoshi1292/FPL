__author__ = 'gj'

import json
from pymongo import MongoClient


def create_database():
    client = MongoClient('localhost', 27017)
    db = client['fpl']
    collection = db['stats']

    with open('stats.json', 'r') as infile:
        data = json.load(infile)

    collection.insert(data)


def query_database():
    client = MongoClient('localhost', 27017)
    db = client['fpl']
    collection = db['stats']

    collection.find()


create_database()

