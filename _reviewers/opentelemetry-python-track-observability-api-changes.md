---
title: Track observability API changes
description: Stay informed about API changes in observability libraries like OpenTelemetry,
  especially during their active development phases. Ensure that both implementation
  code and documentation are updated to reflect the current API patterns.
repository: open-telemetry/opentelemetry-python
label: Observability
language: Other
comments_count: 2
repository_stars: 2061
---

Stay informed about API changes in observability libraries like OpenTelemetry, especially during their active development phases. Ensure that both implementation code and documentation are updated to reflect the current API patterns.

When implementing observability tooling:
1. Verify import paths and method names against the currently used library version
2. Document which version of the library your code is compatible with
3. Regularly review observability code when upgrading dependencies

For example, note how OpenTelemetry's API changed between versions:

```python
# For older OpenTelemetry 0.4:
from opentelemetry.ext.flask_util import instrument_app
tracer.add_span_processor(span_processor)

# For newer OpenTelemetry versions:
from opentelemetry.ext.flask import instrument_app
trace.tracer_provider().add_span_processor(span_processor)
```

Maintaining correct configuration is essential for collecting accurate telemetry data. Inconsistent or outdated observability code can result in missing or incorrect metrics, traces, and logs.