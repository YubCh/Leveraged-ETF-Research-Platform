import pandas as pd
import math

#indicator as strategy containing Series of number 1 to 0 showing the percentage of capital in stocks 0.8 -> 80% of capital into stocks. 0 -> sell every stock 

def dca(prices, indicator, amount = 100, period_in_d=21, start_capital=1000, start_date = 0):
  portfolio_value = []
  shares = 0
  not_invested_capital = start_capital
  
  for days in range(start_date, len(prices)):
    if days % period_in_d == 0:
      not_invested_capital += amount
      shares, not_invested_capital = allocate(shares, not_invested_capital, prices.iloc[days], indicator.iloc[days])
       
    portfolio_value.append(shares * prices.iloc[days])
  return pd.Series(portfolio_value,index=prices.index[start_date:])
 
def allocate(shares, capital, price, day):
  if day < 1:
    shares *= math.floor(1 - day)
    capital += price * shares
    return shares, capital
  if capital >= price:
    shares = math.floor(capital / price)
    capital -= shares * price
    return shares, capital
  return 0, capital


def only_buy_draw_down(prices):
  draw_down = False

  return

def only_buy(prices):
  return pd.Series(1.0, index=range(len(prices)))