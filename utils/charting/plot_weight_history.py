import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def plot_weight_history(history, line_col="steelblue", bg_col="white"):
    matplotlib.use('Agg')  # Set backend to prevent segfault

    date   = [datetime.datetime.strptime(obs[0], "%Y-%m-%d") for obs in history]
    weight = [obs[1] for obs in history]
    mean   = [obs[2] for obs in history]

    fig = plt.figure(figsize=(4, 5))

    fig.patch.set_facecolor(bg_col)
    plt.gca().set_facecolor(bg_col)

    plt.plot(date, weight, label="weight", color=line_col, marker='.', zorder=3)
    plt.plot(date, mean, label="4 session average", color=line_col, linestyle="dashed", zorder=3)

    plt.ylabel("kg")
    # plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x} kg"))
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, 1.075), ncol=2)
    plt.legend().get_frame().set_facecolor(bg_col)
    plt.grid(True, zorder=0)
    fig.autofmt_xdate()
    fig.tight_layout()

    return plt.gcf()
