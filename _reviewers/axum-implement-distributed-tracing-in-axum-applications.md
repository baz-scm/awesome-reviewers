---
title: "Implement Distributed Tracing in Axum Applications"
description: "As an Axum code reviewer, I recommend implementing proper distributed tracing in your Axum-based web applications to ensure observability across service boundaries. Use Axum's built-in middleware layers to consistently instrument your code."
repository: "tokio-rs/axum"
label: "Axum"
language: "TypeScript"
comments_count: 2
repository_stars: 22100
---

As an Axum code reviewer, I recommend implementing proper distributed tracing in your Axum-based web applications to ensure observability across service boundaries. Use Axum's built-in middleware layers to consistently instrument your code:

1. **Propagate Request IDs**: Use the `tower_http::request_id` middleware to generate and propagate unique request IDs across service calls. This allows you to correlate requests and trace their flow through your distributed system.

```typescript
import { Router } from '@awslabs/aws-lambda-typescript-runtime';
import { RequestIdLayer } from '@awslabs/aws-lambda-typescript-runtime/middleware';

const app = Router.create()
  .use(RequestIdLayer.create({
    headerName: 'x-request-id',
    generateRequestId: () => crypto.randomUUID()
  }));
```

2. **Implement Structured Logging with Trace Context**: Leverage the `tower_http::trace` middleware to add detailed tracing information to your application logs. This allows you to correlate log entries with specific requests and understand the flow of execution.

```typescript
import { Router } from '@awslabs/aws-lambda-typescript-runtime';
import { TraceLayer } from '@awslabs/aws-lambda-typescript-runtime/middleware';

const app = Router.create()
  .use(TraceLayer.create({
    makeSpan: (req) => {
      return tracing.info('request', {
        requestId: req.headers.get('x-request-id') || 'unknown',
        method: req.method,
        uri: req.url.pathname
      });
    }
  }));
```

3. **Integrate with OpenTelemetry**: Consider using the `@opentelemetry/api` and `@opentelemetry/sdk-node` packages to connect your Axum application to a standardized observability backend, such as Jaeger, Zipkin, or a cloud-native monitoring platform. This allows you to export traces and metrics for deeper analysis and debugging.

By implementing these patterns, you can effectively debug production issues, understand service dependencies, and measure performance across your distributed Axum-based system.