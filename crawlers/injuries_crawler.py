__author__ = 'gj'

import json

from mongo import DbManager
from urls import MONGODB_URL, INJURIES_URL
from global_variables import GW_DB, INJURIES_COLLECTIONS
from utils import normalize, get_table_from_url, dump_as_json


def get_player_injuries():
    """
    Returns a dictionary containing information about player injuries and suspensions

    :rtype: dict[str, list]
    """
    player_injuries = {'injuries': []}
    table = get_table_from_url(INJURIES_URL, "ffs-ib ffs-ib-full-content ffs-ib-sort")

    i = 0
    critical = ['Injured', 'Disciplinary', 'On Loan', 'Unavailable', 'Doubt 50%',
                'Doubt 75%', 'Suspended']
    safe = {'Doubt 25%': 0.75, 'Available': 1}

    name, team, availability, return_date = '', '', 1, ''
    for row in table:
        if i == 0:
            name = normalize(row.find('img').text).split('(')[0].strip().split(' ')[-1]
        elif i == 1:
            team = normalize(row.text)
        elif i == 2:
            status = normalize(row.find('span').text)
            if status in critical:
                availability = 0
            else:
                availability = safe[status]
        elif i == 3:
            return_date = normalize(row.text)
        elif i == 4:
            pass
        elif i == 5:
            i = 0
            player_injuries['injuries'].append({'name': name, 'team': team,
                                                'availability': availability,
                                                'return_date': return_date})
            name, team, doubt, return_date = '', '', '', ''
            continue
        i += 1

    return player_injuries


def insert_injuries_in_db(db_manager):
    """
    Inserts player injuries in the database

    :param db_manager: database manager handle
    :type db_manager: mongo.DbManager
    """
    # injuries = get_player_injuries()
    # dump_as_json(injuries, '../data/injuries.json')

    with open('../data/injuries.json', 'r') as infile:
        injury_data = json.load(infile)

    for key, injuries in injury_data.items():
        db_manager.insert(GW_DB, key, injuries)


if __name__ == '__main__':
    db_manager = DbManager(MONGODB_URL)
    db_manager.drop_db(GW_DB)
    db_manager.create_db(GW_DB)
    db_manager.create_collections(GW_DB, INJURIES_COLLECTIONS)
    insert_injuries_in_db(db_manager)
