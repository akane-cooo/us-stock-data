import qlib
from qlib.config import REG_US
from qlib.data import D

# initialize qlib
qlib.init(provider_uri="data/us_stock", region=REG_US, kernels=1)

# read stock data frame
symbols = ["AAPL", "MSFT"]
start, end = "2026-09-01", "2026-11-20"
fields = ["open", "high", "low", "close", "volume"]

bars = D.features(
    symbols,
    ["$" + field for field in fields],
    start_time=start,
    end_time=end,
    freq="day",
)

bars.columns = fields
df = bars.reset_index().rename(columns={"instrument": "symbol"})

print(df.head())
