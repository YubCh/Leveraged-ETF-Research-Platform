from src.data.loader import download_ticker, get_data
from src.data.adjust import adjust
from src.data.artificial_data import simulate
import pandas as pd
import yfinance as yf


 
def test_adjust(ticker):
    ours = adjust(download_ticker(ticker))
    yahoo = yf.download(ticker, period="max", auto_adjust=False)["Adj Close"].squeeze()
    #yahoo uses 20xx-xx-xx 00:00:00+00:00 timezone
    yahoo.index = pd.to_datetime(yahoo.index).tz_localize(None)
    both = pd.concat([ours.rename("ours"), yahoo.rename("yahoo")], axis=1).dropna()

    #ours / both -1 gives us a ratio. the biggest difference should be below 0.001 which is equivalent to 0.1% price difference 
    assert (both["ours"] / both["yahoo"] - 1).abs().max() < 0.001

  

if __name__ == "__main__":
    for t in ["QQQ", "QLD", "TQQQ"]:
     test_adjust(t)