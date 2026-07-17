import pandas as pd
import math

#indicator as strategy containing Series of number 1 to 0 showing the percentage of capital in stocks 0.8 -> 80% of capital into stocks. 0 -> sell every stock 

def dca(prices, indicator=None, amount = 100, period_in_d=21, start_capital=1000, start_date = 0):
  portfolio_value = []
  shares = 0
  not_invested_capital = start_capital
  
  for days in range(start_date, len(prices)):
    if days % period_in_d == 0:
      not_invested_capital += amount
      if indicator is None:
        target = 1.0                        
      else:
        target = indicator.iloc[days]
      if not pd.isna(target):
        shares, not_invested_capital = allocate(shares, not_invested_capital, prices.iloc[days], target)
       
    portfolio_value.append(shares * prices.iloc[days])
  return pd.Series(portfolio_value,index=prices.index[start_date:])
 
def allocate(shares, capital, price, target):
  potential = shares + math.floor(capital / price)
  real_shares_amount = math.floor(potential * target)
  capital += (shares - real_shares_amount) * price
  return real_shares_amount, capital 
   


def only_buy_draw_down(prices, draw_down):
  ret = []
  all_time_high = 0
  for days in range(len(prices)):
    if all_time_high < prices.iloc[days]:
      all_time_high = prices.iloc[days]
      ret.append(None)
    elif (1 - (prices.iloc[days] / all_time_high)) * 100 >= draw_down:
      ret.append(1.0)
    else:
      ret.append(None)
      #shift since we buy from last days price
  return pd.Series(ret, index=prices.index, dtype="float64").shift(1)
 
  