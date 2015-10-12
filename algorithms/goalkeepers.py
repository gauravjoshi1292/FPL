__author__ = 'gj'

from mongo import FplManager


SCORE_WT = 10.0
CS_WT = 7.0
GC_WT = -1.0
SAVES_WT = 1.0
FORM_WT = 9.0
RS_WT = 7.0
MINUTES_WT = 3.0

WT_SUM = SCORE_WT + CS_WT + GC_WT + SAVES_WT + FORM_WT + RS_WT + MINUTES_WT

FIXTURES_LIM = 5


def get_stat_rating(val, max_val, min_val):
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


def get_fixture_rating(team_stats):
    ratings = {}

    points = {}
    fixtures = {}
    for stats in team_stats:
        points[stats['team']] = stats['points']
        fixtures[stats['team']] = stats['fixtures']

    max_rating = get_max_fixture_rating(points=points, n=FIXTURES_LIM)
    min_rating = get_min_fixture_rating(points=points, n=FIXTURES_LIM)

    for team in fixtures:
        team = team
        rating = get_rating_for_n_fixtures(team=team, fixtures=fixtures[team],
                                           points=points, n=FIXTURES_LIM)
        ratings[team] = rating

    fixture_ratings = get_normalized_ratings(ratings=ratings,
                                             max_val=max_rating,
                                             min_val=min_rating,
                                             min_range=0.0,
                                             max_range=5.0)

    return fixture_ratings


def get_goalkeeper_rating(stats, maxs, mins):
    if stats['minutes'] == 0:
        return 0

    score_rating = get_stat_rating(stats['score'], maxs['score'], mins['score'])
    cs_rating = get_stat_rating(stats['clean_sheets'], maxs['clean_sheets'],
                                mins['clean_sheets'])
    gc_rating = get_stat_rating(stats['goals_conceded'], maxs['goals_conceded'],
                                mins['goals_conceded'])
    saves_rating = get_stat_rating(stats['saves'], maxs['saves'], mins['saves'])
    form_rating = get_stat_rating(stats['form'], maxs['form'], mins['form'])
    rs_rating = get_stat_rating(stats['round_score'], maxs['round_score'],
                                mins['round_score'])
    minutes_rating = get_stat_rating(stats['minutes'], maxs['minutes'], mins['minutes'])

    rating = (SCORE_WT*score_rating + CS_WT*cs_rating + GC_WT*gc_rating +
              SAVES_WT*saves_rating + FORM_WT*form_rating + RS_WT*rs_rating +
              MINUTES_WT*minutes_rating) * 5.0 / WT_SUM

    return rating


def get_max_and_min(player_stats):
    maxs = {}
    mins = {}
    for stat in player_stats:
        for key in stat:
            if key in ['_id', 'name', 'team']:
                continue

            try:
                if stat[key] > maxs[key] and stat['minutes']:
                    maxs[key] = stat[key]
            except KeyError:
                if stat['minutes']:
                    maxs[key] = stat[key]

            try:
                if stat[key] < mins[key] and stat['minutes']:
                    mins[key] = stat[key]
            except KeyError:
                if stat['minutes']:
                    mins[key] = stat[key]

    return maxs, mins


def calculate_goalkeeper_ratings(manager, db_name, collection_name):
    goalkeeper_ratings = {}
    goalkeeper_entries = manager.client[db_name][collection_name].find()
    team_entries = manager.client[db_name]['teams'].find()

    maxs, mins = get_max_and_min(player_stats=goalkeeper_entries)
    fixture_ratings = get_fixture_rating(team_stats=team_entries)
    print fixture_ratings

    goalkeeper_entries.rewind()
    for goalkeeper_entry in goalkeeper_entries:
        absolute_rating = get_goalkeeper_rating(stats=goalkeeper_entry, maxs=maxs,
                                                mins=mins)
        affected_rating = (absolute_rating + fixture_ratings[goalkeeper_entry['team']]) / 2.0

        goalkeeper_ratings[(goalkeeper_entry['name'], goalkeeper_entry['team'])] = affected_rating

    return goalkeeper_ratings


fpl_manager = FplManager(uri='mongodb://localhost:27017')

gr = calculate_goalkeeper_ratings(manager=fpl_manager, db_name='fpl',
                                  collection_name='goalkeepers')
print sorted(gr.items(), key=lambda x: x[1], reverse=True)

fpl_manager.close_connection()
