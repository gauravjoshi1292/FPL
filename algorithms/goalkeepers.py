__author__ = 'gj'

from mongo import DbManager
from global_variables import *
from algorithms.common import *

SCORE_WT = 10.0
CS_WT = 7.0
GC_WT = -1.0
SAVES_WT = 1.0
FORM_WT = 10.0
RS_WT = 8.0

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


def calculate_goalkeeper_ratings(db_manager, db_name):
    """
    Returns absolute and affected ratings for all the goalkeepers

    :param db_manager: database manager
    :type db_manager: mongo.DbManager

    :param db_name: database name
    :type db_name: str

    :rtype: dict
    """
    goalkeeper_ratings = {}

    goalkeeper_stats = get_player_stats(db_manager, db_name, 'goalkeepers')
    team_stats = get_team_stats(db_manager, db_name, 'teams')
    injuries = get_injuries(db_manager, db_name, 'injuries')

    maxs, mins = get_max_and_min(goalkeeper_stats)
    fixture_rating = get_fixture_rating(team_stats, FIXTURES_LIM)

    for key, stats in goalkeeper_stats.items():
        player = key[0]
        team = key[1]

        try:
            availability = injuries[player]['availability']
        except KeyError:
            availability = 1

        minutes_rating = get_stat_rating(stats['minutes'], maxs['minutes'], mins['minutes'])
        absolute_rating = get_goalkeeper_rating(stats, maxs, mins)
        affected_rating = minutes_rating * availability * ((absolute_rating + fixture_rating[team]) / 2.0)

        goalkeeper_ratings[(player, team)] = {'absolute_rating': absolute_rating,
                                              'affected_rating': affected_rating}

    return goalkeeper_ratings


fpl_manager = DbManager('mongodb://localhost:27017')
ratings = calculate_goalkeeper_ratings(fpl_manager, DB_NAME)
print sorted(ratings.items(), key=lambda x: x[1]['affected_rating'], reverse=True)
fpl_manager.close_connection()
