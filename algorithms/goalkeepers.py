__author__ = 'gj'

from mongo import FplManager

from algorithms.common import get_stat_rating, get_max_and_min, get_fixture_rating

SCORE_WT = 10.0
CS_WT = 7.0
GC_WT = -1.0
SAVES_WT = 1.0
FORM_WT = 10.0
RS_WT = 7.0
MINUTES_WT = 3.0

WT_SUM = SCORE_WT + CS_WT + GC_WT + SAVES_WT + FORM_WT + RS_WT

FIXTURES_LIM = 5


def get_goalkeeper_rating(stats, maxs, mins):
    """
    Returns the absolute rating for a goalkeeper

    :param stats: keeper's statistics
    :type stats: dict

    :param maxs: max_values for keeper's statistics
    :type maxs: dict

    :param mins: min_values for keeper's statistics
    :type mins: dict

    :rtype: float
    """
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

    rating = (SCORE_WT*score_rating + CS_WT*cs_rating + GC_WT*gc_rating +
              SAVES_WT*saves_rating + FORM_WT*form_rating +
              RS_WT*rs_rating) * 5.0 / WT_SUM

    return rating


def calculate_goalkeeper_ratings(manager, db_name, collection_name):
    """
    Returns absolute and affected ratings for all the goalkeepers

    :param manager: fpl database manager
    :type manager: mongo.FplManager

    :param db_name: database name
    :type db_name: str

    :param collection_name: collection name
    :type collection_name: str

    :rtype: dict
    """
    goalkeeper_ratings = {}
    goalkeeper_entries = manager.find(db_name, 'goalkeepers', {})
    team_entries = manager.find(db_name, 'teams', {})
    injuries = manager.find(db_name, 'injuries', {})

    maxs, mins = get_max_and_min(player_stats=goalkeeper_entries)
    fixture_ratings = get_fixture_rating(team_stats=team_entries, n_fixtures=FIXTURES_LIM)

    goalkeeper_entries.rewind()
    for goalkeeper_entry in goalkeeper_entries:
        injury_info = manager.find_one(db_name, 'injuries',
                                       {'name': goalkeeper_entry['name'],
                                        'team': goalkeeper_entry['team']})
        if injury_info:
            availability = injury_info['availability']
        else:
            availability = 1

        minutes_rating = get_stat_rating(goalkeeper_entry['minutes'], maxs['minutes'],
                                         mins['minutes'])
        absolute_rating = get_goalkeeper_rating(stats=goalkeeper_entry, maxs=maxs,
                                                mins=mins)
        affected_rating = minutes_rating * availability * (
            (absolute_rating + fixture_ratings[goalkeeper_entry['team']]) / 2.0)

        goalkeeper_ratings[(goalkeeper_entry['name'], goalkeeper_entry['team'])] = {
            'absolute_rating': absolute_rating, 'affected_rating': affected_rating}

    return goalkeeper_ratings


fpl_manager = FplManager(uri='mongodb://localhost:27017')
gr = calculate_goalkeeper_ratings(manager=fpl_manager, db_name='fpl',
                                  collection_name='goalkeepers')
print sorted(gr.items(), key=lambda x: x[1]['affected_rating'], reverse=True)
fpl_manager.close_connection()
