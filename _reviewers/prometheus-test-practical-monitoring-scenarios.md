---
title: test practical monitoring scenarios
description: When writing tests for observability features like metrics, functions,
  and alerting expressions, ensure test cases cover practical, real-world monitoring
  scenarios in addition to edge cases. Focus on common usage patterns that developers
  will actually use in production monitoring and alerting.
repository: prometheus/prometheus
label: Observability
language: Other
comments_count: 2
repository_stars: 59616
---

When writing tests for observability features like metrics, functions, and alerting expressions, ensure test cases cover practical, real-world monitoring scenarios in addition to edge cases. Focus on common usage patterns that developers will actually use in production monitoring and alerting.

For monitoring functions, design expressions that return meaningful results for alerting - avoid functions that return binary 0/1 values when you need to identify specific disappearing time series. Instead, create expressions that contain exactly the series you want to monitor.

Example of good practice:
```
# Test common usage pattern
eval range from 50s to 60s step 10s count_over_time(metric1_total[step()])

# For alerting on disappearing series, use expressions like:
present_over_time(some_metric[1h]) unless present_over_time(some_metric[5m])
```

This approach ensures your observability code works effectively in production monitoring scenarios, not just in isolated test conditions.