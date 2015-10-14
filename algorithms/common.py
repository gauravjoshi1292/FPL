__author__ = 'gj'


def get_stat_rating(val, max_val, min_val):
    """
    Returns linearly normalized rating corresponding to the given stat value

    :param val: stat value
    :type val: int | float

    :param max_val: maximum possible value for the stat
    :type max_val: int | float

    :param min_val: minimum possible value for the stat
    :type min_val: int | float

    :rtype: float
    """
    if val == 0:
        return 0.0
    return float(val - min_val) / (max_val - min_val)


def get_normalized_ratings(ratings, max_val, min_val, min_range=0.0, max_range=1.0):
    """
    Returns normalized values corresponding to passed ratings

    :param ratings: rating values
    :type ratings: dict

    :param max_val: maximum possible rating value
    :type max_val: float

    :param min_val: minimum possible rating value
    :type min_val: float

    :param min_range: lower limit for the normalization range
    :type min_range: float

    :param max_range: upper limit for the normalization range
    :type max_range: float

    :rtype: dict
    """
    normalized_ratings = {}

    for key, rating in ratings.items():
        normalized_val = (rating - min_val) / (max_val - min_val)
        normalized_ratings[key] = min_range + (normalized_val * (max_range - min_range))

    return normalized_ratings


def get_rating_for_n_fixtures(team, fixtures, points, n):
    """
    Returns rating for the next n fixtures based on their ease/difficulty

    :param team: team name
    :type team: str

    :param fixtures: fixtures corresponding to the team
    :type fixtures: list

    :param points: league table points corresponding to all the teams
    :type points: dict

    :param n: number of fixtures to consider
    :type n: int

    :rtype: float
    """
    if n > len(fixtures):
        n = len(fixtures)

    rating = 0.0
    fixtures = fixtures[0:n]
    day_factor = 1.0

    for fixture in fixtures:
        opposition = fixture['team']
        place = fixture['place']
        rating += day_factor * (points[team] - points[opposition])

        if place == 'home':
            if rating >= 0:
                rating *= 1.5

            if rating < 0:
                rating /= 1.5

        day_factor /= 2

    return rating


def get_max_fixture_rating(points, n):
    """
    Returns the best possible fixture rating

    :param points: league table points corresponding to all the teams
    :type points: dict

    :param n: number of fixtures to consider
    :type n: int

    :rtype: float
    """
    table = sorted(points.items(), key=lambda x: x[1], reverse=True)
    best_team = table[0][0]

    fixtures = []
    total_teams = len(table)
    for team, _ in table[:total_teams-n-1:-1]:
        fixtures.append({'team': team, 'place': 'home'})

    max_fixture_rating = get_rating_for_n_fixtures(best_team, fixtures, points, n)

    return max_fixture_rating


def get_min_fixture_rating(points, n):
    """
    Returns the worst possible fixture rating

    :param points: league table points corresponding to all the teams
    :type points: dict

    :param n: number of fixtures to consider
    :type n: int

    :rtype: float
    """
    table = sorted(points.items(), key=lambda x: x[1], reverse=True)
    worst_team = table[-1][0]

    fixtures = []
    for team, _ in table[:n]:
        fixtures.append({'team': team, 'place': 'away'})

    min_fixture_rating = get_rating_for_n_fixtures(worst_team, fixtures, points, n)

    return min_fixture_rating


def get_fixture_rating(team_stats, n_fixtures):
    """
    Returns normalized fixture ratings for all the teams

    :param team_stats: team statistics
    :type team_stats: dict

    :param n_fixtures: number of fixtures to consider
    :type n_fixtures: int

    :rtype: dict
    """
    ratings = {}

    points = {}
    all_fixtures = {}
    for team, stats in team_stats.items():
        points[team] = stats['points']
        all_fixtures[team] = stats['fixtures']

    max_rating = get_max_fixture_rating(points, n_fixtures)
    min_rating = get_min_fixture_rating(points, n_fixtures)

    for team, fixtures in all_fixtures.items():
        team = team
        rating = get_rating_for_n_fixtures(team, fixtures, points, n_fixtures)
        ratings[team] = rating

    fixture_ratings = get_normalized_ratings(ratings, max_rating, min_rating, 0.0, 5.0)

    return fixture_ratings


def get_max_and_min(player_stats):
    """
    Returns maximum and minimum values corresponding to all the statistics

    :param player_stats: player statistics
    :type player_stats: dict

    :rtype: dict, dict
    """
    max_values = {}
    min_values = {}
    for player, stats in player_stats.items():
        for key, val in stats.items():
            if key == 'team':
                continue

            try:
                if stats[key] > max_values[key] and stats['minutes']:
                    max_values[key] = stats[key]
            except KeyError:
                if stats['minutes']:
                    max_values[key] = stats[key]

            try:
                if stats[key] < min_values[key] and stats['minutes']:
                    min_values[key] = stats[key]
            except KeyError:
                if stats['minutes']:
                    min_values[key] = stats[key]

    return max_values, min_values
