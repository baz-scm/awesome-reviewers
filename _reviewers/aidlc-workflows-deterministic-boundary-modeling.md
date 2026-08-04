---
title: Deterministic Boundary Modeling
description: 'When an algorithm’s correctness depends on what “exactly” was bound/parsed/scanned,
  never rely on lossy representations (timestamps, ambiguous regex slices, quoted/escaped
  strings, overlapping recursion). Instead:'
repository: awslabs/aidlc-workflows
label: Algorithms
language: TypeScript
comments_count: 8
repository_stars: 3849
---

When an algorithm’s correctness depends on what “exactly” was bound/parsed/scanned, never rely on lossy representations (timestamps, ambiguous regex slices, quoted/escaped strings, overlapping recursion). Instead:

1) Bind results to explicit boundaries/identifiers
- Use an exact attempt/run-floor or stage-attempt key, not second-precision timestamps.
- For audit/event reconciliation, choose the correct anchor event boundary (exclude synthetic rows that shift the window).
- For state review bindings, use a content fingerprint that matches the inspected source boundary.

2) Parse input with a non-ambiguous grammar
- Prefer unambiguous encodings/delimiters (e.g., NUL-delimited `git ... -z`) over default escaping.
- Model full entry structure in regexes/parsers: include continuation lines (e.g., `conditional_on`) and parse per-entry blocks so later fields aren’t dropped or inverted.
- If idempotency matters, use self-delimiting markers (sentinels) and/or content hashes to avoid false positives and ordering ambiguity.

3) Ensure aggregation/counting domains don’t overlap
- Define recursion depth and sweep regions so the same files can’t be counted twice (e.g., exclude `SCAN_SOURCE_DIRS` from the depth-1 sweep if you’ll recurse them at depth 6).

Example (NUL-delimited parsing to avoid quoting bugs):
```ts
const out = spawnSync('git', ['-C', repo, 'ls-files', '-s', '-z'], { encoding: 'utf-8' });
if (out.status !== 0) return null;
const entries = out.stdout.split('\0');
for (const e of entries) {
  if (!e) continue;
  // e is an unquoted/unescaped NUL-separated record; parse fields safely
}
```

Apply this standard anywhere you have: receipt validity, audit-window checks, structural YAML/markdown splicing, or directory scanning/counting—especially when failures would be silent (incorrect acceptance, dropped entries, corrupted semantics, or wrong aggregate totals).