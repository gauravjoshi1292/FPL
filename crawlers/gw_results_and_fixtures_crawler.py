__author__ = 'gj'

from datetime import datetime

from urls import GAMEWEEK_FIXTURES_AND_RESULTS_URL
from global_variables import TEAMS_MAP, GW_DB, YEAR
from utils import normalize, get_table_from_url, dump_as_json, load_as_json


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
                    text = '{0} {1}'.format(normalize(td.text.strip()), YEAR)
                    date = datetime.strptime(text, '%d %b %Y')
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
    # dump_as_json(gw_fixtures_and_results, 'data/gw_fixtures_and_results.json')

    gw_data = load_as_json('data/gw_fixtures_and_results.json')

    for key, data in gw_data.items():
        db_manager.create_collection(GW_DB, key)
        db_manager.insert(GW_DB, key, data)
