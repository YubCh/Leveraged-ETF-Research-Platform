from pathlib import Path
import pandas as pd
import yfinance as yf

DATA_DIR = Path('data/prices')

def download_ticker(ticker: str):
  df = pd.DataFrame(yf.download(
    ticker,
    period = "max",
    interval = "1d",
    auto_adjust = False,
    progress = False
    ))
  
  if df is None or df.empty:
    raise ValueError(f"Ticker name '{ticker}' does not exist")
  return df


if __name__ == "__main__":
  df = download_ticker("QQQ")
  print(df.head())
  print(df.tail())
  print(df.columns)
  print(len(df))