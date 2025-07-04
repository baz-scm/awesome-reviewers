---
title: Document observability context flows
description: When implementing observability features like OpenTelemetry exporters,
  metrics collection, or distributed tracing, clearly document the context flow and
  environment limitations. Make explicit which features are available in specific
  environments (development vs. production), how context is propagated between components,
  and provide proper error handling for...
repository: quarkusio/quarkus
label: Observability
language: Other
comments_count: 2
repository_stars: 14667
---

When implementing observability features like OpenTelemetry exporters, metrics collection, or distributed tracing, clearly document the context flow and environment limitations. Make explicit which features are available in specific environments (development vs. production), how context is propagated between components, and provide proper error handling for unsupported configurations.

For testing scenarios, include examples of how to access telemetry data:

```java
// Create a test-friendly exporter
@ApplicationScoped
static class InMemorySpanExporterProducer {
    @Produces
    @Singleton
    InMemorySpanExporter inMemorySpanExporter() {
        return InMemorySpanExporter.create();
    }
}

// Access the telemetry data in tests
@Inject
InMemorySpanExporter inMemorySpanExporter;

// ...

List<SpanData> traces = inMemorySpanExporter.getFinishedSpanItems();
```

When documenting context propagation, clearly specify where annotations should be placed (e.g., on emitter methods vs. processing methods) and how contexts flow through asynchronous boundaries. For unsupported configurations, implement descriptive error messages that guide users toward correct usage patterns.