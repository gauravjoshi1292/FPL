__author__ = 'gj'

import json

from mongo import DbManager
from utils import normalize, get_table_from_url
from urls import MONGODB_URL, GAMEWEEK_FIXTURES_AND_RESULTS_URL
from global_variables import TEAMS_MAP, GW_DB, GW_FIXTURES_AND_RESULTS_COLLECTIONS


def get_gameweek_fixtures_and_results():
    """
    Returns fixtures and results for the current gameweek

    :rtype: dict
    """
    gw_fixtures_and_results = {'gw_fixtures': [], 'gw_results': []}

    table = get_table_from_url(GAMEWEEK_FIXTURES_AND_RESULTS_URL,
                               'table-matches table-matches-narrow')

    date, home_team, away_team, home_goals, away_goals, win = '', '', '', 0, 0, ''
    for td in table:
        try:
            if td['class'][0] == 'column-date':
                if td.text.strip():
                    date = normalize(td.text.strip())
            elif td['class'][0] == 'column-team-a':
                home_team = TEAMS_MAP[normalize(td.text.strip())]
            elif td['class'][0] == 'column-score':
                score = normalize(td.text.strip())
                home_goals, away_goals = map(int, score.split(' - '))
                if home_goals > away_goals:
                    win = 'home'
                elif home_goals < away_goals:
                    win = 'away'
                else:
                    win = 'draw'
            elif td['class'][0] == 'column-team-b':
                away_team = TEAMS_MAP[normalize(td.text.strip())]
                fixture = {'date': date, 'home_team': home_team, 'away_team': away_team}
                result = {'date': date, 'home_team': home_team, 'away_team': away_team,
                          'home_goals': home_goals, 'away_goals': away_goals, 'win': win}

                gw_fixtures_and_results['gw_fixtures'].append(fixture)
                gw_fixtures_and_results['gw_results'].append(result)

        except KeyError:
            pass

    return gw_fixtures_and_results


def insert_gameweek_fixtures_and_results_in_db(db_manager):
    """
    Inserts gameweek fixtures and results in the database

    :param db_manager: database manager handle
    :type db_manager: mongo.DbManager
    """
    # gw_fixtures_and_results = get_gameweek_fixtures_and_results()
    # dump_as_json(gw_fixtures_and_results, '../data/gw_fixtures_and_results.json')

    with open('../data/gw_fixtures_and_results.json', 'r') as infile:
        results_data = json.load(infile)

    for key, results in results_data.items():
        db_manager.insert(GW_DB, key, results)


if __name__ == '__main__':
    db_manager = DbManager(MONGODB_URL)
    db_manager.drop_db(GW_DB)
    db_manager.create_db(GW_DB)
    db_manager.create_collections(GW_DB, GW_FIXTURES_AND_RESULTS_COLLECTIONS)
    insert_gameweek_fixtures_and_results_in_db(db_manager)
