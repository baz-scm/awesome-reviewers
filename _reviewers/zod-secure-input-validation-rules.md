---
title: Secure Input Validation Rules
description: 'When validating security-sensitive inputs (IDs, hostnames, tokens, IPs,
  payment-like numbers), ensure the implementation is strict, resilient, portable,
  and non-leaky:'
repository: colinhacks/zod
label: Security
language: TypeScript
comments_count: 7
repository_stars: 42628
---

When validating security-sensitive inputs (IDs, hostnames, tokens, IPs, payment-like numbers), ensure the implementation is strict, resilient, portable, and non-leaky:

- Be explicit about sanitation/normalization: don’t name or treat data as “sanitized” unless the required transformation is actually applied before validation.
- Validate the real accepted grammar and edge cases: tighten patterns/logic so you don’t over-accept (e.g., punycode hostnames must include a complete form; JWT header `typ` checks should tolerate valid variants like `JWT-at`).
- Harden regex to reduce ReDoS risk: if a regex is used on attacker-controlled input, prefer patterns that avoid catastrophic backtracking and ensure security tooling/lint rules are satisfied (or justify the exception).
- Keep parsing runtime-portable: don’t use Node-only APIs (e.g., `Buffer`) if the code must run in browsers; prefer `atob`/universal helpers.
- Avoid leaking user-controlled input in error messages: security-related validation errors should not echo “received” raw values back to clients.

Example (portable JWT header decode + non-leaky error style):
```ts
function decodeHeader(headerB64: string) {
  // Convert base64url to base64, then decode in browser-compatible way
  const b64 = headerB64.replace(/-/g, "+").replace(/_/g, "/")
    .padEnd(headerB64.length + ((4 - (headerB64.length % 4)) % 4), "=");
  return JSON.parse(atob(b64));
}

function validateTyp(decoded: any) {
  if ("typ" in decoded && !decoded.typ?.startsWith("JWT")) return false;
  return true;
}

// Error message should not include the raw received discriminator/token/input.
const message = "Invalid discriminator value. Expected one of: ...";
```

Apply this checklist to every change involving validation/parsing logic, regexes, and security-related error reporting.