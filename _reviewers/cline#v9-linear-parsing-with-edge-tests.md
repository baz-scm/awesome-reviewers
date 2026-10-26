---
title: Linear Parsing With Edge-Tests
description: 'When implementing parsing/transformations (CLI output parsing, filenames/paths,
  serialized payload counting), require:


  1) **Delimiter-safe parsing**: split only on the intended field separators, and
  treat the remainder as data when delimiters can appear inside fields.'
repository: cline/cline#v9
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 70868
---

When implementing parsing/transformations (CLI output parsing, filenames/paths, serialized payload counting), require:

1) **Delimiter-safe parsing**: split only on the intended field separators, and treat the remainder as data when delimiters can appear inside fields.
2) **Bounded algorithmic complexity**: avoid patterns that can degrade badly (e.g., catastrophic regex backtracking); prefer explicit linear scans/loop-based parsing.
3) **Platform-correct normalization**: handle path separators carefully so you don’t corrupt filenames that legitimately contain characters like backslashes.
4) **Cost models must be bounded and tested**: don’t let estimates scale with raw payload size when the real cost depends on a smaller factor (e.g., count of images vs base64 length).

Example (delimiter-safe `split` for tab-containing filenames):
```ts
// For numstat -z style records: first two tab-separated fields are counts,
// remainder is the filename (which may contain tabs).
const [addStr, delStr, ...rest] = record.split('\t');
const path = rest.join('\t');
```

Example (avoid regex backtracking with linear trim):
```ts
function trimTrailing(value: string, char: string): string {
  let end = value.length;
  while (end > 0 && value[end - 1] === char) end--;
  return value.slice(0, end);
}
```

Example (path separator semantics):
- Convert to POSIX separators only when producing relative paths for POSIX consumers, and don’t split on a literal backslash unless that’s truly the separator being handled.

Apply this standard by adding focused tests for:
- delimiters-in-data (e.g., tab-containing filenames),
- long inputs that would trigger regex worst-cases,
- filenames containing literal separator characters,
- and bounded scaling properties (e.g., estimates scale with image count, not base64 size).