import pandas as pd




def describe(prices):
  dd = prices / prices.cummax() - 1

  longest, current = 0, 0
  for value in dd:
    if value == 0:
      longest = max(longest, current)
      current = 0
    else:
      current += 1
  longest = max(longest, current)
  return {
    "CAGR": (prices.iloc[-1] / prices.iloc[0]) ** (252 / len(prices)) - 1,
    "Volatility (annualized)": prices.pct_change().std() * 252 ** 0.5,
    "Max Drawdown": dd.min(),
    "Longest Underwater": longest / 252
  }