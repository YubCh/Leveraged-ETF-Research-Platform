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

#buys over ma, sell under ma
def sma_strategy(prices, ma_rate):
  ma = moving_average(prices, ma_rate)
  target = (prices > ma).astype(float) 
  target[ma.isna()] = float("nan")
  return target.shift(1)

#witch to B during dip buy A when recovered. used together with swtich_dca
def dip_switch(prices, enter_at=20, exit_at=0, window=125):
  peak = prices.rolling(window, min_periods=1).max()
  dd = (1 - prices/ peak) * 100
  target = []
  in_dip = False
  for value in dd:
    if not in_dip and value >= enter_at:
      in_dip = True
    elif in_dip and value <= exit_at:
      in_dip = False
    target.append(1 if in_dip else 0)

  return pd.Series(target, index=prices.index).shift(1)