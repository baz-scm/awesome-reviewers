---
title: Stable API Contract Changes
description: When changing an externally consumed interface (proto schemas and client-facing
  CLI/API surfaces), treat the contract as versioned and compatibility-sensitive.
repository: cline/cline#v30
label: API
language: Other
comments_count: 3
repository_stars: 70894
---

When changing an externally consumed interface (proto schemas and client-facing CLI/API surfaces), treat the contract as versioned and compatibility-sensitive.

Apply this checklist:
1) **Use the generator + source of truth** for API/proto artifacts
- If a file is generated from a canonical source (e.g., `state-keys.ts` → `state.proto`), make changes in the canonical source, then **re-run the generator** and confirm the generated output matches what should be committed.
- Run the repo’s schema/type validation (e.g., `npm run protos` / `npm run check-types`) to catch drift early.

2) **Preserve proto wire compatibility**
- For removed/renamed enum values, **do not reuse** their numeric IDs.
- Instead, reserve the old values:
```proto
enum ClineAsk {
  // ... keep existing values
  reserved 14;
  reserved "REPORT_BUG";
}
```

3) **Keep client-facing interface docs/examples aligned with parsing semantics**
- For CLI-style APIs with positional arguments, ensure documentation examples place flags/options in the position the parser expects (e.g., options before the channel/command so they actually reach the underlying connector).
- Example of the principle:
```md
# Wrong (flags after positional arg may not be routed)
cline connect telegram --stop

# Right (flags before positional arg)
cline connect telegram --stop
# (and likewise for --restart)
```

Outcome: fewer breaking changes, fewer mismatched docs, and safer evolution of API/proto contracts.