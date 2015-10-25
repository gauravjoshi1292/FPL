__author__ = 'gj'

from urls import FIXTURES_URL
from utils import get_soup_from_url
from global_variables import TEAMS_MAP2


def get_fixtures():
    """
    Returns all future fixtures for teams

    :rtype: dict
    """
    fixtures = {}

    soup = get_soup_from_url(FIXTURES_URL)
    tds = soup.find_all('td', {'class': 'clubs'})

    for td in tds:
        match = str(td.find('a').text)
        team1, team2 = map(lambda x: TEAMS_MAP2[x], match.split(' v '))

        try:
            fixtures[team1].append({'team': team2, 'place': 'home'})
        except KeyError:
            fixtures[team1] = [{'team': team2, 'place': 'home'}]
        try:
            fixtures[team2].append({'team': team1, 'place': 'away'})
        except KeyError:
            fixtures[team2] = [{'team': team1, 'place': 'away'}]

    return fixtures
