"""Shared strategy definitions.

This file is imported, never run. Every script builds its
strategies from the build_all function so that adding a strategy has always the  identical parameters. So every input can be changed hee.
"""
from src.data.loader import get_data
from src.data.adjust import adjust
from src.data.artificial_data import simulate
from src.backtesting.dca import dca
from src.backtesting.switch import switch_dca
from src.backtesting.strategy import defined_drawdown_window, sma_strategy, dip_switch

PARAMS = dict(income=100, income_period=10, invest_period=10,
              start_capital=1000, start_date=0)

DIP = dict(max_at=50, min_at=20, window=125)
SMA_RATE = 200

#differs per asset

PLAIN_ASSET = "QQQ"
LEVERAGED_ASSET = "TQQQ"
LEVERAGE = 3
EXPENSE_RATIO = 0.0084


NAMES = [f"{PLAIN_ASSET} DCA", f"{LEVERAGED_ASSET} DCA", f"{LEVERAGED_ASSET} dip", f"{LEVERAGED_ASSET} SMA DCA"]

COLORS = {f"{PLAIN_ASSET} DCA": "green", f"{LEVERAGED_ASSET} DCA": "red",
          f"{LEVERAGED_ASSET} dip": "blue", f"{LEVERAGED_ASSET} SMA DCA": "orange"}

def build_asset(plain_asset):
    return {
    "plain":plain_asset,
    "leveraged":simulate(plain_asset, LEVERAGE, EXPENSE_RATIO)
}

def build_all(plain_asset_prices):
    """Build every strategy's portfolio series from one plain_assets price path.
    The leveraged asset is simulated from the same path, so in Monte Carlo all
    strategies live in the same universe and only the strategy differs.
    """
    leveraged = simulate(plain_asset_prices, LEVERAGE, EXPENSE_RATIO)
    return {
        f"{PLAIN_ASSET} DCA":  dca(plain_asset_prices, None, **PARAMS),
        f"{LEVERAGED_ASSET} DCA": dca(leveraged, None, **PARAMS),
        f"{LEVERAGED_ASSET} dip": dca(leveraged, defined_drawdown_window(leveraged, **DIP), **PARAMS),
        f"{LEVERAGED_ASSET} SMA DCA": dca(leveraged, sma_strategy(leveraged, SMA_RATE), allow_sell=True, **PARAMS),
    }

def build_addtional(plain_asset_prices):
    leveraged = simulate(plain_asset_prices,LEVERAGE, EXPENSE_RATIO)
    return {
        f"dip switch {plain_asset_prices} to {leveraged}": switch_dca(plain_asset_prices, leveraged,
                                 dip_switch(plain_asset_prices, enter_at=20, window=125),
                                 **PARAMS),
        f"dip switch {leveraged} to {plain_asset_prices}": switch_dca(plain_asset_prices, leveraged,
                                 dip_switch(plain_asset_prices, enter_at=20, window=125),
                                 **PARAMS),
    }

def maxdd(series):
    #dd from all time high
    return (series / series.cummax() - 1).min()