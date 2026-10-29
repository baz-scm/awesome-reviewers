---
title: Redact credentials at export boundaries
description: 'Any path by which data can leave the trust boundary — tracing/OTLP export,
  debug logs, error messages, DB persistence, cached results, or API responses — must
  pass through a shared sanitizer that scrubs credentials before the data is written,
  logged, or serialized. Treat this as a defense-in-depth problem, not a single regex:
  credentials appear as headers...'
repository: promptfoo/promptfoo
label: Security
language: TypeScript
comments_count: 21
repository_stars: 26565
---

Any path by which data can leave the trust boundary — tracing/OTLP export, debug logs, error messages, DB persistence, cached results, or API responses — must pass through a shared sanitizer that scrubs credentials before the data is written, logged, or serialized. Treat this as a defense-in-depth problem, not a single regex: credentials appear as headers (`Authorization`, `Cookie`, custom bearer headers), query parameters (including signed-URL params like `X-Amz-Signature`, `sig`), JSON/YAML key-value pairs (plural and camelCase/snake_case variants of `token`, `secret`, `apiKey`, `password`, `credential`, `authorization`), URL userinfo, CLI flags (`--user`, `-u`), JWTs/JWKs/JWEs, and nested/serialized JSON embedded inside a larger string. Each of these shapes needs its own matcher and regression test, run against every real export format the data can take (e.g. both JSON and protobuf exporters, DB round-trip, polling APIs), not just the code path being changed. Build redaction centrally (one sanitizer reused everywhere) rather than duplicating ad hoc logic per call site, since new call sites (e.g. a new provider, a new log statement, a new retry/rate-limit path) are easy to forget and must inherit the same protection. When sanitization itself can fail (parse error, oversized/]recursive input, getter that throws), fail closed by omitting or redacting the field rather than throwing the raw value into the output. Example of the kind of gap to watch for:
```ts
// Bad: only strips the known top-level field; header-based credentials and
// nested secrets in config still leak when serialized.
toJSON() {
  return { ...this.config, apiKey: undefined };
}

// Good: route through the shared sanitizer so headers, nested objects, and
// provider-specific secret shapes are all covered.
toJSON() {
  return sanitizeProviderConfig(this.config);
}
```