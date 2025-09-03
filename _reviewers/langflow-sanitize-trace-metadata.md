---
title: sanitize trace metadata
description: Always sanitize trace metadata and attributes before sending to observability
  platforms to ensure compatibility with OpenTelemetry attribute type restrictions.
  Complex objects, custom types, and non-primitive values should be converted to supported
  types (str, int, float, bool, None) or JSON strings to prevent warnings and ensure
  reliable trace data.
repository: langflow-ai/langflow
label: Observability
language: Python
comments_count: 2
repository_stars: 111046
---

Always sanitize trace metadata and attributes before sending to observability platforms to ensure compatibility with OpenTelemetry attribute type restrictions. Complex objects, custom types, and non-primitive values should be converted to supported types (str, int, float, bool, None) or JSON strings to prevent warnings and ensure reliable trace data.

Implement sanitization methods that:
- Keep primitive types (str, int, float, bool, None) as-is
- Convert lists/tuples by sanitizing each element
- Serialize dicts and complex objects to JSON strings with fallback to str()

Example implementation:
```python
def sanitize_for_otel(value):
    """Sanitize values for OpenTelemetry attribute compatibility."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    elif isinstance(value, (list, tuple)):
        return [sanitize_for_otel(item) for item in value]
    elif isinstance(value, dict):
        try:
            return json.dumps(value)
        except (TypeError, ValueError):
            return str(value)
    else:
        return str(value)

# Usage in trace metadata
span.set_attributes({
    key: sanitize_for_otel(value) 
    for key, value in metadata.items()
})
```

This prevents OpenTelemetry warnings like "Invalid type StructuredTool in attribute" and ensures consistent trace data across different observability platforms (Traceloop, Opik, Arize Phoenix).