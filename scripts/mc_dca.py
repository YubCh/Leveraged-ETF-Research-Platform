import pandas as pd
from src.research.monte_carlo import block_bootstrap
from src.data.artificial_data import simulate, get_data, adjust
from src.visualization.plots import compare
from src.backtesting.dca import dca
from src.backtesting.strategy import defined_drawdown

qqq = adjust(get_data("qqq"))
paths = block_bootstrap(qqq, n_paths=500)
_3x = simulate(qqq,3,0.0084)

paths_3x = [simulate(p, 3, 0.0084) for p in paths]
plain = dca(_3x,None,100,21,21,0,0)
path_plain = [dca(p,None,100,21,21,0,0) for p in paths_3x]

tqqq_drawdown = dca(_3x, defined_drawdown(_3x,30,10,1), 100,21,21,0,0)
path_drawdown = [dca(p,defined_drawdown(p,30,10,1), 100,21,21,0,0) for p in paths_3x]

compare({"plain dca TQQQ": plain, "tqqq 1": path_plain[0], "tqqq 2": path_plain[1], "tqqq 3": path_plain[2]}, normalize=True)

compare({"dd dca TQQQ": tqqq_drawdown, "dd tqqq 1": path_drawdown[1], "dd tqqq 2": path_drawdown[2], "dd tqqq 3": path_drawdown[3]})

plain_finals = pd.Series([p.iloc[-1] for p in path_plain])
dd_finals = pd.Series([d.iloc[-1] for d in path_drawdown])
print(plain_finals.describe(percentiles=[0.05, 0.5, 0.95]))
print(dd_finals.describe(percentiles=[0.05, 0.5, 0.95]))
print("grad wins in", (dd_finals > plain_finals).mean())