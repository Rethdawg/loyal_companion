# Module containing general utilities
import numpy as np
import matplotlib.pyplot as plt


def plot_currency(historical_dict):
    x_data = []
    y_data = []
    for kp in historical_dict['rates']:
        x_data.append(np.datetime64(kp))
        for rate in historical_dict['rates'][kp]:
            y_data.append(historical_dict['rates'][kp].get(rate))
    fig, ax = plt.subplots()
    ax.plot(x_data, y_data)
    plt.savefig('/static/images/historical.png')
