__author__ = 'gj'

import pymongo

from urls import *
from global_variables import *
from mongo import DbManager


class FplManager(object):
    def __init__(self):
        self.db_manager = DbManager(MONGODB_URL)

    def get_top_goalkeepers(self, n):
        return self.db_manager.find(DB_NAME, 'goalkeepers',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_defenders(self, n):
        return self.db_manager.find(DB_NAME, 'defenders',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_midfielders(self, n):
        return self.db_manager.find(DB_NAME, 'midfielders',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_forwards(self, n):
        return self.db_manager.find(DB_NAME, 'forwards',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)


if __name__ == '__main__':
    fpl_manager = FplManager()
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_goalkeepers(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_defenders(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_midfielders(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_forwards(n=5)]
