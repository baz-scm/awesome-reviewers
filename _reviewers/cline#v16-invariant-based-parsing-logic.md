---
title: Invariant-Based Parsing Logic
description: When implementing parsing/filtering/estimation algorithms, define the
  exact invariants your logic must preserve, then encode them as structure-aware state
  machines—not ad-hoc regex/heuristics—and bound worst-case work.
repository: cline/cline#v16
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70882
---

When implementing parsing/filtering/estimation algorithms, define the exact invariants your logic must preserve, then encode them as structure-aware state machines—not ad-hoc regex/heuristics—and bound worst-case work.

Checklist:
- Preserve structure: if the upstream format can reuse request IDs/paths (e.g., rename/copy, paired log lines), carry the extra key fields needed to maintain correctness.
- Use explicit pairing/order rules: drop/keep decisions should be driven by complete patterns (e.g., “start is dropped only if a successful end follows”), not by partial matches.
- Make estimates invariant to payload shape: billing/token estimates must reflect the intended complexity unit (e.g., per image), not raw payload size (base64 length).
- Enforce bounds: cap file counts, scan bytes, link expansion depth, and avoid operations with catastrophic performance (e.g., regex patterns with polynomial backtracking). Prefer linear loops for untrusted input.
- Normalize and validate paths: convert to a canonical relative form and reject anything that escapes the intended root.
- Add tests for edge cases and “oracle parity” where possible (e.g., SDK parser rules, real git porcelain outputs, payload-size extremes).

Example (pairing-based filtering):
```ts
function shouldDropPollingStart(lines: string[]) {
  // Invariant: only drop a start line when its own successful end appears after it.
  // Maintain per (clientId, requestId, command) sequence state.
  // If there is no successful end, keep the start (so the report shows the hub is alive/stuck).
}
```

Apply this standard to parsing/token-estimation/filtering code paths so correctness holds under real-world adversarial formats and worst-case input sizes.