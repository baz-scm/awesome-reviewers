---
title: Spec-Aligned Parsing Algorithms
description: When implementing parsing/transform/estimation algorithms for structured
  inputs, prioritize **format-correct tokenization**, **stateful correctness**, and
  **complexity safety**.
repository: ClInE/cLiNe
label: Algorithms
language: TypeScript
comments_count: 9
repository_stars: 70838
---

When implementing parsing/transform/estimation algorithms for structured inputs, prioritize **format-correct tokenization**, **stateful correctness**, and **complexity safety**.

**Standards**
1) **Tokenize by the real wire format, not by intuition**
- If the producer uses NUL-separated records, split on `"\0"` and respect record boundaries.
- If a field can contain delimiters (e.g., filenames with TABs), split only on the first *N* delimiters and keep the remainder.

2) **Use state machines for paired/stream semantics**
- For log/event streams, don’t drop items with heuristics. Pair `start` and `end` using stable keys (e.g., command + request id + client id), and only apply transformations when the required end condition is met.

3) **Avoid duplicated “business rules” in parsers**
- If there is a canonical implementation (e.g., an SDK), call into it so precedence rules can’t drift (e.g., `disabled` wins over legacy `enabled: false`).
- When inline vs block structures matter (e.g., YAML frontmatter), ensure your “range length” logic follows the real grammar.

4) **Prevent pathological complexity**
- Avoid regex patterns known to backtrack badly on adversarial input; prefer linear scans/loops.

5) **Enforce bounds while reading/processing**
- Cap sizes (archives, buffers, text bytes) and ensure truncation behavior is explicit and tested.

**Example: stateful pairing filter (pattern)**
```ts
const pollingCommands = new Set([
  "session.list",
  "settings.list",
  "schedule.list",
  "schedule.upcoming",
  "schedule.list_executions",
  "schedule.active",
]);

// Drop a polling start line only if the matching successful end appears later.
export function dropPollingStarts(text: string): string {
  // Maintain seen starts by key; consume when an ok end is observed.
  const seen = new Map<string, boolean>();
  const lines = text.split("\n");

  const keyOf = (line: string) => {
    // Extract: command + requestId + clientId (implementation depends on log shape)
    // Return null when not a relevant polling command line.
    // (Use safe parsing; avoid overly permissive regex.)
    return null as string | null;
  };

  // First pass: mark matching start/end success.
  for (const line of lines) {
    const key = keyOf(line);
    if (!key) continue;
    if (line.includes('"message":"command.start"')) seen.set(key, false);
    if (line.includes('"message":"command.end"') && line.includes('"ok":true')) seen.set(key, true);
  }

  // Second pass: drop only those starts whose matching end was successful.
  return lines.filter((line) => {
    const key = keyOf(line);
    if (!key) return true;
    if (line.includes('"message":"command.start"')) return seen.get(key) !== true;
    return true;
  }).join("\n");
}
```
Apply the same principles to git-output parsing, YAML frontmatter parsing, and token/billing estimators: make delimiter/grammar handling explicit, keep algorithms linear-time, and back correctness with targeted tests for tricky inputs.