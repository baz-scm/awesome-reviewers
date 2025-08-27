---
title: Use structured logging
description: Always use structured logging methods like klog.InfoS and klog.ErrorS
  instead of unstructured methods like klog.Infoln, klog.Infof, or klog.Errorln. Structured
  logging improves log parsing, analysis, and monitoring capabilities. Additionally,
  ensure log messages are clear, descriptive, and provide complete context about actions
  taken and values being set.
repository: volcano-sh/volcano
label: Logging
language: Go
comments_count: 5
repository_stars: 4899
---

Always use structured logging methods like klog.InfoS and klog.ErrorS instead of unstructured methods like klog.Infoln, klog.Infof, or klog.Errorln. Structured logging improves log parsing, analysis, and monitoring capabilities. Additionally, ensure log messages are clear, descriptive, and provide complete context about actions taken and values being set.

Key requirements:
- Use klog.InfoS/ErrorS for structured logging with key-value pairs
- Choose appropriate log levels (InfoS for informational messages, ErrorS for actual errors)
- Write clear, descriptive messages that explain what action is being taken
- Include relevant context and final values in log messages
- Add strategic logging to help with debugging and performance monitoring

Example transformation:
```go
// Bad - unstructured logging
klog.Infoln("pod=", pod.Name, "scoreMap=", gs.ScoreMap[pod.Name])
klog.ErrorS(nil, "loadPlugin", "pathxxx", pluginPath) // wrong level for non-error

// Good - structured logging
klog.InfoS("Scoring node for pod", "pod", pod.Name, "score", gs.ScoreMap[pod.Name])
klog.InfoS("Loading plugin", "path", pluginPath)

// Bad - unclear message
klog.V(3).Infof("node %s is not ready,need continue", n.Name)

// Good - clear, descriptive message
klog.V(3).InfoS("Node is not ready/unschedulable, skipping node", "node", n.Name)
```