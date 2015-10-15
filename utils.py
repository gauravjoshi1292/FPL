__author__ = 'gj'

import json
import time
import socket
import urllib2
import unicodedata
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from urls import *
from mongo import DbManager


DB_NAME = 'fpl'
COLLECTION_NAMES = ['teams', 'goalkeepers', 'defenders', 'midfielders', 'forwards',
                    'injuries']

PLAYER_TYPES = {'goalkeepers': 1, 'defenders': 2, 'midfielders': 3, 'forwards': 4}


TEAMS_MAP = {'Arsenal': 'ARS', 'Aston Villa': 'AVL',
             'Bournemouth': 'BOU', 'Chelsea': 'CHE',
             'Crystal Palace': 'CRY', 'Everton': 'EVE',
             'Leicester City': 'LEI', 'Liverpool': 'LIV',
             'Manchester United': 'MUN', 'Manchester City': 'MCI',
             'Newcastle United': 'NEW', 'Norwich City': 'NOR',
             'Southampton': 'SOU', 'Stoke City': 'STK',
             'Sunderland': 'SUN', 'Swansea City': 'SWA',
             'Tottenham Hotspur': 'TOT', 'Watford': 'WAT',
             'West Bromwich Albion': 'WBA', 'West Ham United': 'WHU'
             }


TEAMS_MAP2 = {'Arsenal': 'ARS', 'Aston Villa': 'AVL',
              'Bournemouth': 'BOU', 'Chelsea': 'CHE',
              'Crystal Palace': 'CRY', 'Everton': 'EVE',
              'Leicester': 'LEI', 'Liverpool': 'LIV',
              'Man Utd': 'MUN', 'Man City': 'MCI',
              'Newcastle': 'NEW', 'Norwich': 'NOR',
              'Southampton': 'SOU', 'Stoke': 'STK',
              'Sunderland': 'SUN', 'Swansea': 'SWA',
              'Spurs': 'TOT', 'Watford': 'WAT',
              'West Brom': 'WBA', 'West Ham': 'WHU'
              }

ALL_STAT_TYPES = {'now_cost': 4, 'total_points': 6, 'event_points': 5, 'minutes': 7,
                  'selected_by_percent': 3, 'assists': 7, 'clean_sheets': 7,
                  'yellow_cards': 7, 'red_cards': 7, 'saves': 7, 'bonus': 7,
                  'ea_index': 7, 'dreamteam_count': 7, 'form': 7, 'points_per_game': 7,
                  'bps': 7, 'goals_conceded': 7, 'goals_scored': 7, 'own_goals': 7,
                  'penalties_missed': 7, 'penalties_saved': 7, 'value_form': 7,
                  'value_season': 7, 'transfers_in': 7, 'transfers_out': 7,
                  'transfers_in_event': 7, 'transfers_out_event': 7,
                  'cost_change_start': 7, 'cost_change_start_fall': 7,
                  'cost_change_event': 7, 'cost_change_event_fall': 7}

STAT_MAP = {'now_cost': 'price', 'total_points': 'score',
                'event_points': 'round_score', 'minutes': 'minutes',
                'selected_by_percent': 'selected_by', 'assists': 'assists',
                'clean_sheets': 'clean_sheets', 'yellow_cards': 'yellow_cards',
                'red_cards': 'red_cards', 'saves': 'saves', 'bonus': 'bonus',
                'ea_index': 'ea_index', 'dreamteam_count': 'dreamteam_count',
                'form': 'form', 'points_per_game': 'ppg', 'bps': 'bps',
                'goals_conceded': 'goals_conceded', 'goals_scored': 'goals_scored',
                'own_goals': 'own_goals', 'penalties_missed': 'penalties_missed',
                'penalties_saved': 'penalties_saved', 'value_form': 'value_form',
                'value_season': 'value_season', 'transfers_in': 'transfers_in',
                'transfers_out': 'transfers_out',
                'transfers_in_event': 'transfers_in_week',
                'transfers_out_event': 'transfers_out_week',
                'cost_change_start': 'price_rise',
                'cost_change_start_fall': 'price_fall',
                'cost_change_event': 'price_rise_week',
                'cost_change_event_fall': 'price_fall_week'}


