from src.data.loader import get_data
from src.data.adjust import adjust
from src.data.artificial_data import extend_data
from src.backtesting.dca import dca, defined_drawdown, total_invested
import pandas as pd
tqqq = extend_data("TQQQ", 3, 0.0084)
ticker = tqqq

results = {}
for max_at in [10,30,50,70]:
  for min_at in [0, 5, 10, 20, 40]:
    for p in [0.5, 1, 1.5, 2.0]:
      row = {}
      for start in [0, 500, 1000, 2000]:
        indicator = defined_drawdown(ticker, max_at, min_at, p)
        series = dca(ticker, indicator, 100, 21, 21, 0, start)
        total_investment = total_invested(len(tqqq), 100, 21, 0, start)
        row[f"start: {start}"] = series.iloc[-1] /total_investment
      results[f"max_at: {max_at}, min_at: {min_at}, p={p}"] = row

df = pd.DataFrame(results).T
pd.set_option("display.float_format", "{:.2f}".format)
print(df)
print(df.max().max())