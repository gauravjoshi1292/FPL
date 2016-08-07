__author__ = 'gj'

import os
import collections


def get_data_from_file(filename):
    with open(filename) as fp:
        data = collections.OrderedDict()
        keys = fp.readline()
        for key in keys.split():
            data[key] = []

        for line in fp:
            values = line.split()
            if not values:
                continue

            i = 0
            for key in data.keys():
                if i == 0:
                    data[key].append(values[i])
                else:
                    data[key].append(float(values[i]))
                i += 1

    return data


def get_plot_data(x_key, y_key):
    data = {}
    path = os.path.abspath(os.path.dirname(__file__))
    high_price_forwards = get_data_from_file("{0}/../training_data/forwards/high_price_forwards.txt".format(path))
    mid_price_forwards = get_data_from_file("{0}/../training_data/forwards/mid_price_forwards.txt".format(path))
    low_price_forwards = get_data_from_file("{0}/../training_data/forwards/low_price_forwards.txt".format(path))

    for key in high_price_forwards:
        data[key] = []
        data[key].extend(high_price_forwards[key])
        data[key].extend(mid_price_forwards[key])
        data[key].extend(low_price_forwards[key])

    return {x_key: data[x_key], y_key: data[y_key]}
