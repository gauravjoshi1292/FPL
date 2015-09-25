__author__ = 'gj'

from urls import *
from utils import normalize
from utils import get_soup_from_url


ALL_STAT_TYPES = {'now_cost': 4, 'total_points': 6, 'event_points': 5, 'minutes': 7,
                  'selected_by_percent': 3, 'assists': 7, 'clean_sheets': 7,
                  'yellow_cards': 7, 'red_cards': 7, 'saves': 7, 'bonus': 7,
                  'ea_index': 7, 'dreamteam_count': 7, 'form': 7, 'points_per_game': 7,
                  'bps': 7, 'goals_conceded': 7, 'goals_scored': 7, 'own_goals': 7,
                  'penalties_missed': 7, 'penalties_saved': 7, 'value_form': 7,
                  'value_season': 7, 'transfers_in': 7, 'transfers_out': 7,
                  'transfers_in_event': 7, 'transfers_out_event': 7,
                  'cost_change_start': 7, 'cost_change_start_fall': 7,
                  'cost_change_event': 7, 'cost_change_event_fall': 7}

STAT_MAPPING = {'now_cost': 'price', 'total_points': 'score',
                'event_points': 'round_score', 'minutes': 'minutes',
                'selected_by_percent': 'selected_by', 'assists': 'assists',
                'clean_sheets': 'clean_sheets', 'yellow_cards': 'yellow_cards',
                'red_cards': 'red_cards', 'saves': 'saves', 'bonus': 'bonus',
                'ea_index': 'ea_index', 'dreamteam_count': 'dreamteam_count',
                'form': 'form', 'points_per_game': 'ppg', 'bps': 'bps',
                'goals_conceded': 'goals_conceded', 'goals_scored': 'goals_scored',
                'own_goals': 'own_goals', 'penalties_missed': 'penalties_missed',
                'penalties_saved': 'penalties_saved', 'value_form': 'value_form',
                'value_season': 'value_season', 'transfers_in': 'transfers_in',
                'transfers_out': 'transfers_out',
                'transfers_in_event': 'transfers_in_week',
                'transfers_out_event': 'transfers_out_week',
                'cost_change_start': 'price_rise',
                'cost_change_start_fall': 'price_fall',
                'cost_change_event': 'price_rise_week',
                'cost_change_event_fall': 'price_fall_week'}


def get_stat_from_text(text, stats_type):
    """
    Returns a value by converting string to appropriate type

    :param text: text to be converted
    :type text: str

    :param stats_type: type of stat

    :rtype: int | float
    """
    if stats_type in ['transfers_in', 'transfers_out', 'transfers_in_event',
                      'transfers_out_event']:
        return int(text.replace(',', ''))

    elif stats_type in ['now_cost', 'form', 'points_per_game', 'value_form',
                        'value_season', 'cost_change_start', 'cost_change_start_fall',
                        'cost_change_event', 'cost_change_event_fall']:
        return float(text)

    elif stats_type == 'selected_by_percent':
        return float(text.strip('%'))

    return int(text)


def get_table_from_url(url, table_class):
    """
    Given a url and table class, returns the table element with that class

    :param url: page url
    :type url: str

    :param table_class: table class
    :type table_class: str

    :rtype: bs4.element.ResultSet
    """
    soup = get_soup_from_url(url=url)
    table = soup.find('table', {'class': table_class})

    if not table:
        return []

    tds = table.findAll('td', {'class': None})
    return tds


def scrape_stat_from_table(url_template, stat_type, table_class, column):
    """
    Scrapes and returns statistic from the table

    :param url_template: page url template
    :type url_template: str

    :param stat_type: type of stat
    :type stat_type: str

    :param table_class: table class
    :type table_class: str

    :param column: column that contains stat
    :type column: int

    :rtype: dict[(str, str), int | float]
    """
    data = {}

    page = 1
    while True:
        url = url_template.format(stat_type=stat_type, page=page)
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
                    value = get_stat_from_text(normalize(td.text), stat_type)
                    data[(name, team)] = value
                    name = ''
                    team = ''
                    check = False
                    continue

                i += 1
        page += 1

    return data


def add_stat_to_dictionary(data_dict, stat, stat_type):
    """
    Adds statistics to the dictionary of all players

    :param data_dict: dictionary containing players
    :type data_dict: dict[(str, str), dict[str, int | float]]

    :param stat: dictionary containing stat
    :type stat: dict[(str, str), int | float]

    :param stat_type: type of stat
    :type stat_type: str
    """
    for player, value in stat.items():
        try:
            data_dict[player][STAT_MAPPING[stat_type]] = value
        except KeyError:
            data_dict[player] = {}
            data_dict[player][STAT_MAPPING[stat_type]] = value


def get_goalkeeper_stats():
    """
    Returns all the statistics for keepers

    :rtype: dict[(str, str), dict[str, int | float]]
    """
    goalkeeper_stats = {}

    for stat_type, column in ALL_STAT_TYPES.items():
        stat = scrape_stat_from_table(url_template=GOALKEEPER_STATS_URL,
                                      stat_type=stat_type,
                                      table_class='ismTable',
                                      column=column)

        add_stat_to_dictionary(data_dict=goalkeeper_stats, stat=stat, stat_type=stat_type)

    return goalkeeper_stats


print get_goalkeeper_stats()
