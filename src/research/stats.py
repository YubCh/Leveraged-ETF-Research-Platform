import pandas as pd


#for graph
def describe(prices):
  dd = prices / prices.cummax() - 1
  longest = longest_underwater_years(dd)
  return {
    "CAGR": (prices.iloc[-1] / prices.iloc[0]) ** (252 / (len(prices) - 1)) - 1,
    "Volatility (annualized)": prices.pct_change().std() * 252 ** 0.5,
    "Max Drawdown": dd.min(),
    "Longest Underwater": longest / 252,
    "Best Day": prices.pct_change().max(),
    "Worst Day": prices.pct_change().min(),
    "Total Return": ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100
  }


def describe_portfolio(series, total_invested):
  dd = series / series.cummax() - 1
  longest = longest_underwater_years(dd)
  return {
    "Final Value": series.iloc[-1],
    "Total Invested": total_invested,
    "Max Drawdown": dd.min(),
    "Longest Underwater": longest / 252,
    "Multiple on Investment": series.iloc[-1] / total_invested
  }


def longest_underwater_years(dd):
  longest, current = 0, 0
  for value in dd:
    if value == 0:
      longest = max(longest, current)
      current = 0
    else:
      current += 1
  return max(longest, current)

def count_draw_downs(prices, start, max_at, window=100):
    peak = prices.rolling(window).max()         
    dd = (1 - prices / peak) * 100
    dd = dd.iloc[start:]
    count = 0
    below = False
    for value in dd:
        if value >= max_at and not below:
            count += 1
            below = True
        elif value < max_at:
            below = False
    return count