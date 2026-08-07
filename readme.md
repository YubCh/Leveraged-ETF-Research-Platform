# Leveraged ETF Research Platform

Backtesting framework analyzing leveraged ETFs like QLD and TQQQ from QQQ or SSO and UPRO from SPY across 27 years of market history - including the dot-com crash that real leveraged funds never lived through.

The core idea: leveraged ETF's like TQQQ(2010) only exist after the post crash of the dot-com bubble and the subprime-mortage crisis. This project reconstructs their full history from the underlying index and validates the reconstruction against the real funds (~0.999 daily-return correlation), so different strategies can be tested.

## The problem this project solves

Is leveraged strategy actually better than just buying the index.


## Key findings

- TQQQ Lost to QQQ over 1999-2026. Synthetic TQQQ compounded at ~4.3%/year vs QQQ's ~10.9% with a -99.97% max drawdown during the dot-com bubble and spent ~26years underwater before recently hitting its previous all time high before the dot-com bubble burst. - invisible in every TQQQ backtest that starts in 2010.

- buying over and selling under the 200 day SMA on leveraged DCA eliminates catastrophic drawdowns 0 vs 13 drawdowns >= 80% on TQQQ and reduces the drawdown depth in 90% of our monte-carlo bootstrapped histories, but only wins at 31% in final wealth. It is an insurance - you end up selling many small drawdowns to avoid crashes but usually end up with less final wealth but in a safer way.  


-




## How it works

``` data  -> strategy -> executor -> measure -> visualize
```

- data: download, divided-adjust, simulate the leveraged series, splice the synthetic history onto real (if needed)
- strategy: stock - cash allocation (```1.0```= fully invested, ```0.0``` = holding full cash, ```Nan``` = don't trade)
- executor: ```python dca() ``` runs any strategy, investing period and amount, start capital and time, optionally allowed to sell
- measure: ```python describe_portfolio()```
- visualize: stock charts, drawdown histogram, outcome distributions 


## How to Run
```python
python3 -m venv .venv
source .venv/bin/active
pip install -r requirements.txt

python main.py

# Each single executions
# python -m scripts.real_history
# python -m scripts.monte_carlo
# python -m scripts.drawdown_counts

```



## Caveats

- all simulated histories are reshuffles of one real 1999 - 2026 period. Those are plausible paths but do not predict the future

- no transactions costs, taxes or bid- ask spread are taken in account

- Drawdowns are used in a 125days window. Years of decline can be counted as multiple drawdowns rather than a single drawdown. V-shape rebounds can be not listed: if the window starts in 2025 April it misses the ~25% drawdown that rebounded and hit its all time high around in 125 days which results in 0% drawdown.