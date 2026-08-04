---
title: Deterministic External Testing
description: When external services are flaky or untestable, make CI deterministic
  by (1) pruning recorded interactions to the stable outcomes your playback will actually
  match, and (2) using narrowly-scoped linter/test exclusions only when a dependency
  prevents meaningful coverage.
repository: Azure/azure-cli
label: Testing
language: Yaml
comments_count: 2
repository_stars: 4592
---

When external services are flaky or untestable, make CI deterministic by (1) pruning recorded interactions to the stable outcomes your playback will actually match, and (2) using narrowly-scoped linter/test exclusions only when a dependency prevents meaningful coverage.

How to apply:
- Recorded HTTP/VCR tests (playback)
  - Remove transient error interactions from recordings (e.g., occasional 5xx) unless your playback matcher/expectations truly require them.
  - Verify how your VCR matchers behave (body/header matching, request counting). If default matchers don’t differentiate by body or don’t enforce counts, keep only the single “expected success” response for the call path exercised in playback.
  - Keep the recording aligned with what the SDK will do during replay (e.g., one DELETE → one successful 200).
- Linter/test exclusions
  - Use exclusions only for the specific parameter/command that cannot be tested due to an external dependency.
  - Justify the exclusion with: dependency reason, why meaningful testing isn’t possible right now, and why the value is effectively fixed for users.
  - Keep the exclusion minimal and revisit once the external service behavior is fixed.

Example (VCR/playback YAML intent):
- If you see multiple recorded failures for the same request, keep only the stable success entry(s) needed for replay (e.g., remove transient `DELETE` 500s, leaving a single 200), ensuring the playback still matches the request your code issues.