---
title: Test Parsing Invariants
description: For algorithmic code that depends on dynamic state or structured text
  output, require (1) explicit invariants, (2) precise parsing/splitting rules, and
  (3) tests that cover adversarial edge cases—plus fuzz/sequence testing for state
  machines.
repository: cline/cline#v24
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70891
---

For algorithmic code that depends on dynamic state or structured text output, require (1) explicit invariants, (2) precise parsing/splitting rules, and (3) tests that cover adversarial edge cases—plus fuzz/sequence testing for state machines.

Apply this standard by:
- State machines / pagination (e.g., cursor + visible window): document invariants like “skipping a row before the cursor must not reorder unrelated visible rows” and “only the skipped row disappears.” Verify with:
  - A deterministic sequence test (known verb/action order)
  - A fuzz/property test over random verb sequences asserting invariants (“skip hides only its row”, “undo restores it”).
- Parsers of external command output (git, YAML, logs): avoid “split on whitespace”/broad regexes.
  - Use delimiter-aware splitting (e.g., for `--numstat -z`, split on the first two tabs; keep the remainder as the filename).
  - Preserve multi-record semantics (e.g., rename/copy original paths) rather than discarding follow-up records.
  - Correctly handle multi-line/nested structures by measuring top-level entry span (inline scalar vs block scalar).
- Algorithmic estimation rules: encode the real intended model (e.g., per-image token cost) and lock it with tests that reject naive approximations.

Example (delimiter-safe parsing pattern):
```ts
// For outputs like: <additions>\t<deletions>\t<path...-with-tabs>
function parseNumstatRecord(record: string): { add: number|null; del: number|null; path: string } {
  const [addRaw, delRaw, ...rest] = record.split('\t');
  if (rest.length === 0) throw new Error('bad record');
  const path = rest.join('\t');
  const add = addRaw === '-' ? null : Number(addRaw);
  const del = delRaw === '-' ? null : Number(delRaw);
  return { add, del, path };
}
```

Checklist for PRs in this area:
- What are the invariants (state) or the grammar (parsing)?
- Do you have unit tests that hit the tricky edge cases (delimiter/tab/rename/or inline vs block)?
- For state transitions: do you have at least one sequence test and a randomized/fuzz check that asserts the invariants hold across many action orders?
- For “estimation” algorithms: do tests ensure the implementation matches the intended cost model rather than naive approximations? 