import pandas as pd
from src.data.loader import get_data
from src.data.adjust import adjust
# Extracting data from QQQ to get QLD and TQQQ back to the start of QQQ
# QLD was born 2008 and TQQQ 2010

#simulate allows to get adj_close data for tickers with a leverage of x
def simulate(adj_close, leverage, expense_ratio, borrow_rate = 0.02):
  daily_returns = adj_close.pct_change().fillna(0) * leverage
  leveraged_daily_fees = (expense_ratio + (leverage - 1) * borrow_rate) /252 
  leveraged_daily_returns = daily_returns - leveraged_daily_fees
  leveraged_series = 100 * (1 + leveraged_daily_returns).cumprod()
  return leveraged_series
#some tickers like TQQQ were born back in 2010. To track it back to a certain date we have to concat the ticker TQQQ and get the data before 2010 from a simulated dataset
def extend_data(ticker, leverage, expense_ratio, base="QQQ"):
  real = adjust(get_data(ticker), dividends=True, splits=False)
  sim = simulate(adjust(get_data(base), dividends=True, splits=False), leverage, expense_ratio)

  first_date = real.index.min()
  scale =  real.iloc[0] / sim.loc[first_date] 
  sim_part = sim[sim.index < first_date] * scale

  return pd.concat([sim_part, real])
