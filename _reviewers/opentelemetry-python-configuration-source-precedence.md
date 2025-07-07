---
title: Configuration source precedence
description: Define and document a clear precedence order when configurations come
  from multiple sources (code parameters, environment variables, defaults). Typically,
  explicit parameters should take precedence over environment variables, which should
  take precedence over defaults.
repository: open-telemetry/opentelemetry-python
label: Configurations
language: Python
comments_count: 5
repository_stars: 2061
---

Define and document a clear precedence order when configurations come from multiple sources (code parameters, environment variables, defaults). Typically, explicit parameters should take precedence over environment variables, which should take precedence over defaults.

For collection-based configurations, decide whether sources should be merged (additive) or replaced:

```python
# Additive approach (params + env vars)
span_exporters = _import_exporters(
    span_exporter_names + _get_exporter_names("traces"),
    # ...
)

# Replacement approach (params override env vars)
headers = self._headers or tuple()
# Instead of: headers = tuple(_OTLP_GRPC_HEADERS)

# Feature flags for breaking changes
if not environ.get("OTEL_PYTHON_EXPERIMENTAL_DISABLE_PROMETHEUS_UNIT_NORMALIZATION"):
    # Apply new normalization behavior
    metric_name = sanitize_full_name(metric.name)
    metric_unit = map_unit(metric.unit)
else:
    # Use legacy behavior
    metric_name = self._sanitize(metric.name)
```

Document the precedence behavior clearly, especially for components that might be configured through multiple mechanisms. Consider providing temporary opt-out mechanisms via environment variables when making breaking configuration changes.