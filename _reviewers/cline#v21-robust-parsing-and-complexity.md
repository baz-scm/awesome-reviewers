---
title: Robust Parsing And Complexity
description: When implementing algorithms that transform structured text/state (parsers,
  token estimators, diff/change collectors, path mappers, state-window logic), optimize
  for correctness under adversarial inputs and predictable performance.
repository: cline/cline#v21
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When implementing algorithms that transform structured text/state (parsers, token estimators, diff/change collectors, path mappers, state-window logic), optimize for correctness under adversarial inputs and predictable performance.

Apply these rules:
1) Use boundary-aware parsing: when a field can contain delimiter characters, split only on the first N delimiters and keep the remainder intact.
2) Normalize representations explicitly: when generating paths/keys, convert to a consistent separator scheme so literal characters (e.g., backslashes) aren’t accidentally treated as escapes.
3) Keep state scoped to the correct window: for stateful computations across turns/steps, ensure older or out-of-scope messages don’t leak into current results.
4) Prefer complexity-safe implementations: avoid regex patterns that can backtrack badly on long inputs; use loops/finite scans for trimming/search.
5) Add targeted tests for edge cases that break the naive algorithm (tab-containing filenames, payload-size changes, separator cases, and “only the newest prompt matters” scoping).

Example (boundary-aware parsing):
```ts
// Wrong: `record.split("\t")` can break filenames containing tabs.
// Right: split on the first two tabs, keep the remainder as the filename.
const [add, del, inlinePath] = record.split("\t");
// If you need “first two tabs only”, use an index-based split:
const i1 = record.indexOf("\t");
const i2 = record.indexOf("\t", i1 + 1);
const add2 = record.slice(0, i1);
const del2 = record.slice(i1 + 1, i2);
const path = record.slice(i2 + 1); // remainder preserved
```

Example (path normalization):
```ts
import path from "node:path";
import { toPosixSeparators } from "your-utils";

const relative = path.relative(workspaceRoot, absFilePath);
const normalized = toPosixSeparators(relative); // keep literal backslashes intact
```

Adopting this standard prevents subtle correctness bugs (wrong scope, mangled filenames) and avoids performance cliffs (regex backtracking, unbounded naive logic).