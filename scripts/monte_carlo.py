"""Monte Carlos analysis: every strategy across n bootstrapped paths.

The real history is one path. This resamples 20-day blocks of real QQQ
returns so into many alternative paths, applies leverage to each,
and runs every strategy in every universe
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.data.adjust import adjust
from src.data.loader import get_data
from src.research.monte_carlo import block_bootstrap
from scripts.strategies import NAMES, COLORS,PLAIN_ASSET,LEVERAGED_ASSET,  build_all, maxdd
"""
Orientation:
NAMES =
 [f"{PLAIN_ASSET} DCA",               IDX: 0
  f"{LEVERAGED_ASSET} DCA",           IDX: 1
  f"{LEVERAGED_ASSET} dip",           IDX: 2
  f"{LEVERAGED_ASSET} SMA DCA"]       IDX: 3
"""

BENCHMARK = NAMES[0]


def collect(n_paths=500,start=None):
    """Run every strategy on n_paths bootstrapped histories.
    Returns (finals, maxdrawdowns) as dicts of name -> pd.Series."""
    plain_asset = adjust(get_data(PLAIN_ASSET))
    if start:
        plain_asset = plain_asset.loc[start:]
    finals = {name: [] for name in NAMES}
    dds = {name: [] for name in NAMES}

    for path in block_bootstrap(plain_asset, n_paths=n_paths):
        for name, series in build_all(path).items():
            finals[name].append(series.iloc[-1])
            dds[name].append(maxdd(series))

    return ({k: pd.Series(v) for k, v in finals.items()},
            {k: pd.Series(v) for k, v in dds.items()})


def report(finals, dds):
    print("final value:")
    for name in NAMES:
        f = finals[name]
        print(f"  {name} median={f.median():.0f}  mean={f.mean():.0f}"
        
              f"  <=5%={f.quantile(0.05):.0f}  =<95%={f.quantile(0.95):.0f}")
    print()
    print("\n mnax drawdown (median,less negative -> better):")
    for name in NAMES:
        print(f"  {name} {dds[name].median():.3f}")

    print(f"\n win rate vs {BENCHMARK} (final value):")
    for name in NAMES[1:]:
        print(f"  {name} beats {BENCHMARK} in "
              f"{(finals[name] > finals[BENCHMARK]).mean():.1%} of paths")
    print("dddddddddddd")
    print(f"\nwin rate vs {NAMES[1]}:")

    plain = finals[NAMES[1]]
    for name in (NAMES[2], NAMES[3]):
        print(f"  {name} beats {NAMES[1]} in "
              f"{(finals[name] > plain).mean():.1%} of paths")
    print()

def distribution_plot(finals, real_finals=None):
    """Outcome histograms.

    Log dollar axis:
    axis spacing is logarithmic for better reability.
    real_finals (optional): is final value from the real history,
    drawn as a vertical line so you can see how good our actully performed.
    """
    all_values = pd.concat(finals.values())
    positive = all_values[all_values > 0]
   #real history has to be in range 
    lo, hi = max(positive.min(), 1), positive.max()
    if real_finals:
         
        lo = min(lo, min(real_finals.values()))
        hi = max(hi, max(real_finals.values()))
    bins = np.logspace(np.log10(lo), np.log10(hi), 50)

    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True, sharey=True)
    benchmark_median = finals[BENCHMARK].median()

    for ax, name in zip(axes.flat, NAMES):
        ax.hist(finals[name], bins=bins, color=COLORS[name], alpha=0.75)

        ax.axvline(finals[name].median(), color="black",
          linestyle="--",
          linewidth=2,
          label=f"MC median {finals[name].median():.0f}")

        ax.axvline(benchmark_median, color="gray",
          linestyle=":",
          linewidth=2,
          label=f"{BENCHMARK} median")


        if real_finals and name in real_finals:
          rv = real_finals[name]
          pct = (finals[name] < rv).mean()
          ax.axvline(
            rv,
            color="magenta",
            linewidth=2.5,
            label=f"real history {rv:.0f}, beats ({pct:.0%} other paths)")
        
        ax.set_xscale("log")
        ax.set_title(name)
        ax.legend(fontsize=8)

    for ax in axes[1]:
      ax.set_xlabel("Final portfolio value ($, log axis)")
    for ax in axes[:, 0]:
      ax.set_ylabel("Number of histories")
    for ax in axes.flat:
      ax.tick_params(labelbottom=True, labelleft=True)

    fig.suptitle("Outcome distributions across bootstrapped histories")
    plt.tight_layout()
    plt.show()


def run(n_paths=500, plot=True, start=None):
    label = f"from {start}" if start else""
    print(f"Monte Carlo ({n_paths} paths){label}")
    finals, dds = collect(n_paths,start)
    report(finals, dds)

    if plot:
        real = adjust(get_data(PLAIN_ASSET))
        real_finals = {name: s.iloc[-1] for name, s in build_all(real).items()}
        distribution_plot(finals, real_finals)
    return finals, dds


if __name__ == "__main__":
    run()