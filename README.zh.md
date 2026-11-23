# 美股日线数据

[English](./README.md)

## 1. 项目简介

本项目提供 **2019 年以来**的美股日线数据，采用 [Qlib](https://github.com/microsoft/qlib) 二进制格式。每个发布版本以交易日历中的最新交易日命名（`YYYY-MM-DD`），预计在每个交易日结束后更新。

目前覆盖 500 多只股票，详见 [us_stock_list.csv](./us_stock_list.csv)。如果希望加入某只股票，欢迎提交 Issue。

## 2. 发布数据的目录结构与字段

在仓库的 Releases 页面下载 `us_stock-YYYY-MM-DD.tar.gz`。

### 目录结构

```text
us_stock/
├── calendars/
│   └── day.txt                  # 每行一个交易日
├── instruments/
│   └── all.txt                  # 股票代码、起始日期和结束日期，以制表符分隔
└── features/
    └── <symbol>/                # 小写股票代码，例如 aapl
        └── <field>.day.bin      # 每个字段对应一个二进制文件
```

### 数据字段

**说明**　发布的数据已做复权处理。开盘价、最高价、最低价、收盘价和 VWAP 均乘以复权因子，成交量则除以同一个复权因子。

| 字段 | 说明 |
| --- | --- |
| `open` | 开盘价 |
| `high` | 当日最高价 |
| `low` | 当日最低价 |
| `close` | 收盘价 |
| `volume` | 成交量 |
| `vwap` | 成交量加权平均价 |
| `factor` | 源数据提供的复权因子 |

## 3. 数据使用方法

运行 `pip install pyqlib` 安装 Qlib。

```python
import qlib
from qlib.config import REG_US
from qlib.data import D

# 初始化 Qlib
qlib.init(provider_uri="data/us_stock", region=REG_US, kernels=1)

# 读取指定股票和日期范围内的日线数据
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

# 设置字段名，并将股票代码和日期从索引转为列
bars.columns = fields
df = bars.reset_index().rename(columns={"instrument": "symbol"})

print(df.head())
```

## 4. 反馈与建议

欢迎通过 Issue 报告数据问题、反馈程序错误或提出建议。报告数据问题时，请尽量提供发布版本的日期、股票代码和受影响的交易日。

本项目不接受 Pull Request。