def normalize(text):
    """
    Returns a NFKD normalized ASCII form of the text

    :type text: str

    :rtype: str
    """
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')


def get_soup_from_url(url):
    """
    Given a url returns a soup of page source

    :param url: web url
    :type url: str

    :rtype: bs4.BeautifulSoup
    """
    try:
        response = urllib2.urlopen(url)
    except socket.error:
        proxy = urllib2.ProxyHandler({'http': 'http://bcproxy.ddu-india.com:8080'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)

    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup


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

    tables = soup.findAll('table')
    i = 0
    for table in tables:
        tds = table.findAll('td')
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


def get_chrome_driver(url):
    """
    Returns a selenium chrome driver

    :param url: page url
    :type url: str


    :rtype: selenium.webdriver.chrome.webdriver.WebDriver
    """
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def get_firefox_driver(url):
    """
    Returns a selenium firefox driver

    :param url: page ur;
    :type url: str

    :rtype: selenium.webdriver.firefox.webdriver.WebDriver
    """
    driver = webdriver.Firefox()
    driver.get(url)
    return driver


def get_safari_driver(url):
    """
    Returns a selenium safari driver

    :param url: page url
    :type url: str

    :rtype: selenium.webdriver.safari.webdriver.WebDriver
    """
    driver = webdriver.Safari()
    driver.get(url)
    return driver


def get_driver(url):
    """
    Return a selenium webdriver depending upon what's available on the system

    :param url: page url
    :type url: str

    :rtype: selenium.webdriver.chrome.webdriver.WebDriver |
            selenium.webdriver.firefox.webdriver.WebDriver |
            selenium.webdriver.safari.webdriver.WebDriver
    """
    try:
        driver = get_chrome_driver(url)
    except WebDriverException:
        try:
            driver = get_firefox_driver(url)
        except WebDriverException:
            try:
                driver = get_safari_driver(url)
            except WebDriverException:
                print "Could not find selenium web driver on system! Quit!"
                return

    return driver


def scroll_to_bottom(driver):
    """
    Scrolls to the bottom of web page

    :type driver: selenium.webdriver.chrome.webdriver.WebDriver |
                  selenium.webdriver.firefox.webdriver.WebDriver |
                  selenium.webdriver.safari.webdriver.WebDriver
    """
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')


def scroll_till_page_is_loaded(driver):
    """
    Scrolls down until the complete web page is loaded

    :type driver: selenium.webdriver.chrome.webdriver.WebDriver |
                  selenium.webdriver.firefox.webdriver.WebDriver |
                  selenium.webdriver.safari.webdriver.WebDriver
    """
    old_source = ''
    source = driver.page_source

    while source != old_source:
        scroll_to_bottom(driver)
        time.sleep(1)
        old_source = source
        source = driver.page_source


def get_soup_from_driver(driver):
    """
    Given a selenium web driver return the soup

    :type driver: selenium.webdriver.chrome.webdriver.WebDriver |
                  selenium.webdriver.firefox.webdriver.WebDriver|
                  selenium.webdriver.safari.webdriver.WebDriver

    :rtype: bs4.BeautifulSoup
    """
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    return soup


def get_table_from_driver(url, table_id):
    """
    Returns the table element with the given id from the web page

    :param url: page url
    :type url: str

    :param table_id: table id
    :type table_id: str

    :rtype: bs4.element.Tag
    """
    driver = get_driver(url)
    scroll_till_page_is_loaded(driver)
    soup = get_soup_from_driver(driver)
    table = soup.find('table', table_id)
    driver.quit()
    return table


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


def get_table_from_url(url, table_class):
    """
    Given a url and table class, returns the table element with that class

    :param url: page url
    :type url: str

    :param table_class: table class
    :type table_class: str

    :rtype: bs4.element.ResultSet
    """
    soup = get_soup_from_url(url)
    table = soup.find('table', {'class': table_class})

    if not table:
        return []

    tds = table.findAll('td')
    return tds


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
        url = url_template.format(player_type, stat_type, page)
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

    :param stat: dictionary containing stat
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
    for player_type, all_stats in data.items():
        organized_data[player_type] = []

        for key, player_stats in all_stats.items():
            new_player_stats = player_stats.copy()
            new_player_stats['name'] = key[1:-1].split(', ')[0][1:-1]
            new_player_stats['team'] = key[1:-1].split(', ')[1][1:-1]

            organized_data[player_type].append(new_player_stats)

    return organized_data


def get_fixtures():
    """
    Returns all future fixtures for teams

    :rtype: list[dict]
    """
    fixtures = {}

    soup = get_soup_from_url(FIXTURES_URL)
    tds = soup.findAll('td', {'class': 'clubs'})

    for td in tds:
        match = str(td.find('a').text)
        team1, team2 = map(lambda x: TEAMS_MAP2[x], match.split(' v '))

        try:
            fixtures[team1].append({'team': team2, 'place': 'home'})
        except KeyError:
            fixtures[team1] = [{'team': team2, 'place': 'home'}]
        try:
            fixtures[team2].append({'team': team1, 'place': 'away'})
        except KeyError:
            fixtures[team2] = [{'team': team1, 'place': 'away'}]

    return fixtures


def get_team_stats():
    """
    Returns a dictionary containing data for all the teams

    :rtype: dict[str, list]
    """
    team_stats = {'teams': []}
    stats = {}
    soup = get_soup_from_url(TEAM_STATS_URL)
    tds = soup.findAll('td')
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


def get_player_injuries():
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


def get_minutes_form():
    kwgs = {'player_type': 1, 'stat_type': 'total_points', 'page': 1}
    driver = get_driver(PLAYER_STATS_URL.format(**kwgs))
    soup = get_soup_from_driver(driver)
    print soup
    driver.quit()

get_minutes_form()


def dump_as_json(data, json_file):
    """
    Dumps the data into a json file

    :type data: dict

    :type json_file: str
    """
    with open(json_file, "w") as outfile:
        json.dump(data, outfile, indent=4)


def insert_player_stats_in_db(db_manager):
    """
    Inserts player statistics in the database

    :param db_manager: database manager handle
    :type db_manager: mongo.DbManager
    """
    # stats = get_organized_data(get_player_stats())
    # dump_as_json(stats, 'player_stats.json')

    with open('player_stats.json', 'r') as infile:
        player_data = json.load(infile)

    for key, player_stats in player_data.items():
        db_manager.insert(DB_NAME, key, player_stats)


def insert_team_stats_in_db(db_manager):
    """
    Inserts team statistics in the database

    :param db_manager: database manager handle
    :type db_manager: mongo.DbManager
    """
    # team_stats = get_team_stats()
    # dump_as_json(team_stats, 'team_stats.json')

    with open('team_stats.json', 'r') as infile:
        team_data = json.load(infile)

    for key, team_stats in team_data.items():
        db_manager.insert(DB_NAME, key, team_stats)


def insert_injuries_in_db(db_manager):
    """
    Inserts player injuries in the database

    :param db_manager: database manager handle
    :type db_manager: mongo.DbManager
    """
    # injuries = get_player_injuries()
    # dump_as_json(injuries, 'injuries.json')

    with open('injuries.json', 'r') as infile:
        injury_data = json.load(infile)

    for key, injuries in injury_data.items():
        db_manager.insert(DB_NAME, key, injuries)


def create_database():
    """
    Creates a mongo database of player statistics
    :return:
    """
    fpl_manager = DbManager('mongodb://localhost:27017')
    fpl_manager.drop_db(DB_NAME)
    fpl_manager.create_db(DB_NAME)
    fpl_manager.create_collections(DB_NAME, COLLECTION_NAMES)

    insert_player_stats_in_db(fpl_manager)
    insert_team_stats_in_db(fpl_manager)
    insert_injuries_in_db(fpl_manager)


create_database()
