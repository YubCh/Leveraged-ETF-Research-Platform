from pathlib import Path
import pandas as pd
import yfinance as yf

DATA_DIR = Path('data/prices')
COLUMNS = ["Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]

def download_ticker(ticker: str, start = None):
  ticker = ticker.upper()
  if start is None:
    df = yf.Ticker(ticker).history(period="max", auto_adjust=False, actions=True)
  else:
    df = yf.Ticker(ticker).history(start = start, auto_adjust=False, actions=True)
  
  if df.empty:
    if df is None:
      raise ValueError(f"Ticker name '{ticker}' does not exist")
    print(f"Ticker name {ticker} already up to date")
    return df
  
  df.index = df.index.tz_localize(None)
  return df[COLUMNS]

def get_data(ticker: str):
  ticker = ticker.upper()
  path = DATA_DIR / f"{ticker}.csv"

  if not path.exists():
    df = download_ticker(ticker).to_csv(path, index=True)

 
  df_old = pd.read_csv(path, index_col=0, parse_dates=True)
  start = df_old.index.max() + pd.Timedelta(days=1)
  if start > pd.Timestamp.today().normalize():
    print(f"Ticker name {ticker} already up to date")
    return df_old
  
  df_new = download_ticker(ticker, start=start)

  if df_new.empty:
    return df_old
  
  df = pd.concat([df_old,df_new])
  df = df[~df.index.duplicated(keep="last")]
  df.to_csv(path)

  return df

  



if __name__ == "__main__":
  df1 = get_data("QQQ")     
  df2 = get_data("QQQ")     
  print(len(df1), len(df2))
  print(df2.tail(2))