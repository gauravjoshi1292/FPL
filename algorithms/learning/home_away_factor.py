__author__ = 'gj'

from utils import *
from mongo import DbManager


def get_home_away_wins_ratio():
    db_manger = DbManager(MONGODB_URL)
    results = db_manger.find(DB_NAME, 'results', {})

    home_wins, away_wins, draws, total = 0.0, 0.0, 0.0, 0.0
    for result in results:
        if result['win'] == 'home':
            home_wins += 1.0
        elif result['win'] == 'away':
            away_wins += 1.0
        else:
            draws += 1.0
        total += 1.0

    home_ratio = home_wins / total
    away_ratio = away_wins / total
    draw_ratio = draws / total

    return home_ratio, away_ratio, draw_ratio


def get_home_results_ratio_for_team(team):
    db_manger = DbManager(MONGODB_URL)
    home_results = db_manger.find(DB_NAME, 'results', {'home_team': team})

    home_wins, home_losses, home_draws, total = 0.0, 0.0, 0.0, 0.0
    for result in home_results:
        if result['win'] == 'home':
            home_wins += 1
        elif result['win'] == 'away':
            home_losses += 1
        else:
            home_draws += 1
        total += 1

    home_win_ratio = home_wins / total
    home_losses_ratio = home_losses / total
    home_draws_ratio = home_draws / total

    ratio = {'home_wins_ratio': home_win_ratio,
             'home_losses_ratio': home_losses_ratio,
             'home_draws_ratio': home_draws_ratio}
    return ratio


def get_away_results_ratio_for_team(team):
    db_manger = DbManager(MONGODB_URL)
    away_results = db_manger.find(DB_NAME, 'results', {'away_team': team})

    away_wins, away_losses, away_draws, total = 0.0, 0.0, 0.0, 0.0
    for result in away_results:
        if result['win'] == 'away':
            away_wins += 1
        elif result['win'] == 'home':
            away_losses += 1
        else:
            away_draws += 1
        total += 1

    away_win_ratio = away_wins / total
    away_losses_ratio = away_losses / total
    away_draws_ratio = away_draws / total

    ratio = {'away_wins_ratio': away_win_ratio,
             'away_losses_ratio': away_losses_ratio,
             'away_draws_ratio': away_draws_ratio}
    return ratio


def get_home_goals_per_game_for_team(team):
    db_manger = DbManager(MONGODB_URL)
    home_results = db_manger.find(DB_NAME, 'results', {'home_team': team})

    home_goals, total = 0.0, 0.0
    for result in home_results:
        home_goals += result['home_goals']
        total += 1

    gpg = home_goals / total
    return gpg


def get_away_goals_per_game_for_team(team):
    db_manger = DbManager(MONGODB_URL)
    away_results = db_manger.find(DB_NAME, 'results', {'away_team': team})

    away_goals, total = 0.0, 0.0
    for result in away_results:
        away_goals += result['away_goals']
        total += 1

    gpg = away_goals / total
    return gpg


if __name__ == '__main__':
    print get_home_away_wins_ratio()
    print get_home_results_ratio_for_team('ARS')
    print get_away_results_ratio_for_team('ARS')
    print get_home_goals_per_game_for_team('ARS')
    print get_away_goals_per_game_for_team('ARS')
