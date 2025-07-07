---
title: Place attributes correctly
description: 'When implementing observability with OpenTelemetry, place attributes
  at the appropriate level in the telemetry hierarchy to ensure effective data collection
  and analysis:'
repository: open-telemetry/opentelemetry-python
label: Observability
language: Markdown
comments_count: 4
repository_stars: 2061
---

When implementing observability with OpenTelemetry, place attributes at the appropriate level in the telemetry hierarchy to ensure effective data collection and analysis:

1. **Use resource attributes** for static, process-level information that applies globally:
   ```python
   # Good: Static information as resource attributes
   resource = Resource.create({
       "environment": "production",
       "service.name": "api-server",
       "service.version": "1.0.0"
   })
   meter_provider = MeterProvider(resource=resource)
   ```

2. **Use baggage** only for appropriate correlation use cases:
   ```python
   # Good: Valid baggage usage
   processor = BaggageMeasurementProcessor(baggage_keys=["user.id", "synthetic_request"])
   
   # Bad: Don't use trace.id in baggage; use exemplars instead for trace correlation
   ```

3. **Avoid timestamps as metric attributes** - timestamps are already handled by the telemetry system:
   ```python
   # Bad: Don't add timestamps to metrics
   new_attributes["processed_at"] = str(int(time.time()))  # Avoid this!
   ```

4. **Add instrument-specific attributes** using the proper API methods:
   ```python
   # Good: Use proper attribute fields in API calls
   meter = meter_provider.get_meter("name", "version", schema_url="url", attributes={"component": "billing"})
   ```

This approach reduces cardinality issues, improves query performance, and follows OpenTelemetry best practices for attribute placement.