---
title: Complexity-safe Parsing
description: When writing parsers, estimators, or state logic driven by external/variable
  inputs, ensure (a) correct delimiter/format semantics, and (b) complexity- and scaling-safety.
repository: cline/cline#x
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70861
---

When writing parsers, estimators, or state logic driven by external/variable inputs, ensure (a) correct delimiter/format semantics, and (b) complexity- and scaling-safety.

**Do**
- **Split only by the delimiters that define fields.** If a filename/payload can contain the delimiter, split on the first *N* occurrences and keep the rest intact.
  ```ts
  // parse `git diff --numstat -z`: add<TAB>del<TAB>path-with-tabs...
  const [add, del, inlinePath] = record.split("\t", 3);
  const path = inlinePath ?? "";
  ```
- **Add tests for delimiter/content edge cases** (e.g., tab-containing filenames; YAML block scalars; POSIX-vs-OS path separators).
- **Avoid regexes with potential pathological backtracking** on long/untrusted input; prefer bounded loops.
- **Cap work and sizes** while parsing/downloading/expanding archives, and validate path normalization to prevent escapes.
- **Ensure estimators scale with intended factors**, not raw payload size (e.g., image token estimates should depend on image count, not base64 byte length).

**Don’t**
- Use naive `split(delimiter)` for structured outputs when fields can legally contain that delimiter.
- Let complexity grow with payload length accidentally (e.g., regex backtracking, per-byte estimation for content where the true cost is per-item/flat).

This standard keeps algorithms predictable, prevents worst-case behavior, and preserves correctness across real-world input variations.