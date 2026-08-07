"""Real-history analysis: every strategy from 1999 to 2026 history.
"""

import pandas as pd

from src.data.loader import get_data
from src.data.adjust import adjust
from src.data.artificial_data import simulate
from src.research.stats import describe_portfolio
from src.backtesting.dca import total_invested
from src.visualization.plots import compare, draw_down_histogram
from scripts.strategies import NAMES, PARAMS,PLAIN_ASSET,LEVERAGED_ASSET, build_all, maxdd, build_asset

"""
Orientation:
NAMES =
 [f"{PLAIN_ASSET} DCA",               IDX: 0
  f"{LEVERAGED_ASSET} DCA",           IDX: 1
  f"{LEVERAGED_ASSET} dip",           IDX: 2
  f"{LEVERAGED_ASSET} SMA DCA"]       IDX: 3
"""
def run(start = None, plot=True):
    label = f"from {start}" if start else ""
    print(f" Real history ({label}-2026)")
    plain_asset = adjust(get_data(PLAIN_ASSET))

    if start:
        plain_asset = plain_asset.loc[start:]
    strategies = build_all(plain_asset)
    base_strategies = build_asset(plain_asset)
    if start:
        #scaling down leveraged to plain to have a same starting point 
        base_strategies["leveraged"] = base_strategies["leveraged"] * (base_strategies["plain"].iloc[0] / base_strategies["leveraged"].iloc[0])

        print(f"start date: {start}, start price: {base_strategies["leveraged"].iloc[0]:.3f}, end price: {base_strategies["leveraged"].iloc[-1]:.3f}, total: {(base_strategies["leveraged"].iloc[-1] / 100):.3f} times return.")
        print(f"{LEVERAGED_ASSET} = {base_strategies['leveraged'].iloc[-1] / base_strategies['plain'].iloc[-1]} x {PLAIN_ASSET}")
        print("\n")
        print("-------------------------------\n")


    invested = total_invested(len(plain_asset), income=PARAMS["income"],
                              income_period=PARAMS["income_period"],
                              start_capital=PARAMS["start_capital"],
                              start_date=PARAMS["start_date"])
    print(f"total invested: {invested:.0f}\n")
    rows = {}
    for name in NAMES:
        s = strategies[name]
        rows[name] = describe_portfolio(s, invested)
    print(pd.DataFrame(rows).T)
    print()

    print(f"head-to-head vs {NAMES[0]} (final value):")
    plain_asset_final = strategies[f"{NAMES[0]}"].iloc[-1]
    for name in NAMES[1:]:
        ratio = strategies[name].iloc[-1] / plain_asset_final
        print(f"  {name} {ratio:.2f} x {NAMES[0]}")
    print()

    if plot:
        compare(base_strategies, title=f"Pure {PLAIN_ASSET}, {LEVERAGED_ASSET} Stock Chart", normalize=False)
        compare(strategies, title="Real history: all stratetgies",
                normalize=False)


if __name__ == "__main__":
    run()