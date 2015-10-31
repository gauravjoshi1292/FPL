__author__ = 'gj'

from global_variables import *

MONGODB_URL = "mongodb://localhost:{port}".format(port=MONGODB_PORT)

TEAM_STATS_URL = ("http://www.premierleague.com/en-gb/matchday/league-table.html?"
                  "season=2015-2016&month=MAY&timelineView=date&toDate=1432422000000&"
                  "tableView=CURRENT_STANDINGS")

FIXTURES_URL = ("http://www.premierleague.com/en-gb/matchday/matches.html?"
                "paramClubId=ALL&paramComp_8=true&view=.dateSeason")

GAMEWEEK_FIXTURES_AND_RESULTS_URL = ("http://www.livefootball.co.uk/premier-league/"
                                     "2015-2016/regular-season/"
                                     "gameweek-{week}")

PLAYER_LIST_URL = "http://fantasy.premierleague.com/player-list/"

PLAYER_STATS_URL = ("http://fantasy.premierleague.com/stats/elements/?"
                    "element_filter=et_{player_type}&"
                    "stat_filter={stat_type}&"
                    "page={page}")

INJURIES_URL = "http://www.fantasyfootballscout.co.uk/fantasy-football-injuries/"

RESULTS_URL = ("http://www.premierleague.com/content/premierleague/en-gb/matchday/"
               "results.html?paramClubId=ALL&paramComp_8=true&paramComp_1=true&"
               "paramComp_2=true&paramComp_5=true&paramComp_6=true&"
               "paramSeasonId={year}&view=.dateSeason")
