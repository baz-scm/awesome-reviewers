---
title: Complete observability documentation
description: Ensure documentation for observability systems provides comprehensive
  information including all required permissions, complete configuration options,
  and clear warnings about operational impacts. Monitoring and metrics systems often
  have significant performance and security implications that users must understand
  to operate them safely.
repository: prometheus/prometheus
label: Observability
language: Markdown
comments_count: 4
repository_stars: 59616
---

Ensure documentation for observability systems provides comprehensive information including all required permissions, complete configuration options, and clear warnings about operational impacts. Monitoring and metrics systems often have significant performance and security implications that users must understand to operate them safely.

Key requirements:
- Include all necessary permissions (e.g., "list/watch" not just "get" for Kubernetes resources)
- Provide complete technical explanations with proper context (e.g., custom histogram bucket values work like 'le' labels in classic histograms)
- Add explicit warnings about performance trade-offs, especially for configurations that can cause high memory usage or time series churn
- Use clear, actionable language that helps users make informed decisions

Example of good documentation:
```yaml
# Promoting all resource attributes to labels, except the ignored ones. 
# 'ignore_resource_attributes' can be used to promote all resource attributes if set to an empty list:
#
#  otlp:
#    ignore_resource_attributes: []
#
# Be aware that changes in attributes received by the OTLP endpoint may result in time series churn and lead to high memory usage by the Prometheus server.
```

This approach prevents operational issues, security gaps, and user confusion in production monitoring systems.