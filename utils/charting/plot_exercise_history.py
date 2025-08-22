def plot_exercise_history(history, unit_intensity, point_col="steelblue", bg_col="white"):
    return None

#import datetime
#import matplotlib
#import matplotlib.pyplot as plt
#import matplotlib.ticker as mticker
#from matplotlib.dates import AutoDateLocator, AutoDateFormatter
#
#
#def plot_exercise_history(history, unit_intensity, point_col="steelblue", bg_col="white"):
#    matplotlib.use('Agg')  # Set backend to prevent segfault
#    date      = [datetime.datetime.strptime(obs[0], "%Y-%m-%d") for obs in history]
#    intensity = [obs[1] for obs in history]
#    n         = [obs[2] * 20 for obs in history]
#
#    fig = plt.figure(figsize=(3.5, 2.5), constrained_layout=True)
#
#    fig.patch.set_facecolor(bg_col)
#    ax = plt.gca()
#    ax.set_facecolor(bg_col)
#
#    ax.scatter(date, intensity, s=n, c=[point_col], zorder=3)
#
#    locator = AutoDateLocator()
#    formatter = AutoDateFormatter(locator)
#    ax.xaxis.set_major_locator(locator)
#    ax.xaxis.set_major_formatter(formatter)
#
#    ax.set_ylabel(unit_intensity)
#    fig.autofmt_xdate()
#    ax.grid(True, zorder=0)
#
#    return fig
#
