import pandas as pd
import math

#indicator as strategy containing Series of number 1 to 0 showing the percentage of capital in stocks 0.8 -> 80% of capital into stocks. 0 -> sell every stock 

def dca(prices, indicator=None, income = 100, income_period = 21, invest_period=21, start_capital=1000, start_date = 0):
  portfolio_value = []
  shares = 0
  not_invested_capital = start_capital 
  for days in range(start_date, len(prices)):
    if days % income_period == 0:
      not_invested_capital += income
    if days % invest_period == 0:
      if indicator is None:
        target = 1.0                        
      else:
        target = indicator.iloc[days]
      if not pd.isna(target):
        shares, not_invested_capital = allocate(shares, not_invested_capital, prices.iloc[days], target)
    portfolio_value.append(shares * prices.iloc[days] + not_invested_capital)
  return pd.Series(portfolio_value,index=prices.index[start_date:])
 
def allocate(shares, capital, price, target):
  potential = shares + math.floor(capital / price)
  real_shares_amount = math.floor(potential * target)
  real_shares_amount = max(real_shares_amount, shares)
  capital += (shares - real_shares_amount) * price
  return real_shares_amount, capital 
   
def total_invested(n_days, income=100, income_period=21, start_capital=1000, start_date=0):
    paydays = len([d for d in range(start_date, n_days) if d % income_period == 0])
    return start_capital + income * paydays
