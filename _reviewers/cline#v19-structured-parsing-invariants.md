---
title: Structured Parsing Invariants
description: When consuming structured/serialized data (CLI output, archives, YAML,
  custom protocols), implement parsing as a deterministic algorithm that respects
  the source format’s boundaries and preserves semantic context. Enforce correctness
  with invariants and edge-case tests.
repository: cline/cline#v19
label: Algorithms
language: TypeScript
comments_count: 9
repository_stars: 70885
---

When consuming structured/serialized data (CLI output, archives, YAML, custom protocols), implement parsing as a deterministic algorithm that respects the source format’s boundaries and preserves semantic context. Enforce correctness with invariants and edge-case tests.

Practical rules:
1) Respect the transport encoding/delimiters
- Prefer protocol-provided separators (e.g., `-z` null-delimited records). Avoid `split("\n")` or generic splitting when filenames/fields can contain delimiter characters.
- If a field separator is ambiguous, split only the first N components, then treat the remainder as the field payload.

2) Preserve multi-record semantics
- Some records (e.g., git rename/copy) require consuming/associating the next record(s) to retain the “old path” vs “new path”. Don’t collapse these into a single record without tracking the additional path.

3) Encode cost/logic as invariants
- Estimators and similar algorithms should follow the real model: e.g., image cost should be driven by image count, not base64 payload length. Add tests that assert invariants like “payload length changes do not change the estimate”.

4) Defensively normalize and validate untrusted inputs
- Normalize paths to a safe canonical form; reject or skip entries that escape the root.
- Cap recursive/expansion behavior (e.g., link expansion depth) to avoid pathological processing.

5) Add targeted edge-case tests
- Examples to cover:
  - Tab/newline/backslash inside filenames.
  - Separator characters inside text fields.
  - Rename/copy paths that must flow through downstream actions.
  - Adversarial archive paths.
  - Payload-size changes that must not affect estimates.

Example: parsing `git diff --numstat -z` without corrupting tab-containing filenames
```ts
export function parseNumstat(output: string) {
  const counts = new Map<string, { additions: number | null; deletions: number | null }>();
  for (const record of output.split("\0")) {
    if (!record) continue;
    // Split only the first two tabs; filename may contain tabs.
    const [add, del, ...rest] = record.split("\t");
    const inlinePath = rest.join("\t");
    counts.set(inlinePath, {
      additions: add === "-" ? null : Number(add),
      deletions: del === "-" ? null : Number(del),
    });
  }
  return counts;
}
```

Apply this standard any time you’re writing parsing/estimation/transform code: first make the parsing boundary unambiguous, then preserve semantic context, then guard with invariants + edge-case tests.