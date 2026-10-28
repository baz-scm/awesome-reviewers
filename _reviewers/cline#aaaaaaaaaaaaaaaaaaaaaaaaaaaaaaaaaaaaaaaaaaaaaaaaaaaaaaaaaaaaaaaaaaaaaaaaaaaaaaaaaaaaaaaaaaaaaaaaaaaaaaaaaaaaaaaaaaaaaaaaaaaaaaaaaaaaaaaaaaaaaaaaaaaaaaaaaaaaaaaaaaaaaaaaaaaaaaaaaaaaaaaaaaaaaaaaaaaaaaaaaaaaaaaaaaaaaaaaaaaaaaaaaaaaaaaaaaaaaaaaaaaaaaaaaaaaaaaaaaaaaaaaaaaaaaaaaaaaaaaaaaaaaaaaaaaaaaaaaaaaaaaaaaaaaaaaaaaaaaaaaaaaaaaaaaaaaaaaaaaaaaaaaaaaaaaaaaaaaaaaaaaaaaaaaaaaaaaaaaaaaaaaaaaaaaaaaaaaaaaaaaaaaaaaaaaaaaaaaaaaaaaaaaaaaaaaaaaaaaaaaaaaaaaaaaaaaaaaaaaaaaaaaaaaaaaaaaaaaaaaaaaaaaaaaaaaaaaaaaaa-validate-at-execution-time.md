---
title: Validate at execution time
description: 'Security-sensitive decisions must be verified against authoritative
  state at the moment they are acted on, never inferred from cached, client-side,
  or structurally unsafe data. Two concrete rules follow from this:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Security
language: TSX
comments_count: 2
repository_stars: 70964
---

Security-sensitive decisions must be verified against authoritative state at the moment they are acted on, never inferred from cached, client-side, or structurally unsafe data. Two concrete rules follow from this:

1. Authorization/eligibility gating (e.g., exposing a privileged command like `/cloud`) must not rely solely on a feature flag or cached session/manifest data (git URL, branch, connection state). That cached data can be used to improve UX (e.g., hiding an option early), but the actual authorization — repo access, account/GitHub permissions, dirty state, remote reachability — must be re-validated server-side at execution time before the privileged action is performed.

2. When looking up a value using an external or attacker-influenced string as an object key (e.g., a file extension or user input), use an own-property check instead of plain bracket/dot access on a plain object. Plain lookups can resolve to inherited `Object.prototype` members (`constructor`, `__proto__`, `toString`, etc.) for malicious or unexpected keys, leading to incorrect behavior or prototype-pollution-style bugs.

Example fix for safe key lookup:
```ts
const EXTENSION_LANGUAGES: Record<string, string> = { ts: "typescript", ... };

function languageForExtension(extension: string): string | undefined {
  // Avoid falling through to inherited properties like constructor/__proto__
  return Object.hasOwn(EXTENSION_LANGUAGES, extension)
    ? EXTENSION_LANGUAGES[extension]
    : undefined;
}
```

Apply this pattern (or use a `Map` instead of a plain object) whenever a lookup table is indexed by external input, and always perform live, authoritative checks before granting access to privileged operations rather than trusting cached flags.