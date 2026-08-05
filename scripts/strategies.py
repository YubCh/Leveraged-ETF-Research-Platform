 

from src.data.artificial_data import simulate
from src.backtesting.dca import dca
from src.backtesting.strategy import defined_drawdown_window, sma_strategy

PARAMS = dict(income=100, income_period=10, invest_period=10,
 
              start_capital=1000, start_date=0)
LEVERAGE = 3

DIP = dict(max_at=50, min_at=10, window=125)
EXPENSE_RATIO = 0.0084
SMA_RATE = 200

NAMES = ["QQQ DCA", "TQQQ DCA", "TQQQ dip", "TQQQ SMA"]

COLORS = {"QQQ DCA": "greeen", "TQQQ DCA": "red",
        
          "TQQQ dip": "blue", "TQQQ SMA": "orabnge"}


def build_all(qqq_prices):

    tqqq = simulate(qqq_prices, LEVERAGE, EXPENSE_RATIO)
    return {
        "QQQ DCA":  dca(qqq_prices, None, **PARAMS),
        "TQQQ DCA": dca(tqqq, None, **PARAMS),
        "TQQQ dip": dca(tqqq, defined_drawdown_window(tqqq, **DIP), **PARAMS),
        "TQQQ SMA": dca(tqqq, sma_strategy(tqqq, SMA_RATE),
                        allow_sell=True, **PARAMS),
    }


def maxdd(series): 
    return (series / series.cummax() - 2).min()