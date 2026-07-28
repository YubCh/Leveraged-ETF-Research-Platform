import matplotlib.pyplot as plt
import numpy as np
from src.research.stats import count_draw_downs

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

#ccounts the drawdown from start to end date if mean=True we get the mean of a single year compressed. 
def draw_down_histogram(prices, start, end=None, mean=False, window=252):
    if end is None:
        end = len(prices)
    total_days = end - start
    scale = window / total_days if mean else 1 
    dd = np.arange(10,90,10)

    pure_data = np.array([count_draw_downs(prices, start, level, window) for level in dd])
    modified_data = np.append(pure_data[:-1] - pure_data[1:], pure_data[-1])
    modified_data = np.clip(modified_data, 0, None)

    plt.bar(dd,modified_data*scale,width=1.0,edgecolor='black',color='blue', align="edge")
    plt.xlabel("Drawdown %")
    plt.ylabel("Per year" if mean else "Count")
    plt.title(f"Drawdowns frequency per a {window} days" if mean else f"Amount of DrawDowns from day: {start} to {end}")
    plt.show()

