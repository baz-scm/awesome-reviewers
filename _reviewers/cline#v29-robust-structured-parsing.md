---
title: Robust Structured Parsing
description: 'When processing external/serialized formats (logs, git output, YAML,
  schemas, paths), implement parsing/normalization as structure-aware algorithms:


  - Use the format’s real separators (e.g., NUL-delimited records, only split on the
  first N tabs) instead of generic `split()`/whitespace assumptions.'
repository: cline/cline#v29
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70893
---

When processing external/serialized formats (logs, git output, YAML, schemas, paths), implement parsing/normalization as structure-aware algorithms:

- Use the format’s real separators (e.g., NUL-delimited records, only split on the first N tabs) instead of generic `split()`/whitespace assumptions.
- For multi-line or paired constructs, use stateful matching/pairing (start↔end, request id/client id) rather than filtering each line independently.
- Respect hierarchical structure and continuations: treat YAML entries as spans that include indented continuation lines (block scalars, nested maps/lists), and don’t let inline comments drift.
- Apply normalization recursively through nested containers (`items`, `anyOf`/`oneOf`/`allOf`), and avoid early “is this object-like?” gates that skip deeper fields.
- Handle platform/path representation explicitly (e.g., convert separators to a consistent form) and add tests for literal edge characters (like a backslash in POSIX filenames).

Example (delimiter-aware parsing of NUL-separated records):

```ts
// NUL-separated git output: never use '\n' splitting.
function parseNulRecords(output: string): string[] {
  return output.split("\0").filter(Boolean);
}

// Example: parse numstat where filenames may contain tabs.
function parseNumstat(output: string) {
  for (const record of output.split("\0")) {
    if (!record) continue;
    const firstTwoTabs = record.split("\t");
    // Ensure you only extract add/del from the first two fields,
    // and treat the remainder as the filename.
  }
}
```

Add regression tests that cover the tricky cases that break naive parsing: unfinished paired events, tab-containing filenames, YAML block scalar/inline scalar differences, nested schema branches, and cross-platform path separator behavior.