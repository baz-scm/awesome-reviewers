---
title: Fixpoint Dataflow Joins
description: 'When adding compiler analyses or optimizations (constant propagation,
  derivation tracking, mutability aliasing), treat computed properties as dataflow
  facts over an IR lattice:'
repository: facebook/react#b10
label: Algorithms
language: TypeScript
comments_count: 4
repository_stars: 251894
---

When adding compiler analyses or optimizations (constant propagation, derivation tracking, mutability aliasing), treat computed properties as dataflow facts over an IR lattice:

- **Use a join/merge function for facts** and apply it whenever new evidence is found.
  - Do **not** overwrite an existing cache entry for the same place/identifier unless the join is “replace.”
- **Run a fixpoint loop** (multi-pass) when new facts can unlock further facts.
- **Validate rewrite/validation preconditions** based on the IR structure before applying transformations (e.g., ensure nested value-block assumptions hold).

Example pattern (merge + fixpoint):
```ts
// Pseudocode for lattice facts
function join(a: Fact, b: Fact): Fact {
  if (a === 'ignored') return b;
  if (b === 'ignored') return a;
  if (a === b) return a;
  return 'fromPropsAndState';
}

let changed = false;
do {
  changed = false;
  for (const block of fn.body.blocks.values()) {
    for (const instr of block.instructions) {
      const newFact = computeFactFromOperands(instr);
      for (const lvalue of eachInstructionLValue(instr)) {
        const oldFact = cache.get(lvalue);
        const merged = oldFact == null ? newFact : join(oldFact, newFact);
        if (oldFact !== merged) {
          cache.set(lvalue, merged);
          changed = true;
        }
      }
    }
  }
} while (changed);
```

Checklist for PRs
- Did you define/extend the lattice (including any new kinds/states) and update the **join/merge** logic accordingly?
- When the same key is encountered multiple times, do you **join** contributions or accidentally overwrite them?
- If correctness depends on iterative discovery, do you run to a **fixpoint** (or prove single-pass is sufficient)?
- Before performing an IR rewrite or making a structural assumption, did you add an **invariant check** (e.g., no nested value blocks, correct scope/context reference set)?