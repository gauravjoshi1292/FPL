__author__ = 'gj'

from utils.forwards import get_plot_data


def get_forwards_sorted_by_total_score():
    """
    Score is defined as total accurate shots
    :return:
    """
    data = get_plot_data('total_shots', 'name')
    total_shots_data = data['total_shots']
    players = data['name']
    shot_accuracy_data = get_plot_data('shot_accuracy', 'points')['shot_accuracy']
    scores = [total_shots_data[i]*shot_accuracy_data[i] for i in range(len(total_shots_data))]
    player_scores = [(players[i], scores[i]) for i in range(len(players))]

    player_scores = sorted(player_scores, key=lambda x: x[1], reverse=True)
    print player_scores


def get_forwards_sorted_by_value():
    """
    Value is defined as score per price
    :return:
    """
    data = get_plot_data('total_shots', 'name')
    total_shots_data = data['total_shots']
    players = data['name']
    data = get_plot_data('shot_accuracy', 'price')
    shot_accuracy_data = data['shot_accuracy']
    prices = data['price']
    values = [(total_shots_data[i]*shot_accuracy_data[i])/prices[i] for i in range(len(total_shots_data))]
    player_values = [(players[i], values[i], prices[i]) for i in range(len(players))]

    player_values = sorted(player_values, key=lambda x: x[1], reverse=True)
    print player_values


get_forwards_sorted_by_total_score()
get_forwards_sorted_by_value()
