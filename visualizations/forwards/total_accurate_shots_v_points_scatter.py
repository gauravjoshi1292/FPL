__author__ = 'gj'

from bokeh.plotting import figure, output_file, show

from utils.read_data import get_plot_data

data = get_plot_data('forwards', 'total_shots', 'points')
total_shots_data = data['total_shots']
points = data['points']
shot_accuracy_data = get_plot_data('shot_accuracy', 'points')['shot_accuracy']
accurate_shots = [total_shots_data[i]*shot_accuracy_data[i] for i in range(len(total_shots_data))]
output_file("total_accurate_shots_v_points_scatter.html")
p = figure(plot_width=600, plot_height=600)
p.circle(accurate_shots, points, size=20, color="navy", alpha=0.5)
show(p)
