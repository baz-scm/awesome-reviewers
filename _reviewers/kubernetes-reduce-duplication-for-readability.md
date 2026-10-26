---
title: Reduce Duplication For Readability
description: 'Write code so intent is immediately obvious: avoid repeated boilerplate,
  collapse near-identical branches, and centralize shared logic/values.


  Practical rules:'
repository: kUbernetes/kUbernetes
label: Code Style
language: Go
comments_count: 15
repository_stars: 128688
---

Write code so intent is immediately obvious: avoid repeated boilerplate, collapse near-identical branches, and centralize shared logic/values.

Practical rules:
- Extract repeated patterns into small helpers (including test helpers) instead of duplicating large blocks.
- Parameterize the differences (e.g., pass policy/topology as an argument) rather than copying whole functions.
- Move additive variants into dedicated files (e.g., *_resize.go/*_resize_test.go) so the original path is clearly unchanged.
- Prefer named struct initializers and clear variable names over positional literals.
- Replace complex boolean expressions with intermediate variables; remove redundant conditions.
- Use constants/shared explanations for repeated values/comments; avoid bespoke one-off helpers when a standard constructor suffices.
- Keep helpers close to where they’re used (especially test-only helpers) rather than growing generic shared packages.

Example (boolean readability + dedupe):
```go
// Instead of one dense conditional, name the pieces.
websocketTunnel := utilfeature.DefaultFeatureGate.Enabled(features.ExtendWebSocketsToKubelet) &&
	wsstream.IsWebSocketRequestWithTunnelingProtocol(request.Request)

if websocketTunnel {
	servermetrics.IncStreamingWebSocketRequest("portforward")
	// ...
}
```

Example (test/body dedupe):
```go
topologyPolicyTest := func(topoPolicy string, /* other args */) {
	// common test setup and assertions here
}

// Use it for each policy instead of copying the full test body.
topologyPolicyTest("none", ...)
topologyPolicyTest("best-effort", ...)
```