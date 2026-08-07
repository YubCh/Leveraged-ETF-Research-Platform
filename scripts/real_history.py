"""Real-history analysis: every strategy from 1999 to 2026 history.
"""

import pandas as pd

from src.data.loader import get_data
from src.data.adjust import adjust
from src.research.stats import describe_portfolio
from src.backtesting.dca import total_invested
from src.visualization.plots import compare, draw_down_histogram
from scripts.strategies import NAMES, PARAMS,PLAIN_ASSET,LEVERAGED_ASSET, build_all, maxdd

"""
Orientation:
NAMES =
 [f"{PLAIN_ASSET} DCA",               IDX: 0
  f"{LEVERAGED_ASSET} DCA",           IDX: 1
  f"{LEVERAGED_ASSET} dip",           IDX: 2
  f"{LEVERAGED_ASSET} SMA DCA"]       IDX: 3
"""
def run(plot=True):
    print(" Real history (1999-2026)")
    plain_asset = adjust(get_data(PLAIN_ASSET))
    strategies = build_all(plain_asset)

    invested = total_invested(len(plain_asset), income=PARAMS["income"],
                              income_period=PARAMS["income_period"],
                              start_capital=PARAMS["start_capital"],
                              start_date=PARAMS["start_date"])
    print(f"total invested: {invested:.0f}\n")
    print(0)
    rows = {}
    for name in NAMES:
        s = strategies[name]
        rows[name] = describe_portfolio(s, invested)
    print(pd.DataFrame(rows))
    print()

    print(f"head-to-head vs {NAMES[0]} (final value):")
    plain_asset_final = strategies[f"{NAMES[0]}"].iloc[-1]
    for name in NAMES[1:]:
        ratio = strategies[name].iloc[-1] / plain_asset_final
        print(f"  {name:10s} {ratio:6.2f} x {NAMES[0]}")
    print()

    if plot:
        compare(strategies, title="Real history: all stratetgies",
                normalize=False)


if __name__ == "__main__":
    run()