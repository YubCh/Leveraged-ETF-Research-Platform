"""Finding 2: 200-day SMA rotation on leveraged DCA.

Claim: SMA-200 rotation reliably reduces drawdown but usually reduces final
wealth.

Three experiments prove it:
  1. real_history_comparison   - plain vs SMA on the real (extended) history
  2. monte_carlo_comparison    - the trade-off across many bootstrapped paths
  3. drawdown_count_comparison - does SMA reduce the NUMBER of deep crashes
"""

import numpy as np
import pandas as pd

from src.data.loader import get_data
import matplotlib.pyplot as plt
from src.data.adjust import adjust
from src.research.monte_carlo import block_bootstrap
from src.backtesting.dca import dca
from src.backtesting.strategy import sma_strategy

from src.research.stats import count_draw_downs    
from src.data.artificial_data import simulate

def maxdd(s):
    return (s / s.cummax() - 1).min()


 
# 1. Real history
 
def real_history_comparison():
    print("Finding 2.1: real history (extended TQQQ, 1999-2026)")
    tqqq = simulate(adjust(get_data("QQQ")), 3, 0.0084)

    plain = dca(tqqq, None, start_capital=0)
    sma = dca(tqqq, sma_strategy(tqqq, 200), start_capital=0, allow_sell=True)

    print(f"plain: maxDD={maxdd(plain):.3f}  final={plain.iloc[-1]:,.0f}")
    print(f"sma  : maxDD={maxdd(sma):.3f}  final={sma.iloc[-1]:,.0f}")
    print()


 
# 2. Monte Carlo  
 
def monte_carlo_comparison(n_paths=200):
    print(f"Finding 2.2: Monte Carlo trade-off ({n_paths} paths)")
    qqq = adjust(get_data("QQQ"))
    paths_3x = [simulate(p, 3, 0.0084) for p in block_bootstrap(qqq, n_paths=n_paths)]

    plain_dd, plain_end, sma_dd, sma_end = [], [], [], []
    
    for p in paths_3x:
        plain = dca(p, None, start_capital=0)
        sma = dca(p, sma_strategy(p, 200), start_capital=0, allow_sell=True)

        plain_dd.append(maxdd(plain))
        plain_end.append(plain.iloc[-1])

        sma_dd.append(maxdd(sma))
        sma_end.append(sma.iloc[-1])

    plain_dd, plain_end = pd.Series(plain_dd), pd.Series(plain_end)
    sma_dd, sma_end     = pd.Series(sma_dd), pd.Series(sma_end)

    print("drawdown (less negative = better):")

    print(f"  plain  mean={plain_dd.mean():.3f}  median={plain_dd.median():.3f}")
    print(f"  sma    mean={sma_dd.mean():.3f}  median={sma_dd.median():.3f}")
    print(f"  sma shallower in {(sma_dd > plain_dd).mean():.1%} of paths")
    print("final value:")
    print(f"  plain  mean={plain_end.mean():,.0f}  median={plain_end.median():,.0f}")
    print(f"  sma    mean={sma_end.mean():,.0f}  median={sma_end.median():,.0f}")
    print(f"  sma higher final in {(sma_end > plain_end).mean():.1%} of paths")
    print()


 
# 3. Drawdown frequency
 
def _count_bands(series, window=100):
    levels = np.arange(10, 90, 10)
    cumulative = np.array([count_draw_downs(series, 0, lvl, window) for lvl in levels])
    bands = np.append(cumulative[:-1] - cumulative[1:], cumulative[-1])
    return levels, np.clip(bands, 0, None)


def drawdown_count_comparison(window=100):
    print(f"Finding 2.3: drawdown frequency (window={window})")
    tqqq = simulate(adjust(get_data("QQQ")), 3, 0.0084)

    plain = dca(tqqq, None, start_capital=0)
    sma = dca(tqqq, sma_strategy(tqqq, 200), start_capital=0, allow_sell=True)

    levels, plain_bands = _count_bands(plain, window)
    _, sma_bands = _count_bands(sma, window)

    print("levels:", levels)
    print("plain :", plain_bands)
    print("sma   :", sma_bands)

    w = 4
    plt.bar(levels, plain_bands, width=w, align="edge",
            color="red", alpha=0.6, label="plain DCA")
    plt.bar(levels + w, sma_bands, width=w, align="edge",
            color="blue", alpha=0.6, label="SMA-200 DCA")
    
    plt.xlabel("Drawdown %")
    plt.ylabel("Number of drawdowns")
    plt.title(f"Drawdown frequency: plain vs SMA-200 (window={window})")
    plt.legend()
    plt.show()
    print()


def run():
    real_history_comparison()
    monte_carlo_comparison()
    drawdown_count_comparison()


if __name__ == "__main__":
    run()