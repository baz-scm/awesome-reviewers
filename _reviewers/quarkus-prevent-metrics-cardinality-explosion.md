---
title: Prevent metrics cardinality explosion
description: When implementing metrics and telemetry in your application, avoid using
  dynamic values like path parameters or user IDs directly as metric tags or dimensions.
  This practice causes cardinality explosion, which leads to excessive memory usage,
  degraded performance, and can overwhelm your monitoring systems.
repository: quarkusio/quarkus
label: Observability
language: Java
comments_count: 2
repository_stars: 14667
---

When implementing metrics and telemetry in your application, avoid using dynamic values like path parameters or user IDs directly as metric tags or dimensions. This practice causes cardinality explosion, which leads to excessive memory usage, degraded performance, and can overwhelm your monitoring systems.

Instead:

1. Use route templates rather than actual paths:
   - Good: `/client-endpoint-with-path-param/{name}` as a metric tag
   - Bad: `/client-endpoint-with-path-param/123` as a metric tag

2. For high-cardinality data like tenant IDs or user identifiers:
   - Store them in span attributes for tracing
   - Use exemplars to correlate metrics with traces
   - Query APM systems for detailed analysis

Example of proper implementation:

```java
// WRONG: Will cause cardinality explosion
@Path("template/path/{value}")
public class PathTemplateResource {
    @GET
    public String get(@PathParam("value") String value) {
        // Don't do this - adds a high-cardinality tag
        ContextLocals.put("metric-tag", value);
        // ...
    }
}

// CORRECT: Uses route templates instead
@Path("template/path/{value}")
public class PathTemplateResource {
    @GET
    public String get(@PathParam("value") String value) {
        // For tracing/debugging, put in span attributes instead
        Span.current().setAttribute("path.value", value);
        // ...
    }
}
```

Remember that for each unique tag value, you multiply the number of time series across all other dimensions (methods, status codes, endpoints), which can quickly overwhelm your metrics system.