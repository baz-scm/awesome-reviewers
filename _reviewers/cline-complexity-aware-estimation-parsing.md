---
title: Complexity-Aware Estimation Parsing
description: 'When implementing “estimation” or “parsing/transform” logic, design
  for both correctness and worst-case performance: (1) don’t let the algorithm scale
  with irrelevant large payload sizes when the true cost depends on a different factor,
  and (2) avoid pathological worst-case parsing constructs (notably regexes that can
  backtrack badly). Enforce these with...'
repository: CLINE/cline
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 70839
---

When implementing “estimation” or “parsing/transform” logic, design for both correctness and worst-case performance: (1) don’t let the algorithm scale with irrelevant large payload sizes when the true cost depends on a different factor, and (2) avoid pathological worst-case parsing constructs (notably regexes that can backtrack badly). Enforce these with explicit bounds and tests.

**Standards**
1. **Use bounded surrogates for cost/metrics**
   - Prefer per-entity costs (e.g., “per image”) over payload-length-based costs (e.g., base64 character count) when the metric you estimate is billed that way.
   - Add tests that compare large vs small payloads and ensure the estimate changes only within expected limits.

2. **Make parsing/normalization complexity-safe**
   - Avoid regex patterns that can degrade badly on long inputs; use linear scans/loops where appropriate.
   - Add explicit caps: maximum bytes processed, maximum recursion/link expansion depth, maximum file counts, etc.

3. **Validate invariants under complex transitions**
   - For stateful logic (pagination/skip/refresh flows), preserve invariants and validate with fuzz/property-style sequences.

**Example (bounded image-token estimation)**
```ts
const CHARS_PER_TOKEN = 3; // legacy baseline used for text blocks
const ESTIMATED_TOKENS_PER_IMAGE = 300; // example: constant per image

function estimateTokensForContent(content: unknown[]): number {
  let tokens = 0;
  for (const block of content) {
    if (typeof block === "string") {
      if (block.trim()) tokens += Math.ceil(block.length / CHARS_PER_TOKEN);
      continue;
    }
    if (block && typeof block === "object" && (block as any).type === "image") {
      // Payload length must not dominate the estimate.
      tokens += ESTIMATED_TOKENS_PER_IMAGE;
    }
  }
  return tokens;
}
```

**Example (complexity-safe trimming)**
```ts
// Avoid backtracking-prone regexes on long runs.
function trimTrailing(value: string, char: string): string {
  let end = value.length;
  while (end > 0 && value[end - 1] === char) end--;
  return value.slice(0, end);
}
```

Adopt this standard whenever you add (a) estimators, (b) document/format parsers, (c) archive/file walkers, or (d) state machines—especially when inputs can be large or adversarial.