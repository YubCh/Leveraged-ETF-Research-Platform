"""
How often does a strategy crash in a certain period, and how deep.
Max drawdown reports the worst crash. Since we are trading with leverage assets we want to see how often how deep and how fast a crash appears.

The counting uses a window-period for a crash, since e.g. the all time high in extended tqqq takes ~20years to recover. The window can be chosen. 
"""


import numpy as np

import matplotlib.pyplot as plt

from src.research.stats import count_draw_downs
from src.data.loader import get_data
from src.data.adjust import adjust
from scripts.strategies import NAMES, COLORS, PLAIN_ASSET, LEVERAGED_ASSET, build_all

DD_LEVELS = np.arange(10,100,10)


def count_dd(series, window=125):
  cumulative_dd = np.array([count_draw_downs(series, 0 , lvl, window) for lvl in DD_LEVELS])
  pure_dd = np.append(cumulative_dd[:-1] - cumulative_dd[1:], cumulative_dd[-1])
  return np.clip(pure_dd, 0 , None)


def plot_bars(bars,window, title):
  fig, axes = plt.subplots(2,2, figsize=(13,8), sharex=True, sharey=True)
  for ax, name in zip(axes.flat, NAMES):
     ax.bar(DD_LEVELS, bars[name],
             width=8,
             align="edge", color=COLORS[name], alpha=0.8,edgecolor="black")
     ax.set_title(f"{name} (total: {bars[name].sum()})")
     ax.grid(True, alpha=0.3, linestyle="--")
     ax.set_xticks(DD_LEVELS)
  for ax in axes[1]:
     ax.set_xlabel("Drawdown depth")
  for ax in axes[:, 0]:
     ax.set_ylabel("Number of drawdowns")
  for ax in axes.flat:
     ax.tick_params(labelbottom=True, labelleft=True)

  fig.suptitle(f"{title} (window={window})")
  plt.tight_layout()
  plt.show()


def report_bars(bands, window=125):
  print(f"drawdown depth per bar "
        f"(median across paths, window={window}):")
  header = " ".join(f"{lvl}%" for lvl in DD_LEVELS)
  print(f"  {''}{header}")
  for name in NAMES:
      medians = np.median(bands[name], axis=0)
      row = " ".join(f"{m} " for m in medians)
      print(f"  {name}{row}")
  print()

    
def run(window=125):
  print(f"Drawdown frequency (window={window})")
  plain_asset = adjust(get_data(PLAIN_ASSET))
  strategies = build_all(plain_asset)
  bars = {
    name: count_dd(strategies[name], window) for name in NAMES
  }
  print("draw down levels", DD_LEVELS)
  for name in NAMES:
    print(f"{name}", bars[name])
  print("\n")
  plot_bars(bars,window,  f"How often each strategy crashes and their depth (window={window})")

if __name__ == "__main__":
    run()
