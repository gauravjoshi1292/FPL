__author__ = 'gj'

import json

from mongo import DbManager
from fixtures_crawler import get_fixtures
from urls import TEAM_STATS_URL, MONGODB_URL
from utils import get_soup_from_url, dump_as_json
from global_variables import TEAMS_MAP, GW_DB, TEAMS_COLLECTIONS


def get_team_stats():
    """
    Returns a dictionary containing data for all the teams

    :rtype: dict[str, list]
    """
    team_stats = {'teams': []}
    stats = {}
    soup = get_soup_from_url(TEAM_STATS_URL)
    tds = soup.find_all('td')
    keys = ['played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'goal_diff',
            'points']

    fixtures = get_fixtures()
    i = 0
    flag = False
    for col in tds:
        try:
            if col['class'][0] == 'col-club':
                flag = True
                stats['team'] = TEAMS_MAP[str(col.text)]
                continue
        except KeyError:
            pass

        if flag:
            stats[keys[i]] = int(col.text)
            i += 1

        if i > 7:
            i = 0
            flag = False
            stats['fixtures'] = fixtures[stats['team']]
            team_stats['teams'].append(stats)
            stats = {}

    return team_stats


def insert_team_stats_in_db(db_manager):
    """
    Inserts team statistics in the database

    :param db_manager: database manager handle
    :type db_manager: mongo.DbManager
    """
    # team_stats = get_team_stats()
    # dump_as_json(team_stats, '../data/team_stats.json')

    with open('../data/team_stats.json', 'r') as infile:
        team_data = json.load(infile)

    for key, team_stats in team_data.items():
        db_manager.insert(GW_DB, key, team_stats)


if __name__ == '__main__':
    db_manager = DbManager(MONGODB_URL)
    db_manager.drop_db(GW_DB)
    db_manager.create_db(GW_DB)
    db_manager.create_collections(GW_DB, TEAMS_COLLECTIONS)
    insert_team_stats_in_db(db_manager)
