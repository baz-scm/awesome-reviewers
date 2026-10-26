---
title: Bounded, Linear Parsing
description: Write parsing and transformation code with (1) linear-time string handling,
  (2) delimiter-accurate boundaries that preserve data, and (3) explicit safety bounds
  for stateful or recursive flows.
repository: cline/cline#v26
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70893
---

Write parsing and transformation code with (1) linear-time string handling, (2) delimiter-accurate boundaries that preserve data, and (3) explicit safety bounds for stateful or recursive flows.

Apply it like this:
- **Avoid pathological regex**: prefer index/loop scans over regexes that can backtrack badly on long input.
- **Parse using the source’s real record format**: NUL-delimited records must split on `\0`, tab-based formats must only split on the specified tab fields and keep the remainder as the filename.
- **Handle value spans precisely**: distinguish inline scalars vs block scalars so comments/continuations stay attached to the correct YAML entry.
- **Guard state/recursion with invariants + caps**: for paginated/stateful UIs and for linked-directory expansion/traversal, define what must remain stable (e.g., which rows stay visible) and cap expansion depth/size to prevent runaway behavior.
- **Test tricky boundaries**: add pinned sequence tests (and fuzz sequences when it’s a state machine) plus regression tests for corner-case filenames/inputs (tabs, backslashes, long strings).

Example (bounded, linear string scan instead of potentially bad regex):
```ts
// Linear-time trim of trailing delimiter characters.
function trimTrailing(value: string, char: string): string {
  let end = value.length;
  while (end > 0 && value[end - 1] === char) end--;
  return value.slice(0, end);
}
```

Example (tab-delimiter: split only the required fields, keep the rest as filename):
```ts
// Suppose a record is: <add>\t<del>\t<path-with-tabs-possibly>
const [addStr, delStr, ...rest] = record.split("\t");
const path = rest.join("\t");
```

These practices keep algorithmic behavior predictable (linear where intended), prevent worst-case slowdowns, and maintain correctness across real-world inputs and edge cases.