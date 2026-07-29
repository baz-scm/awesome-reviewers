---
title: Harden auth and output
description: 'Security-sensitive data and sinks must be hardened before use. Concretely:


  1) Auth/token validity guarantees

  - When returning or printing OAuth/bearer tokens, ensure the token is proactively
  refreshed if it’s close to expiring.'
repository: earendil-works/pi
label: Security
language: TypeScript
comments_count: 3
repository_stars: 79783
---

Security-sensitive data and sinks must be hardened before use. Concretely:

1) Auth/token validity guarantees
- When returning or printing OAuth/bearer tokens, ensure the token is proactively refreshed if it’s close to expiring.
- Implement this in the shared auth path (e.g., `getAuth`) so all call sites benefit, using a refresh threshold that matches real provider behavior (e.g., provider-specific skew rather than a one-size-fits-all 30 minutes).

2) Sanitize strings embedded into terminal escape sequences
- Before constructing OSC 8 (or other control-sequence) hyperlinks, strip control characters from any untrusted URL/string (e.g., remove `\x00-\x1f` and `\x7f`).

3) Use secure, permissioned temp locations
- Prefer an app-controlled temp root (respecting a canonical directory helper / env override) with strict permissions (e.g., `0700`).
- Create a unique subdirectory per invocation/session to prevent cross-process stomping.
- Avoid relying on raw `tmpdir()` unless you can enforce the same security model.

Example (sanitizing OSC 8 link URLs):
```ts
function stripControlChars(s: string): string {
  return s.replace(/[\x00-\x1f\x7f]/g, "");
}

const href = stripControlChars(token.href ?? "");
const osc8Open = `\x1b]8;;${href}\x07`;
const osc8Close = `\x1b]8;;\x07`;
```