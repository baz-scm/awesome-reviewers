---
title: Event Pairing Invariants
description: 'When processing ordered event streams (logs, messages, tool calls),
  don’t apply heuristics that assume events will be well-formed. Instead, encode explicit
  invariants:'
repository: cline/cline#v5
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70864
---

When processing ordered event streams (logs, messages, tool calls), don’t apply heuristics that assume events will be well-formed. Instead, encode explicit invariants:
- Define the identity key(s) for matching (e.g., command + request ID + client ID).
- Treat “start/initiated” and “end/completed” as a pair: apply effects only when the matching terminal event is observed with the required success condition.
- Preserve unmatched or failed/incomplete pairs (don’t drop them).
- Scope computations to the intended window/turn so earlier events can’t leak into later decisions.

Minimal pattern (pairing with a keyed map):
```ts
type Key = string; // e.g., `${command}:${requestId}:${clientId}`
const pending = new Map<Key, { startLine: string; startIndex: number }>();

const startsToKeep: string[] = [];
const outputLines: string[] = [];

for (const line of lines) {
  const { command, requestId, clientId, ok } = parseLine(line);
  const key = command && requestId && clientId ? `${command}:${requestId}:${clientId}` : null;

  const isStart = line.includes('"message":"command.start"');
  const isEnd = line.includes('"message":"command.end"');

  if (key && isStart) {
    pending.set(key, { startLine: line, startIndex: outputLines.length });
    // don’t emit yet (or mark as removable)
    continue;
  }

  if (key && isEnd) {
    const p = pending.get(key);
    pending.delete(key);
    if (!p) {
      outputLines.push(line); // unknown pair; keep conservative
    } else if (ok) {
      // matched successful end => safe to drop the start
      outputLines.push(line);
    } else {
      // failed end => keep both start and end
      outputLines.splice(p.startIndex, 0, p.startLine);
      outputLines.push(line);
    }
    continue;
  }

  outputLines.push(line);
}

// Any pending starts never ended: keep them so stalled systems still show up.
for (const p of pending.values()) {
  outputLines.splice(p.startIndex, 0, p.startLine);
}
```

Use this standard when: (1) selecting among fallback candidates under eligibility constraints, (2) summarizing logs while avoiding false negatives, or (3) computing derived “facts” from message histories. The goal is to make the algorithm respect ordering, identity, and success/failure semantics via data structures and bounded scope—not via ad-hoc filtering.