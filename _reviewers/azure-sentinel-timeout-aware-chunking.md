---
title: Timeout-Aware Chunking
description: For any long-running ingestion/connectors, optimize for throughput while
  preventing timeout failures. Implement (1) near-timeout early exit and (2) realistic,
  configurable chunk/batch sizing.
repository: Azure/Azure-Sentinel
label: Performance Optimization
language: Python
comments_count: 2
repository_stars: 6042
---

For any long-running ingestion/connectors, optimize for throughput while preventing timeout failures. Implement (1) near-timeout early exit and (2) realistic, configurable chunk/batch sizing.

How to apply:
- Timeout-aware loop: In record-processing loops, compute a deadline with a safety margin and stop when you’re close to the platform’s execution limit. Persist progress/state before returning so the job can resume.
- Chunk/batch sizing: Avoid overly small fixed chunk sizes. Set chunk size based on realistic API/data limits (e.g., payload capacity) and observed performance, and make it configurable.

Example (Python-style):
```python
import os
import time
from datetime import datetime, timedelta

fetch_delay = int(os.getenv("FetchDelay", 10))
chunksize = int(os.getenv("ChunkSize", 10000))  # tune based on payload limits

# Assume the runtime provides a total timeout; configure a safety margin.
# Example: stop 30s before timeout.
safety_seconds = int(os.getenv("TimeoutSafetySeconds", 30))
runtime_timeout_seconds = int(os.getenv("RuntimeTimeoutSeconds", 300))
dealine = time.time() + (runtime_timeout_seconds - safety_seconds)

processed = 0
for chunk in get_next_chunks(chunksize):
    if time.time() >= deadine:
        save_progress(processed)
        return  # exit early to avoid hard timeout

    process_chunk(chunk)
    processed += len(chunk)

    time.sleep(fetch_delay)
```

This reduces bottlenecks (larger, appropriate chunks) and prevents hard failures (early exit before timeouts).