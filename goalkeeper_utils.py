__author__ = 'gj'

from urls import *
from utils import normalize
from utils import get_soup_from_url


def get_table_from_url(url, table_class):
    soup = get_soup_from_url(url=url)
    table = soup.find('table', {'class': table_class})
    tds = table.findAll('td', {'class': None})
    return tds


def get_stat_from_text(text, stats_type):
    if stats_type == 'now_cost':
        return float(text)
    elif stats_type == 'selected_by_percent':
        return float(text.strip('%'))

    return int(text)


def scrape_stats_from_table(url_template, stats_type, table_class, column):
    data = {}

    page = 1
    while True:
        url = url_template.format(stats_type=stats_type, page=page)
        table = get_table_from_url(url=url, table_class=table_class)

        if not table:
            break

        name, team, value, i, check = '', '', 0, 0, False
        for td in table:
            if len(td.findChildren()) == 1:
                continue

            if len(td.findChildren()) == 2:
                i = 0
                check = True
                continue

            if check:
                if i == 0:
                    name = normalize(td.text)
                elif i == 1:
                    team = normalize(td.text)
                elif i == column:
                    value = get_stat_from_text(normalize(td.text), stats_type)
                    data[(name, team)] = value
                    name = ''
                    team = ''
                    check = False
                    continue

                i += 1
        page += 1

    return data
    

def get_goalkeeper_scores():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='total_points',
                                   table_class='ismTable',
                                   column=6)


def get_goalkeeper_prices():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='now_cost',
                                   table_class='ismTable',
                                   column=4)


def get_goalkeeper_round_scores():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='total_points',
                                   table_class='ismTable',
                                   column=5)


def get_goalkeeper_minutes_played():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='minutes',
                                   table_class='ismTable',
                                   column=7)


def get_goalkeeper_selected_by_percent():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='selected_by_percent',
                                   table_class='ismTable',
                                   column=3)


def get_goalkeeper_goals_scored():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='goals_scored',
                                   table_class='ismTable',
                                   column=7)


def get_goalkeeper_assists():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='assists',
                                   table_class='ismTable',
                                   column=7)


def get_goalkeeper_clean_sheets():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='clean_sheets',
                                   table_class='ismTable',
                                   column=7)


# print get_goalkeeper_scores()
# print get_goalkeeper_prices()
# print get_goalkeeper_round_scores()
# print get_goalkeeper_minutes_played()
# print get_goalkeeper_selected_by_percent()
# print get_goalkeeper_goals_scored()
# print get_goalkeeper_assists()
print get_goalkeeper_clean_sheets()