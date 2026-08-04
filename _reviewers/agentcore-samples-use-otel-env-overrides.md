---
title: Use OTEL Env Overrides
description: When configuring OTLP tracing exporters in observability code, rely on
  the runtime-provided `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS`
  environment variables, rather than hardcoding or redundantly passing `endpoint=`
  and `headers=` into `OTLPSpanExporter`. This prevents configuration drift and duplicated
  settings.
repository: awslabs/agentcore-samples
label: Observability
language: Other
comments_count: 2
repository_stars: 3244
---

When configuring OTLP tracing exporters in observability code, rely on the runtime-provided `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS` environment variables, rather than hardcoding or redundantly passing `endpoint=` and `headers=` into `OTLPSpanExporter`. This prevents configuration drift and duplicated settings.

Example (omit redundant exporter overrides):
```python
import os
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Configure only resource/service metadata in code
resource = Resource.create({
    "model_id": "agentcore-strands-agent",
})

provider = TracerProvider(resource=resource)

# Do NOT set endpoint= / headers= here if the launch environment already sets:
#   OTEL_EXPORTER_OTLP_ENDPOINT
#   OTEL_EXPORTER_OTLP_HEADERS
exporter = OTLPSpanExporter()
provider.add_span_processor(BatchSpanProcessor(exporter))
```

Apply this by: (1) removing in-code `endpoint`/`headers` overrides, (2) documenting which OTEL env vars must be supplied to the process/container/agent launch, and (3) ensuring CI/CD or deployment manifests provide those variables consistently.