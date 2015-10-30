__author__ = 'gj'

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

    return {'wins': wins/total, 'losses': losses/total, 'draws': draws/total}


def predict_result(home_team, away_team):
    qhandler = QueryHandler()
    last_five_results = qhandler.get_last_n_results(home_team, n=5)
    last_five_home_results = qhandler.get_last_n_results(home_team, n=5, place='home')
    last_five_away_results = qhandler.get_last_n_results(home_team, n=5, place='away')

    last_three_results_against = qhandler.get_last_n_results(home_team, n=3, opposition=away_team)
    last_three_home_results_against = qhandler.get_last_n_results(home_team, n=3, opposition=away_team)
    last_three_away_results_against = qhandler.get_last_n_results(home_team, n=3, opposition=away_team)

    ratios_overall = get_ratios(last_five_results)
    win_ratios_overall = ratios_overall['wins']
    loss_ratios_overall = ratios_overall['losses']
    draws_ratios_overall = ratios_overall['draws']


if __name__ == '__main__':
    predict_result('Arsenal', 'Manchester City')
