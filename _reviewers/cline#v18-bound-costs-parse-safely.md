---
title: Bound Costs, Parse Safely
description: 'When implementing algorithmic logic for external data (git output, paths,
  token/cost estimation), avoid naive assumptions that make correctness or complexity
  hinge on arbitrary payload details. Instead: (1) make parsing delimiter-safe and
  format-aware; (2) make cost/size estimators complexity-bounded and validate scaling
  invariants.'
repository: cline/cline#v18
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70884
---

When implementing algorithmic logic for external data (git output, paths, token/cost estimation), avoid naive assumptions that make correctness or complexity hinge on arbitrary payload details. Instead: (1) make parsing delimiter-safe and format-aware; (2) make cost/size estimators complexity-bounded and validate scaling invariants.

Apply these rules:
- Delimiter-safe parsing: split only on the delimiter positions the format specifies (e.g., “first two tabs, rest is filename”); use record framing correctly (e.g., NUL-delimited records for porcelain output); handle multi-record constructs (rename/copy extra path records) explicitly.
- Complexity-bounded estimation: never compute token/cost directly from raw base64/string length when the real pricing scales by count (e.g., per-image). Ensure the estimate’s sensitivity matches the true complexity driver (e.g., image count), and add tests that assert monotonic/bounded properties.
- Output normalization: normalize separators/representations consistently (e.g., POSIX relative paths) without breaking legitimate characters (e.g., literal backslashes in filenames).
- Prove external assumptions with targeted tests: if you rely on disjointness/merge behavior (e.g., combining trees), encode that reasoning as a unit/integration test with realistic edge cases.

Example (delimiter-safe split for numstat-like records):
```ts
function parseNumstat(output: string) {
  const map = new Map<string, { additions: number | null; deletions: number | null }>();
  for (const rec of output.split("\0")) {
    if (!rec) continue;
    // Split only the first two tab-separated fields; keep remaining tabs in filename.
    const i1 = rec.indexOf("\t");
    const i2 = rec.indexOf("\t", i1 + 1);
    if (i1 < 0 || i2 < 0) continue;
    const add = rec.slice(0, i1);
    const del = rec.slice(i1 + 1, i2);
    const file = rec.slice(i2 + 1);
    map.set(file, {
      additions: add === "-" ? null : Number(add),
      deletions: del === "-" ? null : Number(del),
    });
  }
  return map;
}
```

Minimum checklist for PRs in this area:
- Parsing changes include edge-case tests (tabs in filenames, embedded delimiter characters, multi-record handling).
- Estimation changes include scaling tests (changing payload length doesn’t move the estimate; changing item count does).
- Path/normalization changes include filenames that would break naive separator handling.