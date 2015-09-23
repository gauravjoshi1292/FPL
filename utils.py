__author__ = 'gj'

import time
import socket
import urllib2
import datetime
import unicodedata
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from urls import *


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
        proxy = urllib2.ProxyHandler({"http": "http://bcproxy.ddu-india.com:8080"})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)

    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_league_table_data():
    """
    Returns a dictionary containing league table data for all the teams

    :rtype: dict
    """
    table_data = {}
    team_data = {}
    team_name = ""
    soup = get_soup_from_url(url=LEAGUE_TABLE_URL)
    tds = soup.findAll("td")
    keys = ["played", "won", "drawn", "lost", "goals_for", "goals_against", "goal_diff",
            "points"]

    i = 0
    flag = False
    for col in tds:
        try:
            if col["class"][0] == "col-club":
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

    tables = soup.findAll("table")
    i = 0
    for table in tables:
        tds = table.findAll("td")
        player_name = ""
        player_data = {}

        j = 0
        for td in tds:
            if j == 0:
                player_name = unicodedata.normalize("NFKD", td.text).encode("ascii", "ignore")
            elif j == 1:
                player_data["team"] = unicodedata.normalize("NFKD", td.text).encode("ascii", "ignore")
            elif j == 2:
                player_data["points"] = int(td.text)
            elif j == 3:
                player_data["price"] = float(td.text.encode("ascii", "ignore"))
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
                player_name = unicodedata.normalize("NFKD", td.text).encode("ascii", "ignore")
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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_till_page_is_loaded(driver):
    """
    Scrolls down until the complete web page is loaded

    :type driver: selenium.webdriver.chrome.webdriver.WebDriver |
                  selenium.webdriver.firefox.webdriver.WebDriver |
                  selenium.webdriver.safari.webdriver.WebDriver
    """
    old_source = ""
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
    soup = BeautifulSoup(source, "html.parser")
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
    table = soup.find("table", id=table_id)
    driver.quit()
    return table


def get_url_for_stats(stats_type):
    """
    Given the type of stats construct the page url and return it

    :param stats_type: type of stats, eg: saves, goals-conceded etc.
    :type stats_type: str

    :rtype: str
    """
    date = datetime.datetime.strptime(str(datetime.date.today()),
                                      "%Y-%m-%d").strftime("%d/%m/%Y")

    url = GOALKEEPING_STATS_URL.format(stats_type=stats_type, curr_date=date)
    return url


def get_clean_sheets():
    """
    Returns clean sheet stats for all the keepers

    :rtype: dict
    """
    clean_sheet_data = {}
    url = get_url_for_stats(stats_type="clean-sheets")
    table = get_table_from_driver(url=url, table_id="ranking-stats-table")
    tds = table.findAll("td")

    i = 0
    name, team, matches_played, minutes_played, clean_sheets = "", "", 0, 0, 0
    for td in tds:
        try:
            if td["class"][0] == "table-playerteam-field":
                name = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-name"}).text).encode("ascii", "ignore").split()[-1]
                team = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-team"}).text).encode("ascii", "ignore").split(" - ")[1]
                i = 0
                continue

        except KeyError:
            if i == 0:
                matches_played = int(td.text)
                i += 1
            elif i == 1:
                minutes_played = int(td.text)
                i += 1
            elif i == 2:
                i = 0
                clean_sheets = int(td.text)
                clean_sheet_data[name] = {"team": team,
                                          "matches_played": matches_played,
                                          "minutes_played": minutes_played,
                                          "clean_sheets": clean_sheets}

    return clean_sheet_data


def get_saves():
    """
    Returns saves stats for all the keepers

    :rtype: dict
    """
    saves_data = {}
    url = get_url_for_stats(stats_type="saves")
    table = get_table_from_driver(url=url, table_id="ranking-stats-table")
    tds = table.findAll("td")

    i = 0
    name, team, saves = "", "", 0
    for td in tds:
        try:
            if td["class"][0] == "table-playerteam-field":
                name = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-name"}).text).encode("ascii", "ignore").split()[-1]
                team = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-team"}).text).encode("ascii", "ignore").split(" - ")[1]
                i = 0
                continue

        except KeyError:
            if i == 5:
                i = 0
                saves = int(td.text)
                saves_data[name] = {"team": team, "saves": saves}
                continue
            else:
                i += 1

    return saves_data


