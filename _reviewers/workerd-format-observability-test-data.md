---
title: Format observability test data
description: When writing tests for observability systems (tracing, metrics, logging),
  structure test assertions to be easily readable and debuggable. Instead of placing
  complex JSON outputs or structured data on single lines, split them across multiple
  lines with proper formatting.
repository: cloudflare/workerd
label: Observability
language: JavaScript
comments_count: 2
repository_stars: 6989
---

When writing tests for observability systems (tracing, metrics, logging), structure test assertions to be easily readable and debuggable. Instead of placing complex JSON outputs or structured data on single lines, split them across multiple lines with proper formatting.

This approach significantly improves the debugging experience when tests fail, as diff outputs clearly show which specific parts of the observability data don't match expectations. For example, instead of:

```javascript
let expected = [
  '{"type":"onset","executionModel":"stateless","scriptTags":[],"info":{"type":"custom"}}{"type":"spanOpen","name":"fetch","parentSpanId":"0"}{"type":"spanClose","outcome":"ok"}{"type":"outcome","outcome":"ok","cpuTime":0,"wallTime":0}'
];
```

Format it as:

```javascript
let expected = [
  `{"type":"onset","executionModel":"stateless","scriptTags":[],"info":{"type":"custom"}}
   {"type":"spanOpen","name":"fetch","parentSpanId":"0"}
   {"type":"attributes","info":[{"name":"http.request.method","value":"POST"}]}
   {"type":"spanClose","outcome":"ok"}
   {"type":"outcome","outcome":"ok","cpuTime":0,"wallTime":0}`
];
```

This formatting makes future instrumentation changes much easier to inspect and produces clear, line-by-line diff outputs when assertions fail, allowing developers to quickly identify exactly which observability events or attributes are incorrect.