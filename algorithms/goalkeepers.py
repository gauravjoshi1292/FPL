__author__ = 'gj'

from mongo import FplManager


SCORE_WT = 10
CS_WT = 7
GC_WT = -1
SAVES_WT = 1
FORM_WT = 9
RS_WT = 7
MINUTES_WT = 3

WT_SUM = SCORE_WT + CS_WT + GC_WT + SAVES_WT + FORM_WT + RS_WT + MINUTES_WT


def get_stat_rating(val, max_val, min_val):
    return float(val-min_val)/(max_val - min_val)


def get_goalkeeper_rating(stats, maxs, mins):
    if stats['minutes'] == 0:
        return 0

    score_rating = get_stat_rating(stats['score'], maxs['score'], mins['score'])
    cs_rating = get_stat_rating(stats['clean_sheets'], maxs['clean_sheets'],
                                mins['clean_sheets'])
    gc_rating = get_stat_rating(stats['goals_conceded'], maxs['goals_conceded'],
                                mins['goals_conceded'])
    saves_rating = get_stat_rating(stats['saves'], maxs['saves'], mins['saves'])
    form_rating = get_stat_rating(stats['form'], maxs['form'], mins['form'])
    rs_rating = get_stat_rating(stats['round_score'], maxs['round_score'],
                                mins['round_score'])
    minutes_rating = get_stat_rating(stats['minutes'], maxs['minutes'], mins['minutes'])

    rating = (SCORE_WT*score_rating + CS_WT*cs_rating + GC_WT*gc_rating +
              SAVES_WT*saves_rating + FORM_WT*form_rating + RS_WT*rs_rating +
              MINUTES_WT*minutes_rating) * 5 / WT_SUM

    return rating


def get_max_and_min(player_stats):
    maxs = {}
    mins = {}
    for stat in player_stats:
        for key in stat:
            if key in ['_id', 'name', 'team']:
                continue

            try:
                if stat[key] > maxs[key] and stat['minutes']:
                    maxs[key] = stat[key]
            except KeyError:
                if stat['minutes']:
                    maxs[key] = stat[key]

            try:
                if stat[key] < mins[key] and stat['minutes']:
                    mins[key] = stat[key]
            except KeyError:
                if stat['minutes']:
                    mins[key] = stat[key]

    return maxs, mins


def calculate_goalkeeper_ratings(manager, db_name, collection_name):
    goalkeeper_ratings = {}
    goalkeeper_entries = manager.client[db_name][collection_name].find()

    maxs, mins = get_max_and_min(goalkeeper_entries)

    goalkeeper_entries.rewind()
    for goalkeeper_entry in goalkeeper_entries:
        rating = get_goalkeeper_rating(goalkeeper_entry, maxs, mins)
        goalkeeper_ratings[(goalkeeper_entry['name'], goalkeeper_entry['team'])] = rating

    return sorted(goalkeeper_ratings.items(), key=lambda x: x[1], reverse=True)


fpl_manager = FplManager(uri='mongodb://localhost:27017')

print calculate_goalkeeper_ratings(manager=fpl_manager, db_name='fpl',
                                   collection_name='goalkeepers')

fpl_manager.close_connection()
