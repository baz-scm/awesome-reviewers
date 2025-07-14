---
title: Use appropriate metric types
description: 'When instrumenting applications with metrics, choose the correct metric
  type based on what you''re measuring to ensure accurate and useful observability
  data:'
repository: nodejs/node
label: Observability
language: Markdown
comments_count: 3
repository_stars: 112178
---

When instrumenting applications with metrics, choose the correct metric type based on what you're measuring to ensure accurate and useful observability data:

1. **Use monotonic (increase-only) counters** for events or cumulative quantities to ensure compatibility with systems like Prometheus that expect strictly increasing values.

2. **Use histograms or distributions for durations** rather than simple counters, as durations represent a distribution of values.

3. **Consider specialized gauge types** for specific use cases, such as high-water mark gauges for tracking peak values:

```javascript
// GOOD: Using a histogram/distribution for request durations
const requestDuration = createHistogram('api.request.duration.ms');
function handleRequest(req, res) {
  const startTime = performance.now();
  // Process request...
  requestDuration.record(performance.now() - startTime);
}

// GOOD: Using a monotonic counter for counting events
const apiCalls = createCounter('api.calls.total');
function handleRequest(req, res) {
  apiCalls.increment();
  // Process request...
}

// GOOD: Using a high-water mark gauge for tracking peak memory usage
const memoryHighWaterMark = createHighWaterMarkGauge('memory.peak.bytes');
setInterval(() => {
  memoryHighWaterMark.update(process.memoryUsage().heapUsed);
}, 1000);
```

Choosing the right metric type ensures that monitoring systems can correctly interpret and visualize your data, leading to more meaningful insights and better observability.