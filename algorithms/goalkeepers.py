__author__ = 'gj'

from mongo import FplManager


def get_stat_rating(val, avg):
    return (val-avg)/avg


def get_goalkeeper_rating(stats, avgs):
    score_rating = get_stat_rating(stats['score'], avgs['score'])
    cs_rating = get_stat_rating(stats['clean_sheets'], avgs['clean_sheets'])
    gc_rating = get_stat_rating(stats['goals_conceded'], avgs['goals_conceded'])
    saves_rating = get_stat_rating(stats['saves'], avgs['saves'])
    form_rating = get_stat_rating(stats['form'], avgs['form'])
    rs_rating = get_stat_rating(stats['round_score'], avgs['round_score'])
    minutes_rating = get_stat_rating(stats['minutes'], avgs['minutes'])

    rating = (score_rating + cs_rating - gc_rating + saves_rating +
              form_rating + rs_rating + minutes_rating)
    return rating


def get_avgs(player_stats):
    avgs = {}
    sums = {}
    count = {}
    for stat in player_stats:
        for key in stat:
            if key in ['_id', 'name', 'team']:
                continue
            try:
                sums[key] += stat[key]
                if stat['minutes']:
                    count[key] += 1
            except KeyError:
                sums[key] = stat[key]
                if stat['minutes']:
                    count[key] = 1

    for key in sums:
        avgs[key] = float(sums[key])/count[key]

    return avgs


def calculate_goalkeeper_ratings(manager, db_name, collection_name):
    goalkeeper_ratings = {}
    goalkeeper_entries = manager.client[db_name][collection_name].find()

    avgs = get_avgs(goalkeeper_entries)

    goalkeeper_entries.rewind()
    for goalkeeper_entry in goalkeeper_entries:
        rating = get_goalkeeper_rating(goalkeeper_entry, avgs)
        goalkeeper_ratings[(goalkeeper_entry['name'], goalkeeper_entry['team'])] = rating

    return goalkeeper_ratings


fpl_manager = FplManager(uri='mongodb://localhost:27017')

print calculate_goalkeeper_ratings(manager=fpl_manager, db_name='fpl',
                                   collection_name='goalkeepers')

fpl_manager.close_connection()
