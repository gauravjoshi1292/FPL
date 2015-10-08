__author__ = 'gj'

from mongo import FplManager


def get_goalkeeper_rating(stats):
    rating = 0

    score = stats['score']
    cs = stats['clean_sheets']
    gc = stats['goals_conceded']
    saves = stats['saves']
    form = stats['form']
    rs = stats['round_score']
    mp = stats['minutes']
    rs = stats['round_score']

    return rating


def get_goalkeeper_ratings(manager, db_name, collection_name):
    print fpl_manager.client.database_names()
    for goalkeeper_entry in manager.client[db_name][collection_name].find():
        print 'ss'
        rating = get_goalkeeper_rating(goalkeeper_entry)
        print rating


fpl_manager = FplManager(uri='mongodb://localhost:27017')

get_goalkeeper_ratings(manager=fpl_manager, db_name='fpl', collection_name='goalkeepers')
