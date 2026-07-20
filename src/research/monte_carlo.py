import pandas as pd
import numpy as np


#alternative history generator
def block_bootstrap(prices, n_paths=1000, block_days=20, seed=0):
  rng = np.random.default_rng(seed)
  returns = prices.pct_change().dropna().to_numpy()
  n = len(returns)
  n_blocks = n // block_days + 1
  paths = []
  for _ in range(n_paths):
    starts = rng.integers(0, n - block_days, size=n_blocks)
    sampled = np.concatenate([returns[s:s + block_days] for s in starts])[:n]
    path = 100 * np.cumprod(1 + sampled)
    paths.append(pd.Series(path, index=prices.index[1:]))
  return paths