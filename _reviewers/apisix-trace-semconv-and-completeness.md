---
title: Trace semconv and completeness
description: 'Make observability outputs standards-compliant and fully observable.


  Apply this when writing instrumentation and when publishing tracing/telemetry examples:'
repository: apache/apisix
label: Observability
language: Markdown
comments_count: 2
repository_stars: 16922
---

Make observability outputs standards-compliant and fully observable.

Apply this when writing instrumentation and when publishing tracing/telemetry examples:
1) **Validate semantic conventions**: For HTTP-related telemetry, ensure attributes conform to the OpenTelemetry HTTP semantic conventions (semconv). If you have older non-compliant attributes, you may keep them (deprecated/legacy), but **add new compliant attributes** so downstream analysis remains correct.
2) **Handle the complete signal in examples**: Code samples that demonstrate telemetry must log/handle the primary emitted data and lifecycle events—at minimum **data** plus **end** (and **error**), not just headers/metadata.

Example (stream handling in an observability-oriented gRPC-Web example):
```js
const stream = client.lotsOfReplies(req, {});

stream.on('metadata', (metadata) => {
  console.log('Response headers:', metadata);
});

stream.on('data', (response) => {
  console.log('Reply:', response.getReply());
});

stream.on('end', () => {
  console.log('Stream ended');
});

stream.on('error', (err) => {
  console.error('Error:', err);
});
```

Example (semantic convention compliance principle):
- When your trace/log sample shows HTTP attributes that don’t match the http semconv registry, add the correct semconv-aligned attribute(s) (and keep legacy ones if needed), so observability tooling can reliably interpret fields.