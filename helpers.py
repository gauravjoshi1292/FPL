__author__ = 'gj'

import urllib2
from bs4 import BeautifulSoup
from urls import *


def get_soup_from_url(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_table_data():
    table_data = {}
    team_data = {}
    team_name = ""
    soup = get_soup_from_url(LEAGUE_TABLE_URL)
    tds = soup.findAll("td")
    keys = ["played", "won", "drawn", "lost", "goals_for", "goals_against", "goal_diff", "points"]

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
                player_name = td.text.encode('ascii', 'ignore')
            elif j == 1:
                player_data["team"] = td.text.encode('ascii', 'ignore')
            elif j == 2:
                player_data["points"] = int(td.text)
            elif j == 3:
                player_data["price"] = td.text.encode('ascii', 'ignore')
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
                player_name = td.text.encode('utf-8')
                continue

            j += 1

        i += 1

    return goalkeepers, defenders, midfielders, forwards


def get_clean_sheets():
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get(GOALKEEPER_CLEAN_SHEETS)

    e1 = driver.find_element_by_xpath("//option[@value='Goalkeeper Stats']")
    e2 = driver.find_element_by_xpath("//option[@value='18'][@class='gkeeper']")

    print e1.text
    print e2.text

    # e1.click()
    # e2.click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    source = driver.page_source
    print source

    soup = BeautifulSoup(source)
    print soup

# print get_table_data()
# print get_player_list()
get_clean_sheets()