def get_goals_conceded():
    """
    Returns goals conceded stats for all the keepers

    :rtype: dict
    """
    goals_conceded_data = {}
    url = get_url_for_stats(stats_type="goals-conceded")
    table = get_table_from_driver(url=url, table_id="ranking-stats-table")
    tds = table.findAll("td")

    i = 0
    name, team, saves = "", "", 0
    for td in tds:
        try:
            if td["class"][0] == "table-playerteam-field":
                name = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-name"}).text).encode("ascii", "ignore").split()[-1]
                team = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-team"}).text).encode("ascii", "ignore").split(" - ")[1]
                i = 0
                continue

        except KeyError:
            if i == 8:
                i = 0
                goals_conceded = int(td.text)
                goals_conceded_data[name] = {"team": team,
                                             "goals_conceded": goals_conceded}
                continue
            else:
                i += 1

    return goals_conceded_data


def get_all_goalkeepers():
    """
    Returns a dictionary of all the keepers found on the site

    :rtype: dict
    """
    goalkeepers = {}
    url = get_url_for_stats(stats_type="performance-score")
    table = get_table_from_driver(url=url, table_id="ranking-stats-table")
    tds = table.findAll("td")

    i = 0
    name = ""
    for td in tds:
        try:
            if td["class"][0] == "table-playerteam-field":
                name = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-name"}).text).encode("ascii", "ignore").split()[-1]
                team = unicodedata.normalize(
                    "NFKD", td.find_next("div", {"class": "stats-player-team"}).text).encode("ascii", "ignore").split(" - ")[1]
                goalkeepers[name] = {"team": team, "minutes_played": 0,
                                     "clean_sheets": 0, "matches_played": 0,
                                     "saves": 0, "goals_conceded": 0}
                continue

        except KeyError:
            if not name:
                continue

            if i == 0:
                goalkeepers[name]["matches_played"] = int(td.text)
            elif i == 1:
                goalkeepers[name]["minutes_played"] = int(td.text)
            elif i == 5:
                i = 0
                name = ""
                continue

            i += 1

    return goalkeepers


def get_goalkeeper_stats():
    """
    Returns statistics for all the keepers from squawka

    :rtype: dict
    """
    goalkeeper_stats = {}
    goalkeepers = get_all_goalkeepers()
    clean_sheet_stats = get_clean_sheets()
    saves_stats = get_saves()
    goals_conceded_stats = get_goals_conceded()

    for player in goalkeepers:
        goalkeeper_stats[player] = goalkeepers[player]
        try:
            goalkeeper_stats[player]["matches_played"] = clean_sheet_stats[player]["matches_played"]
            goalkeeper_stats[player]["minutes_played"] = clean_sheet_stats[player]["minutes_played"]
            goalkeeper_stats[player]["clean_sheets"] = clean_sheet_stats[player]["clean_sheets"]
        except KeyError:
            pass

        try:
            goalkeeper_stats[player]["saves"] = saves_stats[player]["saves"]
        except KeyError:
            pass

        try:
            goalkeeper_stats[player]["goals_conceded"] = goals_conceded_stats[player]["goals_conceded"]
        except KeyError:
            pass

    return goalkeeper_stats


def get_goalkeeper_data():
    """
    Returns a dictionary containing data for all the keepers in the league

    :rtype: dict
    """
    goalkeeper_data = {}
    all_goalkeepers = get_player_list()[0]
    goalkeeper_stats = get_goalkeeper_stats()

    for player in all_goalkeepers:
        data = all_goalkeepers[player]
        try:
            data.update(goalkeeper_stats[player])
        except KeyError:
            data.update({'goals_conceded': 0, 'minutes_played': 0, 'saves': 0,
                         'clean_sheets': 0, 'matches_played': 0})

        goalkeeper_data[player] = data

    return goalkeeper_data
