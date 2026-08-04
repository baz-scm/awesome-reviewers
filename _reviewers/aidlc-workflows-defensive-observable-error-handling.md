---
title: Defensive Observable Error Handling
description: 'Coding standard for hook/compose-style tooling: never fail silently;
  parse defensively; gate writes by installed compatibility; and make transient failures
  self-healing. Diagnostics must only fail on real faults (e.g., stale markers), not
  normal in-flight states.'
repository: awslabs/aidlc-workflows
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 3849
---

Coding standard for hook/compose-style tooling: never fail silently; parse defensively; gate writes by installed compatibility; and make transient failures self-healing. Diagnostics must only fail on real faults (e.g., stale markers), not normal in-flight states.

Apply:
1) Normalize & parse defensively
- Treat real-world inputs as messy: handle CRLF, trailing newlines, inline-empty forms, and whitespace.
```ts
const t = toolResult.trim();
const m = t.match(/^Created the (.+) file\.$/);
```
- Prefer tolerant parsing for YAML-ish lists: support both `field: []` and block lists; don’t rely on a regex that only matches one form.

2) No silent no-ops: log “can’t apply” cases
- If a contribution/merge can’t be applied because a target field is missing or unknown keys are encountered, write a drop/log entry (don’t just return unchanged).
```ts
if (!hasField(content, 'produces')) {
  recordDrop(`contribution to ${target}: no 'produces:' field; adds dropped`);
  return content;
}
```
- For declared-but-unimplemented surfaces, explicitly log that the key is deferred/ignored.

3) Compatibility gate writes by installed schema
- If a new optional field may be unknown to older engine versions, probe the installed engine schema (or capability) before editing stage files, and skip+log when unsupported.

4) Make transient failures recoverable
- Avoid “compile gate” logic that can turn a one-off failure into a permanent broken state.
- Persist a retry marker on compile failure and clear it on success, or trigger recompilation when the merged artifacts aren’t present in the compiled graph.

5) Health/doctor outputs: fail only on real faults
- When you detect an in-flight artifact (e.g., a compose marker), compute TTL freshness and set `pass` accordingly (fresh = pass, stale = fail). This prevents false red CI runs.
```ts
const pass = ageMs <= COMPOSE_MARKER_TTL_MS; // fresh advisory ok
results.push({ pass, message: pass ? 'fresh' : 'stale' });
```