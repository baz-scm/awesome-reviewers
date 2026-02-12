---
title: disallow unsafe schemes
description: 'Treat resource URIs and external references as untrusted input: normalize
  and validate schemes, and reject anything not on an explicit allowlist. Motivation:
  schemes such as file: (and other unsafe schemes like javascript: or data: when used
  for resources) can expose local files or enable injection attacks, and are commonly
  blocked by browsers — so they...'
repository: likec4/likec4
label: Security
language: TypeScript
comments_count: 1
repository_stars: 2582
---

Treat resource URIs and external references as untrusted input: normalize and validate schemes, and reject anything not on an explicit allowlist. Motivation: schemes such as file: (and other unsafe schemes like javascript: or data: when used for resources) can expose local files or enable injection attacks, and are commonly blocked by browsers — so they must not be implicitly trusted.

How to apply:
- Normalize inputs (trim, toLowerCase) before checking.
- Use an allowlist of safe schemes your app requires (e.g., https:, http:) and optionally permit safe relative paths. Reject all others by default.
- For user-provided paths that must reference internal assets, use server-side resolution/whitelisting rather than accepting raw URIs.

Example (pattern adapted from code under review):
// before: filtered out many schemes, but allowed file: was removed
filter(isString)
  .filter(s => {
    const v = s.trim().toLowerCase();
    // allow only http(s) or relative paths starting without a scheme
    return isTruthy(v) && (
      v.startsWith('http:') || v.startsWith('https:') || v.startsWith('.') || v.startsWith('/')
    );
  });

Notes and extensions:
- Consider also rejecting or special-casing other risky schemes (javascript:, data:) depending on context.
- Prefer server-side enforcement for sensitive resources and log/reject invalid attempts.
- Document allowed schemes for each API or component so callers know what is permitted.