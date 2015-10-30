__author__ = 'gj'

import pymongo

from mongo import DbManager
from urls import MONGODB_URL
from global_variables import GW_DB, RESULTS_DB


class QueryHandler(object):
    def __init__(self):
        self.db_manager = DbManager(MONGODB_URL)

    def get_top_goalkeepers(self, n):
        return self.db_manager.find(GW_DB, 'goalkeepers',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_defenders(self, n):
        return self.db_manager.find(GW_DB, 'defenders',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_midfielders(self, n):
        return self.db_manager.find(GW_DB, 'midfielders',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_top_forwards(self, n):
        return self.db_manager.find(GW_DB, 'forwards',
                                    {}).sort('round_score', pymongo.DESCENDING).limit(n)

    def get_last_n_results(self, team, n, opposition=None, place=None, comp=None):
        query = {}
        if place:
            query['place'] = place
        if opposition:
            query['opposition'] = opposition
        if comp:
            query['comp'] = comp

        return self.db_manager.find(RESULTS_DB, team, query).sort('time', pymongo.DESCENDING).limit(n)


if __name__ == '__main__':
    fpl_manager = QueryHandler()
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_goalkeepers(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_defenders(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_midfielders(5)]
    print [(g['name'], g['round_score']) for g in fpl_manager.get_top_forwards(5)]
    print [r for r in fpl_manager.get_last_n_results('Arsenal', 5)]
    print [r for r in fpl_manager.get_last_n_results('Arsenal', 5, 'home')]
    print [r for r in fpl_manager.get_last_n_results('Arsenal', 5, 'home', comp='Barclays Premier League')]
    print [r for r in fpl_manager.get_last_n_results('Arsenal', 5, 'home', 'Everton', 'Barclays Premier League')]
