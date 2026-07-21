from src.research.monte_carlo import block_bootstrap
from src.data.artificial_data import get_data, adjust
from src.visualization.plots import compare




def run():
    qqq = adjust(get_data("QQQ"))
    paths = block_bootstrap(qqq, n_paths=5)
    vol_sim = [p.pct_change().std() * 252**0.5 for p in paths]
    pct_sim_min = [p.pct_change().min() for p in paths]
    pct_sim_mean = [p.pct_change().mean() for p in paths]
    pct_sim_max = [p.pct_change().max() for p in paths]
    
    vol_real = qqq.pct_change().std() * 252 ** 0.5
    pct_real = [qqq.pct_change().min(), qqq.pct_change().mean(), qqq.pct_change().max()]
    print(f"simulated vol: {vol_sim}")
    print(f"real vol: {vol_real}")
    print(f"pct_sim_min: {pct_sim_min}")
    print(f"pct_sim_mean: {pct_sim_mean}")
    print(f"pct_sim_max: {pct_sim_max}")
    print(f"pct_real: {pct_real}")

    compare({"real QQQ": qqq, "path 0": paths[0], "path 1": paths[1], "path 2": paths[2]}, normalize=True)
    

run()