---
title: proper span lifecycle management
description: Ensure spans are properly created, attached to async operations, and
  reported at appropriate times to maintain accurate tracing data. Spans that are
  not properly managed will result in incorrect durations, missing trace data, or
  unreliable observability metrics.
repository: cloudflare/workerd
label: Observability
language: Other
comments_count: 5
repository_stars: 6989
---

Ensure spans are properly created, attached to async operations, and reported at appropriate times to maintain accurate tracing data. Spans that are not properly managed will result in incorrect durations, missing trace data, or unreliable observability metrics.

Key practices:
1. **Attach spans to promises**: For JSG methods returning promises, use `context.attachSpans()` to ensure spans remain active for the duration of the async operation
2. **Report events promptly**: Avoid deferring trace event reporting to destructors or cleanup phases where timing information may be stale
3. **Maintain span context**: Pass trace context through call chains to prevent spans from falling out of scope prematurely

Example of correct span attachment:
```cpp
jsg::Promise<jsg::JsRef<jsg::JsValue>> DurableObjectStorageOperations::get(jsg::Lock& js,
    kj::OneOf<kj::String, kj::Array<kj::String>> keys,
    jsg::Optional<GetOptions> maybeOptions) {
  auto& context = IoContext::current();
  auto userSpan = context.makeUserTraceSpan("durable_object_storage.get"_kjc);
  
  // Correct: attach span to promise to maintain lifecycle
  return context.attachSpans(js, getOne(js, kj::mv(s), options), kj::mv(userSpan));
}
```

Avoid patterns where spans immediately fall out of scope or where trace events are reported with stale timing information, as this compromises the accuracy and usefulness of observability data.