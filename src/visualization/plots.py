import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def compare(series_dict, title=""):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                   gridspec_kw={"height_ratios": [3, 2]})

    for name, s in series_dict.items():
        norm = s / s.iloc[0]             
        ax1.plot(norm.index, norm, label=name)
        dd = s / s.cummax() - 1
        ax2.plot(dd.index, dd)

    ax1.set_yscale("log")
    ax1.yaxis.set_major_formatter(ScalarFormatter())
    ax1.ticklabel_format(axis="y", style="plain")
    ax1.legend()
    ax1.set_title(title)
    ax1.set_ylabel("growth of $1 (log)")
    ax2.set_ylabel("drawdown")
    plt.tight_layout()
    plt.show()                            