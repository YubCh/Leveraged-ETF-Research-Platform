import pandas as pd
import math


#exp draw down
# buys from min_at to max_at dd. Exponent for exponential curve.
def defined_drawdown(prices, max_at, min_at = 0, exponent=1):
  dd = (1 - prices/prices.cummax()) * 100
  target = (dd/max_at).clip(upper=1.0) ** exponent
  target[dd <= min_at] = float("nan")
  return target.round(4).shift(1)

#this prevents us from investing the plain dca if we are years below the peak
def defined_drawdown_window(prices, max_at,min_at=0,exponent=1,window=252):
  peak = prices.rolling(window, min_periods=1).max()
  dd= (1-prices/peak)*100
  target = (dd/max_at).clip(upper=1.0) ** exponent
  target[dd <= min_at] = float("nan")
  return target.round(4).shift(1)

#buy at top
def buy_high(prices):
  target = (prices == prices.cummax()).astype(float)
  target = target.where(target == 1.0)
  return target.shift(1)


def moving_average(prices, ma_rate):
  return prices.rolling(ma_rate).mean()

