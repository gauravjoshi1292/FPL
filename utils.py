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
