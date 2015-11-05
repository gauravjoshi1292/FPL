__author__ = 'gj'

from crawlers.gw_results_and_fixtures_crawler import get_gameweek_fixtures_and_results
from db.query_handler import QueryHandler


def get_history(results):
    total, wins, losses, draws = 0.0, 0.0, 0.0, 0.0
    gs, gc = 0.0, 0.0

    for match in results:
        # print match
        if match['result'] == 'win':
            wins += 1
        elif match['result'] == 'loss':
            losses += 1
        elif match['result'] == 'draw':
            draws += 1

        gs += match['goals_for']
        gc += match['goals_against']
        total += 1

    if total == 0:
        total = 1

    return {'wins': wins/total, 'losses': losses/total, 'draws': draws/total,
            'gspg': gs/total, 'gcpg': gc/total}


def get_home_scores(ratios_overall, ratios_overall_home, ratios_opposition, ratios_opposition_home):
    home_win_score = ratios_overall['wins'] + 2*ratios_overall_home['wins'] + ratios_opposition['wins'] + 2*ratios_opposition_home['wins']
    home_loss_score = ratios_overall['losses'] + 2*ratios_overall_home['losses'] + ratios_opposition['losses'] + 2*ratios_opposition_home['losses']
    home_draw_score = ratios_overall['draws'] + 2*ratios_overall_home['draws'] + ratios_opposition['draws'] + 2*ratios_opposition_home['draws']

    home_gspg_score = (ratios_overall['gspg'] + 2*ratios_overall_home['gspg'] +
                       ratios_opposition['gspg'] +
                       2*ratios_opposition_home['gspg']) / (1 + 2 + 1 + 2)
    home_gcpg_score = (ratios_overall['gcpg'] + 2*ratios_overall_home['gcpg'] +
                       ratios_opposition['gcpg'] +
                       2*ratios_opposition_home['gcpg']) / (1 + 2 + 1 + 2)

    # print ratios_overall['wins'], ratios_overall_home['wins'], ratios_opposition['wins'], ratios_opposition_home['wins']
    # print home_win_score
    return home_win_score, home_loss_score, home_draw_score, home_gspg_score, home_gcpg_score


def get_home_team_score(team, opposition):
    qhandler = QueryHandler()
    last_five_results = qhandler.get_last_n_results(team, n=5)
    last_five_home_results = qhandler.get_last_n_results(team, n=5, place='home')
    last_five_away_results = qhandler.get_last_n_results(team, n=5, place='away')

    last_four_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)
    last_four_home_results_against = qhandler.get_last_n_results(team, n=3, place='home', opposition=opposition)
    last_four_away_results_against = qhandler.get_last_n_results(team, n=3, place='away', opposition=opposition)

    ratios_overall = get_history(last_five_results)
    ratios_overall_home = get_history(last_five_home_results)
    ratios_overall_away = get_history(last_five_away_results)

    ratios_opposition = get_history(last_four_results_against)
    ratios_opposition_home = get_history(last_four_home_results_against)
    ratios_opposition_away = get_history(last_four_away_results_against)

    return get_home_scores(ratios_overall, ratios_overall_home, ratios_opposition, ratios_opposition_home)


def get_away_scores(ratios_overall, ratios_overall_away, ratios_opposition, ratios_opposition_away):
    away_win_score = 2*ratios_overall['wins'] + 2*ratios_overall_away['wins'] + ratios_opposition['wins'] + ratios_opposition_away['wins']
    away_loss_score = 2*ratios_overall['losses'] + 2*ratios_overall_away['losses'] + ratios_opposition['losses'] + ratios_opposition_away['losses']
    away_draw_score = 2*ratios_overall['draws'] + 2*ratios_overall_away['draws'] + ratios_opposition['draws'] + ratios_opposition_away['draws']

    away_gspg_score = (ratios_overall['gspg'] + 2*ratios_overall_away['gspg'] +
                       ratios_opposition['gspg'] +
                       2*ratios_opposition_away['gspg']) / (1 + 2 + 1 + 2)
    away_gcpg_score = (ratios_overall['gcpg'] + 2*ratios_overall_away['gcpg'] +
                       ratios_opposition['gcpg'] +
                       2*ratios_opposition_away['gcpg']) / (1 + 2 + 1 + 2)

    return away_win_score, away_loss_score, away_draw_score, away_gspg_score, away_gcpg_score


def get_away_team_score(team, opposition):
    qhandler = QueryHandler()
    last_five_results = qhandler.get_last_n_results(team, n=5)
    last_five_home_results = qhandler.get_last_n_results(team, n=5, place='home')
    last_five_away_results = qhandler.get_last_n_results(team, n=5, place='away')

    last_four_results_against = qhandler.get_last_n_results(team, n=3, opposition=opposition)
    last_four_home_results_against = qhandler.get_last_n_results(team, n=3, place='home', opposition=opposition)
    last_four_away_results_against = qhandler.get_last_n_results(team, n=3, place='away', opposition=opposition)

    ratios_overall = get_history(last_five_results)
    ratios_overall_home = get_history(last_five_home_results)
    ratios_overall_away = get_history(last_five_away_results)

    ratios_opposition = get_history(last_four_results_against)
    ratios_opposition_home = get_history(last_four_home_results_against)
    ratios_opposition_away = get_history(last_four_away_results_against)

    away_win_score = 2*ratios_overall['wins'] + 2*ratios_overall_away['wins'] + ratios_opposition['wins'] + ratios_opposition_away['wins']
    away_loss_score = 2*ratios_overall['losses'] + 2*ratios_overall_away['losses'] + ratios_opposition['losses'] + ratios_opposition_away['losses']
    away_draw_score = 2*ratios_overall['draws'] + 2*ratios_overall_away['draws'] + ratios_opposition['draws'] + ratios_opposition_away['draws']

    return get_away_scores(ratios_overall, ratios_overall_away, ratios_opposition, ratios_opposition_away)


def predict_result(home_team, away_team):
    home_win_score, home_loss_score, home_draw_score, home_gspg_score, home_gcpg_score = get_home_team_score(home_team, away_team)
    away_win_score, away_loss_score, away_draw_score, away_gspg_score, away_gcpg_score = get_away_team_score(away_team, home_team)

    home_win_prob = home_win_score + away_loss_score
    away_win_prob = home_loss_score + away_win_score
    draw_prob = home_draw_score + away_draw_score

    print home_team, away_team
    # print home_win_prob, away_win_prob, draw_prob

    if home_win_prob > away_win_prob and home_win_prob > draw_prob:
        print home_team
    elif away_win_prob > home_win_prob and away_win_prob > draw_prob:
        print away_team
    else:
        print 'DRAW'

    hg = round(home_gspg_score + away_gcpg_score / 2.0)
    ag = round(away_gspg_score + home_gcpg_score / 2.0)

    print hg, ag, '\n'

if __name__ == '__main__':
    predict_result('Stoke City', 'Chelsea')
