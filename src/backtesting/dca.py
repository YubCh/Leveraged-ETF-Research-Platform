import pandas as pd
import math

def dca(prices, amount = 100, period_in_d=21, start_capital=1000, start_date = 0):
  portfolio_value = []
  shares_amount = 0
  not_invested_capital = start_capital
  
  for days in range(start_date, len(prices)):
    if days % period_in_d == 0:
      not_invested_capital += amount
      shares, not_invested_capital = max_buy(not_invested_capital, prices.iloc[days])
       
      shares_amount += shares
    portfolio_value.append(shares_amount * prices.iloc[days])
  return pd.Series(portfolio_value,index=prices.index[start_date:])


def max_buy(capital, price):
  if capital >= price:
    shares = math.floor(capital / price)
    rest = capital - shares * price
    return shares, rest
  return 0, capital
