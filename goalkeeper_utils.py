__author__ = 'gj'

from urls import *
from utils import get_soup_from_url


def get_goalkeepers_points():
    goalkeeper_points = {}
    url = GOALKEEPER_POINTS
    soup = get_soup_from_url(url=url)
    table = soup.find("table", {"class": "ismTable"})
    print table
    

get_goalkeepers_points()
