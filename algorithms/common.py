__author__ = 'gj'


def get_stat_rating(val, max_val, min_val):
    if val == 0:
        return 0.0
    return float(val - min_val) / (max_val - min_val)


def get_normalized_ratings(ratings, max_val, min_val, min_range=0.0, max_range=1.0):
    normalized_ratings = {}

    for team, rating in ratings.items():
        normalized_val = (rating - min_val) / (max_val - min_val)
        normalized_ratings[team] = min_range + (normalized_val * (max_range - min_range))

    return normalized_ratings


def get_rating_for_n_fixtures(team, fixtures, points, n):
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
    table = sorted(points.items(), key=lambda x: x[1], reverse=True)
    best_team = table[0][0]

    fixtures = []
    total_teams = len(table)
    for team, _ in table[:total_teams-n-1:-1]:
        fixtures.append({'team': team, 'place': 'home'})

    max_fixture_rating = get_rating_for_n_fixtures(team=best_team, fixtures=fixtures,
                                                   points=points, n=n)

    return max_fixture_rating


def get_min_fixture_rating(points, n):
    table = sorted(points.items(), key=lambda x: x[1], reverse=True)
    worst_team = table[-1][0]

    fixtures = []
    for team, _ in table[:n]:
        fixtures.append({'team': team, 'place': 'away'})

    min_fixture_rating = get_rating_for_n_fixtures(team=worst_team, fixtures=fixtures,
                                                   points=points, n=n)

    return min_fixture_rating


def get_fixture_rating(team_stats, n_fixtures):
    ratings = {}

    points = {}
    fixtures = {}
    for stats in team_stats:
        points[stats['team']] = stats['points']
        fixtures[stats['team']] = stats['fixtures']

    max_rating = get_max_fixture_rating(points=points, n=n_fixtures)
    min_rating = get_min_fixture_rating(points=points, n=n_fixtures)

    for team in fixtures:
        team = team
        rating = get_rating_for_n_fixtures(team=team, fixtures=fixtures[team],
                                           points=points, n=n_fixtures)
        ratings[team] = rating

    fixture_ratings = get_normalized_ratings(ratings=ratings, max_val=max_rating,
                                             min_val=min_rating, min_range=0.0,
                                             max_range=5.0)

    return fixture_ratings


def get_max_and_min(player_stats):
    max_values = {}
    min_values = {}
    for stat in player_stats:
        for key in stat:
            if key in ['_id', 'name', 'team']:
                continue

            try:
                if stat[key] > max_values[key] and stat['minutes']:
                    max_values[key] = stat[key]
            except KeyError:
                if stat['minutes']:
                    max_values[key] = stat[key]

            try:
                if stat[key] < min_values[key] and stat['minutes']:
                    min_values[key] = stat[key]
            except KeyError:
                if stat['minutes']:
                    min_values[key] = stat[key]

    return max_values, min_values
