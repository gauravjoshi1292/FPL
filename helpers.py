__author__ = 'gj'

import time
import datetime
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from urls import *


def get_soup_from_url(url):
    """
    Given a url returns a soup of page source
    :param url: web url
    :return:
    """
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
    soup = get_soup_from_url(LEAGUE_TABLE_URL)
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
    soup = get_soup_from_url(PLAYER_LIST_URL)

    tables = soup.findAll("table")
    i = 0
    for table in tables:
        tds = table.findAll("td")
        player_name = ""
        player_data = {}

        j = 0
        for td in tds:
            if j == 0:
                player_name = td.text.encode("ascii", "ignore")
            elif j == 1:
                player_data["team"] = td.text.encode("ascii", "ignore")
            elif j == 2:
                player_data["points"] = int(td.text)
            elif j == 3:
                player_data["price"] = td.text.encode("ascii", "ignore")
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
                player_name = td.text.encode("utf-8")
                continue

            j += 1

        i += 1

    return goalkeepers, defenders, midfielders, forwards


def get_chrome_driver(url):
    """
    Returns a selenium chrome driver
    :param url:
    :type url: str
    :return:
    """
    driver = webdriver.Chrome()
    driver.get(url)
    return driver


def get_firefox_driver(url):
    """
    Returns a selenium firefox driver

    :param url:
    :type url: str

    :return:
    """
    driver = webdriver.Firefox()
    driver.get(url)
    return driver


def get_safari_driver(url):
    """
    Returns a selenium safari driver

    :param url:
    :type url: str

    :return:
    """
    driver = webdriver.Safari()
    driver.get(url)
    return driver


def get_driver(url):
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


def scroll_to_element(driver, tag_name):
    """
    Scroll to elements location in driver's web page
    :param driver:
    :type tag_name: str
    """
    table_elem = driver.find_element_by_tag_name(tag_name)
    webdriver.ActionChains(driver).move_to_element(table_elem).perform()


def get_soup_from_driver(driver):
    """
    Given a selenium web driver return the soup
    :param driver:
    :return:
    """
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")
    return soup


def get_clean_sheets():
    """
    Returns clean sheet data for all the keepers
    :return:
    """
    clean_sheet_data = {}
    date = datetime.datetime.strptime(str(datetime.date.today()),
                                      "%Y-%m-%d").strftime("%d/%m/%Y")

    url = GOALKEEPING_STATS_URL.format(stats_type="clean-sheets", curr_date=date)
    driver = get_driver(url=url)

    scroll_to_element(driver, "footer")
    time.sleep(1)
    soup = get_soup_from_driver(driver)
    table = soup.find("table", id="ranking-stats-table")

    tds = table.findAll("td")
    i = 0
    name, team, matches_played, minutes_played, clean_sheets = "", "", 0, 0, 0
    for td in tds:
        try:
            if td["class"][0] == "table-playerteam-field":
                name = td.find_next("div", {"class": "stats-player-name"}).text.encode(
                    "ascii", "ignore")
                team = td.find_next("div", {"class": "stats-player-team"}).text.encode(
                    "ascii", "ignore").split(" - ")[1]
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
    driver.quit()
    return clean_sheet_data


def get_saves():
    """

    :return:
    """
    saves_data = {}
    date = datetime.datetime.strptime(str(datetime.date.today()),
                                      "%Y-%m-%d").strftime("%d/%m/%Y")

    url = GOALKEEPING_STATS_URL.format(stats_type="saves", curr_date=date)
    driver = get_driver(url)

    scroll_to_element(driver, "footer")
    time.sleep(1)
    soup = get_soup_from_driver(driver)
    table = soup.find("table", id="ranking-stats-table")

    tds = table.findAll("td")
    i = 0
    name, saves = "", 0
    for td in tds:
        try:
            if td["class"][0] == "table-playerteam-field":
                name = td.find_next("div", {"class": "stats-player-name"}).text.encode(
                    "ascii", "ignore")
                continue
        except KeyError:
            if i == 5:
                i = 0
                saves = int(td.text)
                saves_data[name] = {"saves": saves}
                continue
            else:
                i += 1

    driver.quit()
    return saves_data


def get_goals_conceded():
    """

    :return:
    """
    goals_conceded_data = {}
    date = datetime.datetime.strptime(str(datetime.date.today()),
                                      "%Y-%m-%d").strftime("%d/%m/%Y")

    url = GOALKEEPING_STATS_URL.format(stats_type="goals-conceded", curr_date=date)
    driver = get_driver(url)

    scroll_to_element(driver, "footer")
    time.sleep(1)
    soup = get_soup_from_driver(driver)
    table = soup.find("table", id="ranking-stats-table")

    tds = table.findAll("td")
    i = 0
    name, saves = "", 0
    for td in tds:
        try:
            if td["class"][0] == "table-playerteam-field":
                name = td.find_next("div", {"class": "stats-player-name"}).text.encode(
                    "ascii", "ignore")
                continue
        except KeyError:
            if i == 8:
                i = 0
                goals_conceded = int(td.text)
                goals_conceded_data[name] = {"goals_conceded": goals_conceded}
                continue
            else:
                i += 1

    driver.quit()
    return goals_conceded_data

# print get_league_table_data()
# print get_player_list()
# print get_clean_sheets()
# print get_saves()
print get_goals_conceded()
