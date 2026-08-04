---
title: Tracing schema and continuity
description: 'When adding or integrating agent frameworks/invocation paths, ensure
  observability works end-to-end by meeting BOTH requirements: (1) the emitted telemetry
  conforms to the documented OpenTelemetry/OpenInference schema (not merely “OTLP
  transport”), and (2) trace context is propagated across boundaries (e.g., Lambda
  → AgentCore) so traces are continuous and...'
repository: awslabs/agentcore-samples
label: Observability
language: Markdown
comments_count: 3
repository_stars: 3244
---

When adding or integrating agent frameworks/invocation paths, ensure observability works end-to-end by meeting BOTH requirements: (1) the emitted telemetry conforms to the documented OpenTelemetry/OpenInference schema (not merely “OTLP transport”), and (2) trace context is propagated across boundaries (e.g., Lambda → AgentCore) so traces are continuous and visible.

Practical rules:
- Schema conformance: only claim support/evaluability if your instrumentation emits the documented OpenTelemetry/OpenInference fields/structures used by downstream tooling for operation classification and correlation (for example, framework attributes and the expected `scope.name`). Don’t assume that any OTLP-emitting custom scope is supported.
- Context propagation: in serverless or multi-hop setups, verify that upstream trace context is carried into the downstream runtime (e.g., install/configure the required Lambda layer or instrumentation so the trace continues into AgentCore).
- Validation: run a real invocation/evaluation and confirm in your trace/trace-UI that (a) the expected span/event structure appears and (b) Lambda and the agent execution are correlated in a single trace.

Example checklist (pseudo):
```text
1) Instrumentation emits OpenTelemetry/OpenInference per docs
   - validate required semantic fields/structures exist in emitted events/spans
2) Trace continuity across hops
   - Lambda -> AgentCore: ensure trace context propagation is configured
3) Validate in UI
   - confirm single end-to-end trace and presence of Lambda + agent spans
```