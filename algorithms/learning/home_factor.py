__author__ = 'gj'

from utils import *
from mongo import DbManager


def calibrate():
    db_manger = DbManager('mongodb://localhost:27017')
    results = db_manger.find(DB_NAME, 'results', {})

    home_wins = 0
    away_wins = 0
    draws = 0
    for result in results:
        if result['win'] == 'home':
            home_wins += 1
        elif result['win'] == 'away':
            away_wins += 1
        else:
            draws += 1

    print home_wins, away_wins, draws


if __name__ == '__main__':
    calibrate()
