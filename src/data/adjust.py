import pandas as pd

def adjust(df, dividends=True, splits=True):
  df = df.copy()
  df["prev_close"] = df["Close"].shift(1)
  factor_after = 1.0

  for idx,row in df.iloc[::-1].iterrows():
    df.loc[idx, "Adj Close"] = row["Close"] * factor_after  
    if dividends and row["Dividends"] > 0 and pd.notna(row["prev_close"]):
      factor_after = factor_after * (1 - row["Dividends"] / row["prev_close"])
    if splits and row["Stock Splits"] != 0:
      factor_after = factor_after * (1 / row["Stock Splits"])
  
  return df["Adj Close"]