__author__ = 'gj'

import json
import time
import socket
import urllib2
import unicodedata
from bson import json_util
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


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
        time.sleep(5)
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

    tds = table.find_all('td')
    return tds


def dump_as_json(data, json_file):
    """
    Dumps the data into a json file

    :type data: dict

    :type json_file: str
    """
    with open(json_file, "w") as outfile:
        json.dump(data, outfile, indent=4, default=json_util.default)


def load_as_json(json_file):
    """
    Loads the json file and returns a json object

    :param json_file: input json file
    :type json_file: str

    :rtype: dict
    """
    with open(json_file, "r") as infile:
        data = json.load(infile, object_hook=json_util.object_hook)

    return data
