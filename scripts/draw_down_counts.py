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

def run(window=125):
  plain_asset = adjust(get_data(PLAIN_ASSET))
  strategies = build_all(plain_asset)


  bars = {
    name: count_dd(strategies[name], window) for name in NAMES
  }

  print("draw down levels", DD_LEVELS)

  for name in NAMES:
    print(f"{name}", bars[name])
  print("\n")

  width = 8 / len(NAMES)
  plt.figure(figsize=(11,6))
  for i, name in enumerate(NAMES):
     plt.bar(DD_LEVELS + i * width, bars[name], width=width, align="edge",color=COLORS[name],alpha=0.7, label=name)

     plt.xlabel("Drawdown depth")
     plt.ylabel("Number of drawdowns")
     plt.title(f"Hof often each strategy crashes and their depth (window={window})")
     plt.tight_layout()
     plt.show()
     
    


if __name__ == "__main__":
    run()
