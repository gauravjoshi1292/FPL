__author__ = 'gj'

from bokeh.plotting import figure, output_file, show

from utils.forwards import get_plot_data

data = get_plot_data('shot_accuracy', 'points')
output_file("shot_accuracy_v_points_scatter.html")
p = figure(plot_width=600, plot_height=600)
p.circle(data['shot_accuracy'], data['points'], size=20, color="navy", alpha=0.5)
show(p)
