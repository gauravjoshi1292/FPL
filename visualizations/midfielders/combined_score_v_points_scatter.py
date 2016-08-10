__author__ = 'gj'

from bokeh.plotting import figure, output_file, show

from utils.read_data import get_plot_data

data = get_plot_data('midfielders', 'total_shots', 'points')
total_shots_data = data['total_shots']
points = data['points']
shot_accuracy_data = get_plot_data('midfielders', 'shot_accuracy', 'points')['shot_accuracy']
key_passes_data = get_plot_data('midfielders', 'key_passes', 'points')['key_passes']
combined_score = [total_shots_data[i]*shot_accuracy_data[i]+0.33*key_passes_data[i] for i in range(len(total_shots_data))]
output_file("combined_score_v_points_scatter.html")
p = figure(plot_width=600, plot_height=600)
p.circle(combined_score, data['points'], size=20, color="navy", alpha=0.5)
show(p)
