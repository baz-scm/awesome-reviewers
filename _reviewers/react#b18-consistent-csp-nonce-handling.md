---
title: Consistent CSP nonce handling
description: When merging or batching security-sensitive resources (e.g., CSP-nonced
  style/script tags into a shared queue), the nonce must be captured once—at resource/queue
  creation time—and treated as authoritative for all subsequent additions to that
  resource. Do not perform lazy, per-item nonce checks that assume the first value
  is always valid; this hides the fact...
repository: facebook/react#b18
label: Security
language: JavaScript
comments_count: 1
repository_stars: 251889
---

When merging or batching security-sensitive resources (e.g., CSP-nonced style/script tags into a shared queue), the nonce must be captured once—at resource/queue creation time—and treated as authoritative for all subsequent additions to that resource. Do not perform lazy, per-item nonce checks that assume the first value is always valid; this hides the fact that a correctly configured app will consistently pass the same nonce (or none) for every related resource.

Critically, never silently merge or combine content (e.g., concatenating style text) from items that specify different nonce values. Doing so can violate the intent of the CSP `style-src`/`script-src` directives and produce output whose nonce doesn't match what was actually configured for part of the merged content. If a mismatch is detected, either keep the resources separate or emit a clear dev-only warning so the misconfiguration is caught early instead of producing a silently insecure or broken CSP setup.

Example of the risk to guard against:
```js
// Two <style> tags with different nonces should NOT be merged into one output
// with a single nonce attribute — this can defeat CSP enforcement.
<style href="foo" precedence="default" nonce="nonceA">{'.foo{color:red}'}</style>
<style href="bar" precedence="default" nonce="nonceB">{'.bar{color:blue}'}</style>
```
Instead, validate nonce consistency up front (ideally with a dev-only warning when nonces differ) and treat the nonce as a fixed, early-known property of the resource rather than something re-evaluated per call.</description>
</invoke>
