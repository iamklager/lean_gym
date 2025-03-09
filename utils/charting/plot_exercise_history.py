import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def plot_exercise_history(history, unit_intensity, point_col="steelblue", bg_col="white"):

    matplotlib.use('Agg')  # Set backend to prevent segfault
    date      = [datetime.datetime.strptime(obs[0], "%Y-%m-%d") for obs in history]
    intensity = [obs[1] for obs in history]
    n         = [obs[2] * 20 for obs in history]

    fig = plt.figure(figsize=(3.5, 2.5))

    fig.patch.set_facecolor(bg_col)
    plt.gca().set_facecolor(bg_col)

    plt.scatter(date, intensity, s=n, c=point_col, zorder=3)

    plt.ylabel(unit_intensity)
    # plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x} {unit_intensity}"))
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.grid(True, zorder=0)

    return plt.gcf()
