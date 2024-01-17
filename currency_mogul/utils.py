# Module containing general utilities
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
historic_graph_path = 'currency_mogul/static/images/historical.png'


def plot_currency(historical_dict):
    x_data = []
    y_data = []
    for kp in historical_dict['rates']:
        x_data.append(np.datetime64(kp))
        for rate in historical_dict['rates'][kp]:
            y_data.append(historical_dict['rates'][kp].get(rate))
    fig, ax = plt.subplots()
    print(x_data)
    print(y_data)
    ax.plot(x_data, y_data)
    plt.savefig(historic_graph_path)


def clear_graph():
    Path(historic_graph_path).unlink(missing_ok=True)