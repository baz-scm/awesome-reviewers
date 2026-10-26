---
title: Integration-lean Test Strategy
description: When writing tests, prefer validating behavior at the real boundary (real
  adapters/real CLI commands) and keep mocking limited to true external effects—avoid
  “test plumbing” that makes tests brittle, non-portable, or overly coupled to implementation
  details.
repository: cline/cline#v5
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 70864
---

When writing tests, prefer validating behavior at the real boundary (real adapters/real CLI commands) and keep mocking limited to true external effects—avoid “test plumbing” that makes tests brittle, non-portable, or overly coupled to implementation details.

Apply this standard:
- Prefer integration-style coverage for adapter/boundary correctness (e.g., run the real adapter; stub only outbound network/files). Don’t paper over type/runtime mismatches with unit-only mocks when you can assert the real request/response path.
- Avoid heavy mocking that breaks platform support or changes semantics. If the only way to assert something (like process counts) is to mock Node internals or rely on shell/PATH hacks, favor behavioral assertions using real artifacts/snapshots instead.
- Don’t assert on incidental outputs (like exact log payload shapes) unless logs are an explicit contract. Use existing server/behavioral tests for regression coverage instead of wiring up fragile log-spy harnesses.
- For CI/smoke checks, choose the smallest reliable probe that catches runtime regressions; avoid adding complex instrumentation (PID tracking, extra teardown logic) unless it addresses a known failure mode.
- Keep tests resilient to drift by importing exported constants (versions/identifiers) rather than hardcoding ephemeral values.

Example pattern (real adapter + stub external effect):
```ts
// Stub only fetch/network; exercise the real adapter through the boundary.
vi.stubGlobal('fetch', vi.fn().mockResolvedValue(/* fake OpenAI response */));
const result = await transcribeAudio(/* openai-native config */);
expect(fetch).toHaveBeenCalledWith(
  expect.stringContaining('/v1/audio/transcriptions'),
  expect.anything(),
);
expect(result.transcript).toBe(/* expected */);
```

Outcome: tests catch real regressions with less brittleness and less platform-specific harness code.