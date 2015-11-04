__author__ = 'gj'

import os

from urls import TEAM_STATS_URL
from global_variables import TEAMS_MAP, GW_DB
from utils import get_soup_from_url, dump_as_json, load_as_json

from fixtures_crawler import get_fixtures


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
    team_stats = get_team_stats()
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/team_stats.json'))

    dump_as_json(team_stats, file_path)
    team_data = load_as_json(file_path)

    for key, team_stats in team_data.items():
        db_manager.create_collection(GW_DB, key)
        db_manager.insert(GW_DB, key, team_stats)
