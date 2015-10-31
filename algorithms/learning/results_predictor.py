__author__ = 'gj'

from crawlers.gw_results_and_fixtures_crawler import get_gameweek_fixtures_and_results
from db.query_handler import QueryHandler


def get_ratios(results):
    total, wins, losses, draws = 0.0, 0.0, 0.0, 0.0

    for match in results:
        if match['result'] == 'win':
            wins += 1
        elif match['result'] == 'loss':
            losses += 1
        elif match['result'] == 'draw':
            draws += 1
        total += 1

    if total == 0:
        total = 1

    return {'wins': wins/total, 'losses': losses/total, 'draws': draws/total}


def get_home_team_score(team, opposition):
    qhandler = QueryHandler()
    last_five_results = qhandler.get_last_n_results(team, n=5)
    last_five_home_results = qhandler.get_last_n_results(team, n=5, place='home')
    last_five_away_results = qhandler.get_last_n_results(team, n=5, place='away')

    last_four_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)
    last_four_home_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)
    last_four_away_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)

    ratios_overall = get_ratios(last_five_results)
    ratios_overall_home = get_ratios(last_five_home_results)
    ratios_overall_away = get_ratios(last_five_away_results)

    ratios_opposition = get_ratios(last_four_results_against)
    ratios_opposition_home = get_ratios(last_four_home_results_against)
    ratios_opposition_away = get_ratios(last_four_away_results_against)

    home_win_score = ratios_overall['wins'] + ratios_overall_home['wins'] + ratios_opposition['wins'] + ratios_opposition_home['wins']
    home_loss_score = ratios_overall['losses'] + ratios_overall_home['losses'] + ratios_opposition['losses'] + ratios_opposition_home['losses']
    home_draw_score = ratios_overall['draws'] + ratios_overall_home['draws'] + ratios_opposition['draws'] + ratios_opposition_home['draws']

    return home_win_score, home_loss_score, home_draw_score


def get_away_team_score(team, opposition):
    qhandler = QueryHandler()
    last_five_results = qhandler.get_last_n_results(team, n=5)
    last_five_home_results = qhandler.get_last_n_results(team, n=5, place='home')
    last_five_away_results = qhandler.get_last_n_results(team, n=5, place='away')

    last_four_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)
    last_four_home_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)
    last_four_away_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)

    ratios_overall = get_ratios(last_five_results)
    ratios_overall_home = get_ratios(last_five_home_results)
    ratios_overall_away = get_ratios(last_five_away_results)

    ratios_opposition = get_ratios(last_four_results_against)
    ratios_opposition_home = get_ratios(last_four_home_results_against)
    ratios_opposition_away = get_ratios(last_four_away_results_against)

    away_win_score = ratios_overall['wins'] + ratios_overall_away['wins'] + ratios_opposition['wins'] + ratios_opposition_away['wins']
    away_loss_score = ratios_overall['losses'] + ratios_overall_away['losses'] + ratios_opposition['losses'] + ratios_opposition_away['losses']
    away_draw_score = ratios_overall['draws'] + ratios_overall_away['draws'] + ratios_opposition['draws'] + ratios_opposition_away['draws']

    return away_win_score, away_loss_score, away_draw_score


def predict_result(home_team, away_team):
    home_win_score, home_loss_score, home_draw_score = get_home_team_score(home_team, away_team)
    away_win_score, away_loss_score, away_draw_score = get_home_team_score(away_team, home_team)

    home_win_prob = home_win_score + away_loss_score
    away_win_prob = home_loss_score + away_win_score
    draw_prob = home_draw_score + away_draw_score

    # print home_win_prob, away_win_prob, draw_prob

    if home_win_prob > away_win_prob and home_win_prob > draw_prob:
        print home_team
    elif away_win_prob > home_win_prob and away_win_prob > draw_prob:
        print away_team
    elif draw_prob > home_win_prob and draw_prob > away_win_prob:
        print 'DRAW'

if __name__ == '__main__':
    predict_result('Chelsea', 'Liverpool')
    predict_result('Crystal Palace', 'Manchester United')
    predict_result('Manchester City', 'Norwich City')
    predict_result('Newcastle United', 'Stoke City')
    predict_result('Swansea City', 'Arsenal')
    predict_result('Watford', 'West Ham United')
    predict_result('West Bromwich Albion', 'Leicester City')
    predict_result('Everton', 'Sunderland')
    predict_result('Southampton', 'Bournemouth')
    predict_result('Tottenham Hotspurs', 'Aston Villa')
