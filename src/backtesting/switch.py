import pandas as pd
from .dca import allocate

# asset switiching sell a buys b v.v.


def switch_dca(prices_a, prices_b, strategy, income=100, income_period = 10,invest_period=10, start_capital=1000, start_date=0):
  portfolio_value = []
  shares_a,shares_b = 0
  capital = start_capital
  holding_b = False

  for days in range(start_date, len(prices_a)):
    price_a = prices_a.iloc[days]
    price_b = prices_b.iloc[days]

    if days % income_period == 0:
      captial += income

    target= strategy.iloc[days]
    if not pd.isna(target):
      want_b = target >=0.5
      if want_b != holding_b:
        if holding_b:
          shares_b, capital = allocate(shares_b, capital, price_b, 0, allow_sell=True)
        else:
          shares_a, capital =allocate(shares_a, capital, price_b, 0, allow_sell=True) 

        holding_b = want_b

    if days% invest_period == 0:
      if holding_b:
        shares_b, capital = allocate(shares_b, capital, price_b, 1)
      else:
        shares_a, capital = allocate(shares_a, capital, price_a, 1)

    portfolio_value.append(shares_a * prices_a + shares_b * price_b)
  return pd.Series(portfolio_value, index=prices_a.index[start_date:])