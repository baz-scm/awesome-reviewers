---
title: implement proper observability
description: Ensure observability mechanisms (events and metrics) are implemented
  correctly with appropriate types, accurate labeling, and user-focused messaging.
  Use events for user-visible information that appears in `kubectl describe`, not
  just internal logging. Choose correct event types (`EventTypeNormal` for waiting
  states, `EventTypeWarning` for actual failures)...
repository: kubernetes/kubernetes
label: Observability
language: Go
comments_count: 7
repository_stars: 116489
---

Ensure observability mechanisms (events and metrics) are implemented correctly with appropriate types, accurate labeling, and user-focused messaging. Use events for user-visible information that appears in `kubectl describe`, not just internal logging. Choose correct event types (`EventTypeNormal` for waiting states, `EventTypeWarning` for actual failures) and provide consistent, descriptive messages that identify relevant resources like nodes and devices. Avoid duplicate events by checking if they're already being emitted elsewhere in the flow. For metrics, use precise labels that match the actual operation context and employ direct metric operations (`Inc`/`Dec`) when appropriate.

Example of proper event usage:
```go
// Good: Informational event for waiting state
pl.fh.EventRecorder().Eventf(claim, pod, v1.EventTypeNormal, "BindingConditionsPending", "Scheduling", 
    "waiting for driver to report status for device %s/%s/%s on node %s.", 
    deviceRequest.Driver, deviceRequest.Pool, deviceRequest.Device, nodeName)

// Good: Proper metric labeling
f.metricsRecorder.ObservePluginDurationAsync(metrics.PreBindPreFlight, pl.Name(), status.Code().String(), metrics.SinceInSeconds(startTime))
```

This ensures users can effectively troubleshoot issues through `kubectl describe` while maintaining accurate system metrics for monitoring and debugging.