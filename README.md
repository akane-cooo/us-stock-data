# US Stock Data

## 1. Introduction

U.S. stock daily data in [Qlib's](https://github.com/microsoft/qlib) binary format **since 2019**. Each release is named after the latest trading date in its calendar (`YYYY-MM-DD`). The new release expected after each trading day.

Currently there are 500+ stocks in the list: [us_stock_list.csv](./us_stock_list.csv). Feel free to submit issue if you would like to include specific stocks. 

## 2. Release Data Structure and Fields
Download `us_stock-YYYY-MM-DD.tar.gz` from the release page.

### Released data structure
```text
us_stock/
├── calendars/
│   └── day.txt                  # Trading dates, one per line
├── instruments/
│   └── all.txt                  # Symbol, first date, and last date (tab-separated)
└── features/
    └── <symbol>/                # Lowercase stock symbol, such as aapl
        └── <field>.day.bin      # One binary file per field
```
### Stock data fields:
**Note**: All fields have been processed with adjustment factors. Open, high, low, close, and VWAP are multiplied by the adjustment factor, and trading volume is divided by the same factor. factor. 
| Field | Description |
| --- | --- |
| `open` | Opening price |
| `high` | Highest price during the trading day |
| `low` | Lowest price during the trading day |
| `close` | Closing price |
| `volume` | Trading volume |
| `vwap` | Volume-weighted average price |
| `factor` | Factor value supplied by the source data |

## 3. How to use data
install qlib: `pip install pyqlib`

```python
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

# filter and rename columns
bars.columns = fields
df = bars.reset_index().rename(columns={"instrument": "symbol"})

print(df.head())
```

## 4. Contributing

Issues are welcome for data problems, bug reports, and suggestions. When reporting a data problem, please include the release date, stock symbol, and affected trading dates if available.

This project does not accept pull requests.
