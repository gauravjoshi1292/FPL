__author__ = 'gj'

import json
import unicodedata

from mongo import DbManager
from fixtures_crawler import get_fixtures
from urls import PLAYER_LIST_URL, PLAYER_STATS_URL, MONGODB_URL
from utils import normalize, get_soup_from_url, get_table_from_url, dump_as_json
from global_variables import STAT_MAP, ALL_STAT_TYPES, PLAYER_TYPES, GW_DB, PLAYERS_COLLECTIONS


def get_player_list():
    """
    Returns dicts of players having team, price and points info

    :rtype: dict, dict, dict, dict
    """
    goalkeepers = {}
    defenders = {}
    midfielders = {}
    forwards = {}
    soup = get_soup_from_url(PLAYER_LIST_URL)

    tables = soup.find_all('table')
    i = 0
    for table in tables:
        tds = table.find_all('td')
        player_name = ''
        player_data = {}

        j = 0
        for td in tds:
            if j == 0:
                player_name = unicodedata.normalize('NFKD', td.text).encode('ascii', 'ignore')
            elif j == 1:
                player_data['team'] = unicodedata.normalize('NFKD', td.text).encode('ascii', 'ignore')
            elif j == 2:
                player_data['points'] = int(td.text)
            elif j == 3:
                player_data['price'] = float(td.text.encode('ascii', 'ignore'))
            elif j > 3:
                if i < 2:
                    goalkeepers[player_name] = player_data
                elif 2 <= i < 4:
                    defenders[player_name] = player_data
                elif 4 <= i < 6:
                    midfielders[player_name] = player_data
                elif 6 <= i < 8:
                    forwards[player_name] = player_data
                player_data = {}
                j = 1
                player_name = unicodedata.normalize('NFKD', td.text).encode('ascii', 'ignore')
                continue

            j += 1
        i += 1

    return goalkeepers, defenders, midfielders, forwards


def get_stat_from_text(text, stats_type):
    """
    Returns a value by converting string to appropriate type

    :param text: text to be converted
    :type text: str

    :param stats_type: type of stat

    :rtype: int | float
    """
    if stats_type in ['transfers_in', 'transfers_out', 'transfers_in_event',
                      'transfers_out_event']:
        return int(text.replace(',', ''))

    elif stats_type in ['now_cost', 'form', 'points_per_game', 'value_form',
                        'value_season', 'cost_change_start', 'cost_change_start_fall',
                        'cost_change_event', 'cost_change_event_fall']:
        return float(text)

    elif stats_type == 'selected_by_percent':
        return float(text.strip('%'))

    return int(text)


def scrape_stat_from_table(url_template, player_type, stat_type, table_class, column):
    """
    Scrapes and returns statistic from the table

    :param url_template: page url template
    :type url_template: str

    :param player_type: type of player
    :type player_type: int

    :param stat_type: type of stat
    :type stat_type: str

    :param table_class: table class
    :type table_class: str

    :param column: column that contains stat
    :type column: int

    :rtype: dict[(str, str), int | float]
    """
    data = {}

    page = 1
    while True:
        url = url_template.format(player_type=player_type, stat_type=stat_type, page=page)
        table = get_table_from_url(url, table_class)

        if not table:
            break

        name, team, value, i, check = '', '', 0, 0, False
        for td in table:
            if len(td.findChildren()) == 1:
                continue

            if len(td.findChildren()) == 2:
                i = 0
                check = True
                continue

            if check:
                if i == 0:
                    name = normalize(td.text)
                elif i == 1:
                    team = normalize(td.text)
                elif i == column:
                    value = get_stat_from_text(normalize(td.text), stat_type)
                    data[str((name, team))] = value
                    name = ''
                    team = ''
                    check = False
                    continue

                i += 1
        page += 1

    return data


def add_stat_to_dictionary(data_dict, stat, stat_type):
    """
    Adds statistics to the dictionary of all players

    :param data_dict: dictionary containing players
    :type data_dict: dict[(str, str), dict[str, int | float]]

    :param stat: dictionary containing statistics
    :type stat: dict[(str, str), int | float]

    :param stat_type: type of stat
    :type stat_type: str
    """
    for player, value in stat.items():
        try:
            data_dict[player][STAT_MAP[stat_type]] = value
        except KeyError:
            data_dict[player] = {}
            data_dict[player][STAT_MAP[stat_type]] = value


def get_player_stats():
    """
    Returns all the statistics for keepers

    :rtype: dict[(str, str), dict[str, int | float]]
    """
    player_stats = {}

    for player_type, val in PLAYER_TYPES.items():
        stats = {}

        for stat_type, column in ALL_STAT_TYPES.items():
            stat = scrape_stat_from_table(PLAYER_STATS_URL, val, stat_type, 'ismTable',
                                          column)

            add_stat_to_dictionary(stats, stat, stat_type)

        player_stats[player_type] = stats

    return player_stats


def get_organized_data(data):
    """
    Organizes the data into a proper format and returns it

    :type data: dict

    :rtype: dict
    """
    organized_data = {}
    fixtures = get_fixtures()
    for player_type, all_stats in data.items():
        organized_data[player_type] = []

        for key, player_stats in all_stats.items():
            new_player_stats = player_stats.copy()
            name, team = key[1:-1].split(', ')[0][1:-1], key[1:-1].split(', ')[1][1:-1]
            new_player_stats['name'] = name
            new_player_stats['team'] = team
            new_player_stats['next_match'] = fixtures[team][0]

            organized_data[player_type].append(new_player_stats)

    return organized_data


def insert_player_stats_in_db(db_manager):
    """
    Inserts player statistics in the database

    :param db_manager: database manager handle
    :type db_manager: mongo.DbManager
    """
    # stats = get_organized_data(get_player_stats())
    # dump_as_json(stats, '../data/player_stats.json')

    with open('../data/player_stats.json', 'r') as infile:
        player_data = json.load(infile)

    for key, player_stats in player_data.items():
        db_manager.insert(GW_DB, key, player_stats)


if __name__ == '__main__':
    db_manager = DbManager(MONGODB_URL)
    db_manager.drop_db(GW_DB)
    db_manager.create_db(GW_DB)
    db_manager.create_collections(GW_DB, PLAYERS_COLLECTIONS)
    insert_player_stats_in_db(db_manager)
