__author__ = 'gj'

from urls import *
from utils import normalize
from utils import get_soup_from_url


def get_table_from_url(url, table_class):
    soup = get_soup_from_url(url=url)
    table = soup.find('table', {'class': table_class})
    tds = table.findAll('td', {'class': None})
    return tds


def scrape_stats_from_table(url_template, stats_type, table_class, column):
    data = {}

    page = 1
    while True:
        url = url_template.format(stats_type=stats_type, page=page)
        table = get_table_from_url(url=url, table_class=table_class)

        if not table:
            break

        name, team, value, i = '', '', 0, 0
        for td in table:
            try:
                td['class']
            except KeyError:
                if i == 2:
                    name = normalize(td.text)
                elif i == 3:
                    team = normalize(td.text)
                elif i == column:
                    value = float(normalize(td.text))

                if i == 8:
                    data[(name, team)] = value
                    i = 0
                    name = ''
                    team = ''
                    value = 0
                    continue

                i += 1
        page += 1

    return data
    

def get_goalkeeper_scores():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='total_points',
                                   table_class='ismTable',
                                   column=8)


def get_goalkeeper_prices():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='now_cost',
                                   table_class='ismTable',
                                   column=6)


def get_goalkeeper_round_scores():
    return scrape_stats_from_table(url_template=GOALKEEPER_STATS_URL,
                                   stats_type='total_points',
                                   table_class='ismTable',
                                   column=7)


print get_goalkeeper_scores()
print get_goalkeeper_prices()
print get_goalkeeper_round_scores()
