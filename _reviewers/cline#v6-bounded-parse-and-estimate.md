---
title: Bounded Parse And Estimate
description: When implementing parsing, diff analysis, or token/cost estimation algorithms,
  optimize for (a) spec-accurate handling of edge cases and multi-part records and
  (b) provable bounds on runtime/memory so behavior can’t degrade on adversarial or
  simply-large inputs.
repository: cline/cline#v6
label: Algorithms
language: TypeScript
comments_count: 8
repository_stars: 70864
---

When implementing parsing, diff analysis, or token/cost estimation algorithms, optimize for (a) spec-accurate handling of edge cases and multi-part records and (b) provable bounds on runtime/memory so behavior can’t degrade on adversarial or simply-large inputs.

Do:
- Parse with the exact protocol grammar: preserve the remainder of a record after fixed separators (e.g., for `diff --numstat -z`, split only the first two tabs and keep the rest as the filename), and handle multi-record constructs (e.g., `git status` rename/copy where the original path appears in the next record).
- Avoid delimiter bugs: treat filenames as opaque after the defined split points; add tests for tricky filenames (tabs, backslashes).
- Use complexity-safe primitives: avoid regex patterns known to backtrack pathologically on long strings; prefer linear-time loops.
- Enforce hard caps while streaming: limit downloaded/read sizes during IO rather than buffering everything first; cap recursive/linked expansions by depth.
- For estimators/caps: model the real invariants (e.g., image payload length shouldn’t dominate token estimates; compute synthesized defaults as floors/ceilings that preserve prior allowances), and encode those invariants in tests.

Example pattern (delimiter-preserving parsing):
```ts
// Parse `git diff --numstat -z`: <add>\t<del>\t<path>\0
const records = output.split("\0");
for (const record of records) {
  if (!record) continue;
  const firstTwoTabs = record.split("\t", 3);
  const [add, del, path] = firstTwoTabs;
  // path is preserved even if it contains tabs beyond the first two fields
}
```

Example pattern (complexity-safe trimming):
```ts
function trimTrailing(value: string, char: string): string {
  let end = value.length;
  while (end > 0 && value[end - 1] === char) end--;
  return value.slice(0, end);
}
```

Example pattern (stream + cap):
```ts
let received = 0;
for (;;) {
  const { done, value } = await reader.read();
  if (done) break;
  received += value.byteLength;
  if (received > maxBytes) { await reader.cancel(); throw new Error("too large"); }
  chunks.push(value);
}
```

This standard prevents correctness regressions from format edge cases and prevents performance/cost estimation from becoming unstable under large or adversarial inputs.