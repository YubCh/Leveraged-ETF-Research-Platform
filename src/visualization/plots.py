import matplotlib.pyplot as plt


def compare(series_dict, title="", normalize=True, log=True):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                   gridspec_kw={"height_ratios": [2, 1]})

    for name, s in series_dict.items():
        s = s.replace(0, float("nan"))            
        if normalize and s.dropna().iloc[0] > 0:
            s = s / s.dropna().iloc[0]
        ax1.plot(s.index, s, label=name)
        dd = s / s.cummax() - 1
        ax2.plot(dd.index, dd)

    if log:
        ax1.set_yscale("log")
    ax1.legend()
    ax1.set_title(title)
    ax1.set_ylabel("value (log)" if log else "value")
    ax2.set_ylabel("drawdown")
    plt.tight_layout()
    plt.show()