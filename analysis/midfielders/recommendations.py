__author__ = 'gj'

from utils.read_data import get_plot_data


def get_midfielders_sorted_by_total_score():
    """
    Score is defined as total accurate shots + key passes
    :return:
    """
    data = get_plot_data('midfielders', 'total_shots', 'name')
    total_shots_data = data['total_shots']
    players = data['name']
    shot_accuracy_data = get_plot_data('midfielders', 'shot_accuracy', 'points')['shot_accuracy']
    chances_created_data = get_plot_data('midfielders', 'chances_created', 'points')['chances_created']
    scores = [total_shots_data[i]*shot_accuracy_data[i]+0.33*chances_created_data[i] for i in range(len(total_shots_data))]
    player_scores = [(players[i], scores[i]) for i in range(len(players))]

    player_scores = sorted(player_scores, key=lambda x: x[1], reverse=True)
    print(player_scores)


def get_midfielders_sorted_by_value():
    """
    Value is defined as score per price
    :return:
    """
    data = get_plot_data('midfielders', 'total_shots', 'name')
    total_shots_data = data['total_shots']
    players = data['name']
    data = get_plot_data('midfielders', 'shot_accuracy', 'price')
    shot_accuracy_data = data['shot_accuracy']
    chances_created_data = get_plot_data('midfielders', 'chances_created', 'points')['chances_created']
    prices = data['price']
    values = [(total_shots_data[i]*shot_accuracy_data[i]+0.33*chances_created_data[i])/prices[i] for i in range(len(total_shots_data))]
    player_values = [(players[i], values[i], prices[i]) for i in range(len(players))]

    player_values = sorted(player_values, key=lambda x: x[1], reverse=True)
    print(player_values)


get_midfielders_sorted_by_total_score()
get_midfielders_sorted_by_value()
