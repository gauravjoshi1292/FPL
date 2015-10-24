__author__ = 'gj'

from datetime import datetime

from utils import *
from global_variables import *


def build_results(day_results, team_a, team_b, score, location, date, kickoff, comp):
    date_obj = datetime.strptime(date, '%A %d %B %Y')
    kickoff_obj = datetime.strptime('{0} {1}'.format(date, kickoff), '%A %d %B %Y %H:%M')

    goals_for, goals_against = map(int, score.split(' - '))
    if goals_for > goals_against:
        result_a = 'win'
        result_b = 'loss'
    elif goals_for < goals_against:
        result_a = 'loss'
        result_b = 'win'
    else:
        result_a = 'draw'
        result_b = 'draw'

    match_info_a = {'opposition': team_b, 'place': 'home', 'result': result_a,
                    'goals_for': goals_for, 'goals_against': goals_against, 'comp': comp,
                    'location': location, 'date': date_obj, 'time': kickoff_obj}

    match_info_b = {'opposition': team_a, 'place': 'away', 'result': result_b,
                    'goals_for': goals_against, 'goals_against': goals_for, 'comp': comp,
                    'location': location, 'date': date_obj, 'time': kickoff_obj}

    try:
        day_results[team_a].append(match_info_a)
    except KeyError:
        day_results[team_a] = [match_info_a]

    try:
        day_results[team_b].append(match_info_b)
    except KeyError:
        day_results[team_b] = [match_info_b]


def extract_results_from_table(table):
    day_results = {}
    rows = table.find_all('tr')

    team_a, team_b, score, location, date, kickoff, competition = '', '', '', '', '', '', ''
    for row in rows:
        cols = row.find_all(['th', 'td'])
        for col in cols:
            if col.name == 'th':
                date = normalize(col.text.strip())
                span = col.find('span')
                competition = normalize(span['title'].strip())
                continue

            try:
                if col['class'][0] == 'time':
                    kickoff = normalize(col.text.strip())
                elif col['class'] == ['clubs', 'rHome']:
                    team_a = normalize(col.text.strip())
                elif col['class'] == ['clubs', 'rAway']:
                    team_b = normalize(col.text.strip())
                elif col['class'] == ['clubs', 'score']:
                    score = normalize(col.text.strip())
                elif col['class'][0] == 'location':
                    location = normalize(col.text.strip())
                    build_results(day_results, team_a, team_b, score,
                                  location, date, kickoff, competition)
                    team_a, team_b, score, location, kickoff = '', '', '', '', '',
            except KeyError:
                continue

    return day_results


def get_results_for_year(url):
    yearly_results = {}

    driver = get_driver(url)
    scroll_till_page_is_loaded(driver)
    soup = get_soup_from_driver(driver)
    driver.quit()
    #
    # with open('data/soup.txt', 'r') as fp:
    #     from bs4 import BeautifulSoup
    #     soup = BeautifulSoup(fp.read(), 'html.parser')

    tables = soup.find_all('table', {'class': 'contentTable'})
    for table in tables:
        day_results = extract_results_from_table(table)
        for key, val in day_results.items():
            try:
                yearly_results[key].extend(val)
            except KeyError:
                yearly_results[key] = val

    return yearly_results


def get_results():
    results = {}

    year = YEAR - 5
    while year <= YEAR:
        url = RESULTS_URL.format(year=year)
        yearly_results = get_results_for_year(url)
        for key, val in yearly_results.items():
            try:
                results[key].extend(val)
            except KeyError:
                results[key] = val

        year += 1
    return results


def create_results_database():
    results_db_manager = DbManager(MONGODB_URL)
    # results_db_manager.drop_db(RESULTS_DB)
    # results_db_manager.create_db(RESULTS_DB)
    #
    # results = get_results()
    #
    # for team, data in results.items():
    #     results_db_manager.create_collection(RESULTS_DB, team)
    #     results_db_manager.insert(RESULTS_DB, team, data)

    print results_db_manager.client[RESULTS_DB].collection_names()


if __name__ == '__main__':
    create_results_database()
