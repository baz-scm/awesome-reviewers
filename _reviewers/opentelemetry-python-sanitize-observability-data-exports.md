---
title: Sanitize observability data exports
description: 'When exporting observability data (metrics, traces, logs) to external
  systems, properly sanitize all data fields to ensure compatibility and consistency.
  Key requirements:'
repository: open-telemetry/opentelemetry-python
label: Observability
language: Python
comments_count: 6
repository_stars: 2061
---

When exporting observability data (metrics, traces, logs) to external systems, properly sanitize all data fields to ensure compatibility and consistency. Key requirements:

1. Metric Names:
- Remove invalid characters, replacing with underscores
- Handle leading digits by prefixing with underscore
- Maintain consistent casing (lowercase recommended)

2. Label Keys:
- Remove special characters except alphanumeric
- Ensure uniqueness after sanitization
- Use consistent ordering for multi-label metrics

3. Label Values:
- Convert all values to strings
- Escape special characters
- Handle multi-value concatenation with semicolons

Example:

```python
def sanitize_metric_name(name: str) -> str:
    # Handle leading digit
    if name and name[0].isdigit():
        name = "_" + name
    # Replace invalid chars with underscore
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)

def sanitize_label_key(key: str) -> str:
    # Remove special chars
    return re.sub(r"[^a-zA-Z0-9]", "_", key)

def format_label_value(value: Any) -> str:
    # Convert to string and escape
    return str(value).replace("\\", "\\\\").replace("\n", "\\n")

# Usage
metric_name = sanitize_metric_name("2xx.success.rate") # "_2xx_success_rate"
label_key = sanitize_label_key("status.code") # "status_code"
label_value = format_label_value(200) # "200"
```

This ensures reliable data export and prevents issues with downstream observability systems while maintaining semantic meaning of the original data.