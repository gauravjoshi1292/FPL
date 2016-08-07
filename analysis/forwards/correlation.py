__author__ = 'gj'

from scipy.stats.stats import pearsonr

from utils.forwards import get_plot_data


def attack_score_v_points_correlation():
    data = get_plot_data('attack_score', 'points')
    r = pearsonr(data['attack_score'], data['points'])
    return r


def shot_accuracy_v_points_correlation():
    data = get_plot_data('shot_accuracy', 'points')
    r = pearsonr(data['shot_accuracy'], data['points'])
    return r


def total_shots_v_points_correlation():
    data = get_plot_data('total_shots', 'points')
    r = pearsonr(data['total_shots'], data['points'])
    return r


def total_accurate_shots_v_points_correlation():
    data = get_plot_data('total_shots', 'points')
    total_shots_data = data['total_shots']
    points = data['points']
    shot_accuracy_data = get_plot_data('shot_accuracy', 'points')['shot_accuracy']
    accurate_shots = [total_shots_data[i]*shot_accuracy_data[i] for i in range(len(total_shots_data))]
    r = pearsonr(accurate_shots, points)
    return r


def attack_score_v_price_correlation():
    data = get_plot_data('total_shots', 'price')
    r = pearsonr(data['total_shots'], data['price'])
    return r


def total_accurate_shots_v_price_correlation():
    data = get_plot_data('total_shots', 'price')
    total_shots_data = data['total_shots']
    price = data['price']
    shot_accuracy_data = get_plot_data('shot_accuracy', 'price')['shot_accuracy']
    accurate_shots = [total_shots_data[i]*shot_accuracy_data[i] for i in range(len(total_shots_data))]
    r = pearsonr(accurate_shots, price)
    return r


print(attack_score_v_points_correlation())
print(shot_accuracy_v_points_correlation())
print(total_shots_v_points_correlation())
print(total_accurate_shots_v_points_correlation())
print(attack_score_v_price_correlation())
print(total_accurate_shots_v_price_correlation())
