---
title: Cache deterministic results
description: When an operation is deterministic and expensive (often due to external
  IO like `yfinance`), avoid doing the same work twice. Use bounded memoization for
  repeated lookups and explicitly short-circuit cases where two inputs resolve to
  the same underlying entity. Also ensure caches don’t leak between tests.
repository: TauricResearch/TradingAgents
label: Caching
language: Python
comments_count: 2
repository_stars: 71953
---

When an operation is deterministic and expensive (often due to external IO like `yfinance`), avoid doing the same work twice. Use bounded memoization for repeated lookups and explicitly short-circuit cases where two inputs resolve to the same underlying entity. Also ensure caches don’t leak between tests.

Practical rules:
- Memoize pure/deterministic lookup helpers (e.g., mapping ticker → company name) with an LRU cache and a reasonable `maxsize`.
- Add a regression test that asserts repeated calls don’t re-trigger the expensive construction/work.
- Ensure test isolation by clearing caches between tests (e.g., via an `autouse` fixture).
- Before fetching “stock” and “benchmark” data, resolve/compare the benchmark and reuse the already-fetched history when they refer to the same underlying ticker.

Example pattern:

```python
from functools import lru_cache
import yfinance as yf

@lru_cache(maxsize=128)
def company_name(ticker: str) -> str:
    return yf.Ticker(ticker).info.get("longName") or ""

def fetch_returns(ticker: str, benchmark: str, trade_date, end_str):
    stock = yf.Ticker(ticker).history(start=trade_date, end=end_str)

    # Avoid redundant external call when both refer to the same entity
    if benchmark == ticker:
        bench = stock
    else:
        bench = yf.Ticker(benchmark).history(start=trade_date, end=end_str)

    # ...compute metrics using stock and bench...
    return stock, bench
```
