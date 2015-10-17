__author__ = 'gj'

DB_NAME = 'fpl-gw-{0}'.format('9')
COLLECTION_NAMES = ['teams', 'goalkeepers', 'defenders', 'midfielders', 'forwards',
                    'injuries']

PLAYER_TYPES = {'goalkeepers': 1, 'defenders': 2, 'midfielders': 3, 'forwards': 4}


TEAMS_MAP = {'Arsenal': 'ARS', 'Aston Villa': 'AVL',
             'Bournemouth': 'BOU', 'Chelsea': 'CHE',
             'Crystal Palace': 'CRY', 'Everton': 'EVE',
             'Leicester City': 'LEI', 'Liverpool': 'LIV',
             'Manchester United': 'MUN', 'Manchester City': 'MCI',
             'Newcastle United': 'NEW', 'Norwich City': 'NOR',
             'Southampton': 'SOU', 'Stoke City': 'STK',
             'Sunderland': 'SUN', 'Swansea City': 'SWA',
             'Tottenham Hotspur': 'TOT', 'Watford': 'WAT',
             'West Bromwich Albion': 'WBA', 'West Ham United': 'WHU'
             }


TEAMS_MAP2 = {'Arsenal': 'ARS', 'Aston Villa': 'AVL',
              'Bournemouth': 'BOU', 'Chelsea': 'CHE',
              'Crystal Palace': 'CRY', 'Everton': 'EVE',
              'Leicester': 'LEI', 'Liverpool': 'LIV',
              'Man Utd': 'MUN', 'Man City': 'MCI',
              'Newcastle': 'NEW', 'Norwich': 'NOR',
              'Southampton': 'SOU', 'Stoke': 'STK',
              'Sunderland': 'SUN', 'Swansea': 'SWA',
              'Spurs': 'TOT', 'Watford': 'WAT',
              'West Brom': 'WBA', 'West Ham': 'WHU'
              }

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

STAT_MAP = {'now_cost': 'price', 'total_points': 'score',
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

MONTHS = ['August', 'September', 'October', 'November', 'December', 'January',
          'February', 'March', 'April', 'May', 'June']
