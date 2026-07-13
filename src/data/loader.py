from pathlib import Path
import pandas as pd
import yfinance as yf

DATA_DIR = Path('data/prices')
COLUMNS = ["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]

def download_ticker(ticker: str):
  df = yf.Ticker(ticker).history(period="max", auto_adjust=False, actions=True)
  
  if df is None or df.empty:
    raise ValueError(f"Ticker name '{ticker}' does not exist")
  df.index = df.index.tz_localize(None)
  return df[COLUMNS]


if __name__ == "__main__":
  df = download_ticker("QQQ")
  print(df.head())
  print(df.tail())
  print(df.columns)
  print(len(df))