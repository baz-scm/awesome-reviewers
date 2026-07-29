---
title: Spec-Driven Parsing
description: 'For any code that parses/normalizes strings or aggregates structured
  events, require deterministic, complete, and bounded logic:


  - **Complete inputs:** When computing stats/metrics, include every event type that
  can contribute (including newly added variants like tool/compaction usage, memory,
  etc.).'
repository: earendil-works/pi
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 79783
---

For any code that parses/normalizes strings or aggregates structured events, require deterministic, complete, and bounded logic:

- **Complete inputs:** When computing stats/metrics, include every event type that can contribute (including newly added variants like tool/compaction usage, memory, etc.).
- **Deterministic parsing:** Implement normalization using an explicit state machine (e.g., quote states) so semantics match the target interpreter/shell.
- **Avoid unbounded heuristics in core utilities:** Don’t embed large, ad-hoc fallback search strategies in foundational helpers. If special-casing is unavoidable, keep it **narrow, gated (platform/feature flag), and bounded**.
- **Semantics-preserving optimizations:** If you add caching or segmentation (e.g., grapheme width), verify you didn’t change granularity/behavior; preserve intended meaning before optimizing.

Example (quote-aware normalization pattern):
```ts
export function normalizeNulRedirects(command: string): string {
  if (process.platform !== "win32") return command;

  let out = "";
  let inSingle = false;
  let inDouble = false;

  for (let i = 0; i < command.length; i++) {
    const ch = command[i];

    if (ch === "'" && !inDouble) inSingle = !inSingle;
    else if (ch === '"' && !inSingle) {
      const escaped = (() => {
        let bs = 0;
        for (let k = i - 1; k >= 0 && command[k] === "\\"; k--) bs++;
        return bs % 2 === 1;
      })();
      if (!escaped) inDouble = !inDouble;
    }

    out += ch;

    // Only rewrite redirects when not inside quotes (bounded, deterministic)
    // if (!inSingle && !inDouble && matchesNulRedirectAt(i, command)) { ... }
  }

  return out;
}
```

Apply the same standard to metrics aggregation: ensure guards don’t accidentally skip new contributors (e.g., treat any entry type with `usage` as a candidate for token/cost accumulation).