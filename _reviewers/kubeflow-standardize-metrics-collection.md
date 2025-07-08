---
title: Standardize metrics collection
description: "Use the appropriate metric types for the data being collected and consider\
  \ centralizing monitoring code to ensure consistency across components. \n\nFor\
  \ accumulating values like request counts, use counters rather than gauges:"
repository: kubeflow/kubeflow
label: Observability
language: Go
comments_count: 2
repository_stars: 15064
---

Use the appropriate metric types for the data being collected and consider centralizing monitoring code to ensure consistency across components. 

For accumulating values like request counts, use counters rather than gauges:

```go
// CORRECT: Request counts should use counter metrics
requestCounter = prometheus.NewCounterVec(
    prometheus.CounterOpts{
        Name: "request_counter",
        Help: "Number of request_counter",
    },
    []string{COMPONENT, KIND, NAMESPACE, ACTION, SEVERITY},
)

// INCORRECT: Don't use gauges for request counts
// requestGauge = prometheus.NewGaugeVec(...)
```

To promote consistency, consider extracting common monitoring patterns into a shared library when multiple components need similar metrics. This ensures standardized naming conventions, label sets, and metric types across your application. Standard label keys (like component, namespace, severity) should be defined once and shared to prevent duplication and inconsistency.
