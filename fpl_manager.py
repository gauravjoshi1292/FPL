__author__ = 'gj'

import pymongo

from mongo import DbManager
from urls import MONGODB_URL
from global_variables import PLAYERS_DB


class FplManager(object):
    def __init__(self):
        self.db_manager = DbManager(MONGODB_URL)

    def get_top_goalkeepers(self, n):
        return self.db_manager.find(PLAYERS_DB, 'goalkeepers',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_defenders(self, n):
        return self.db_manager.find(PLAYERS_DB, 'defenders',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_midfielders(self, n):
        return self.db_manager.find(PLAYERS_DB, 'midfielders',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_forwards(self, n):
        return self.db_manager.find(PLAYERS_DB, 'forwards',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_last_five_results(self, team):
        results = self.db_manager.find(PLAYERS_DB, 'results',
                                       {'$or': [{'home_team': team}, {'away_team': team}]})
        for r in results:
            print r


if __name__ == '__main__':
    fpl_manager = FplManager()
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_goalkeepers(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_defenders(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_midfielders(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_forwards(5)]
    fpl_manager.get_last_five_results('ARS')
