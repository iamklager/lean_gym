import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.dates import AutoDateLocator, AutoDateFormatter


def plot_weight_history(history, line_col="steelblue", bg_col="white"):
    matplotlib.use('Agg')  # Set backend to prevent segfault

    date   = [datetime.datetime.strptime(obs[0], "%Y-%m-%d") for obs in history]
    weight = [obs[1] for obs in history]
    mean   = [obs[2] for obs in history]

    fig = plt.figure(figsize=(4, 5), constrained_layout=True)

    fig.patch.set_facecolor(bg_col)
    ax = plt.gca()
    ax.set_facecolor(bg_col)

    ax.plot(date, weight, label="weight", color=line_col, marker='.', zorder=3)
    ax.plot(date, mean, label="4 session average", color=line_col, linestyle="dashed", zorder=3)

    ax.set_ylabel("kg")

    # Use AutoDateLocator and AutoDateFormatter for clean x-axis
    locator = AutoDateLocator()
    formatter = AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.075), ncol=2)
    ax.legend().get_frame().set_facecolor(bg_col)
    ax.grid(True, zorder=0)
    fig.autofmt_xdate(rotation=45)

    return fig
