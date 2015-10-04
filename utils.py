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


PLAYER_TYPES = {'goalkeepers': 1, 'defenders': 2, 'midfielders': 3, 'forwards': 4}


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

STAT_MAPPING = {'now_cost': 'price', 'total_points': 'score',
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


def get_league_table_data():
    """
    Returns a dictionary containing league table data for all the teams

    :rtype: dict
    """
    table_data = {}
    team_data = {}
    team_name = ''
    soup = get_soup_from_url(url=LEAGUE_TABLE_URL)
    tds = soup.findAll('td')
    keys = ['played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'goal_diff',
            'points']

    i = 0
    flag = False
    for col in tds:
        try:
            if col['class'][0] == 'col-club':
                flag = True
                team_name = str(col.text)
                continue
        except KeyError:
            pass

        if flag:
            team_data[keys[i]] = int(col.text)
            i += 1

        if i > 7:
            i = 0
            flag = False
            table_data[team_name] = team_data
            team_data = {}

    return table_data


def get_player_list():
    """
    Returns dicts of players having team, price and points info

    :rtype: dict, dict, dict, dict
    """
    goalkeepers = {}
    defenders = {}
    midfielders = {}
    forwards = {}
    soup = get_soup_from_url(url=PLAYER_LIST_URL)

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
    driver.get(url=url)
    return driver


def get_firefox_driver(url):
    """
    Returns a selenium firefox driver

    :param url: page ur;
    :type url: str

    :rtype: selenium.webdriver.firefox.webdriver.WebDriver
    """
    driver = webdriver.Firefox()
    driver.get(url=url)
    return driver


def get_safari_driver(url):
    """
    Returns a selenium safari driver

    :param url: page url
    :type url: str

    :rtype: selenium.webdriver.safari.webdriver.WebDriver
    """
    driver = webdriver.Safari()
    driver.get(url=url)
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
        driver = get_chrome_driver(url=url)
    except WebDriverException:
        try:
            driver = get_firefox_driver(url=url)
        except WebDriverException:
            try:
                driver = get_safari_driver(url=url)
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
        scroll_to_bottom(driver=driver)
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
    driver = get_driver(url=url)
    scroll_till_page_is_loaded(driver=driver)
    soup = get_soup_from_driver(driver=driver)
    table = soup.find('table', id=table_id)
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
    soup = get_soup_from_url(url=url)
    table = soup.find('table', {'class': table_class})

    if not table:
        return []

    tds = table.findAll('td', {'class': None})
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
        url = url_template.format(player_type=player_type, stat_type=stat_type, page=page)
        table = get_table_from_url(url=url, table_class=table_class)

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
            data_dict[player][STAT_MAPPING[stat_type]] = value
        except KeyError:
            data_dict[player] = {}
            data_dict[player][STAT_MAPPING[stat_type]] = value


def get_player_stats():
    """
    Returns all the statistics for keepers

    :rtype: dict[(str, str), dict[str, int | float]]
    """
    player_stats = {}

    for player_type, val in PLAYER_TYPES.items():
        stats = {}

        for stat_type, column in ALL_STAT_TYPES.items():
            stat = scrape_stat_from_table(url_template=GOALKEEPER_STATS_URL,
                                          player_type=val,
                                          stat_type=stat_type,
                                          table_class='ismTable',
                                          column=column)

            add_stat_to_dictionary(data_dict=stats, stat=stat, stat_type=stat_type)

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
            print key[1:-1].split(', ')[0][1:-1]
            new_player_stats['name'] = key[1:-1].split(', ')[0][1:-1]
            new_player_stats['team'] = key[1:-1].split(', ')[1][1:-1]

            organized_data[player_type].append(new_player_stats)

    return organized_data


def dump_as_json(data, json_file):
    """
    Dumps the data into a json file

    :type data: dict

    :type json_file: str
    """
    with open(json_file, "w") as outfile:
        json.dump(data, outfile, indent=4)

stats = get_organized_data(get_player_stats())
dump_as_json(data=stats, json_file='stats.json')
