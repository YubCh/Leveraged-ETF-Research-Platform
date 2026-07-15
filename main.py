from src.research.stats import describe
from src.data.artificial_data import extend_data    
from src.data.loader import get_data
from src.data.adjust import adjust
from src.visualization.plots import compare
from src.backtesting.dca import dca
qqq = adjust(get_data("QQQ"))
 

# ext = extend_data("TQQQ", 3, 0.0084)
# pre2010 = ext[ext.index < "2010-01-01"]
# pre2001 = ext[ext.index < "2000-03-27"]
# print("peak date:", pre2010.idxmax().date(), " peak value:", round(pre2010.max(), 2))
# print("low before peak", pre2001.idxmin().date(), "low value", round(pre2001.min(), 2))
# print("bottom after peak:", round(pre2010.loc[pre2010.idxmax():].min(), 4))
# print("today:", round(ext.iloc[-1], 2))
# print("today vs 2000 peak:", round(ext.iloc[-1] / pre2010.max() - 1, 4))

# print(ext.iloc[0])


# qqq = adjust(get_data("QQQ"))
# series = {
#     "QQQ": qqq,
#     "QLD (ext)": extend_data("QLD", 2, 0.0095),
#     "TQQQ (ext)": extend_data("TQQQ", 3, 0.0084),
# }
# for name, s in series.items():
#     print(name, describe(s))
# compare(series, title="QQQ vs leveraged QQQ, 1999-2026")

qqq = adjust(get_data("QQQ"))
qld = extend_data("QLD", 2, 0.0095)
tqqq = extend_data("TQQQ", 3, 0.0084)
compare({
    "DCA QQQ":  dca(qqq, 100, 21, 0),
    "DCA QLD":  dca(qld, 100, 21, 0),
    "DCA TQQQ": dca(tqqq, 100, 21, 0),
}, title="$100 monthly since 1999")