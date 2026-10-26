---
title: Maintain IR Invariants
description: 'When implementing compiler optimizations/analyses (especially transformations
  over HIR/CFG), treat local structure and dataflow assumptions as *explicit invariants*:
  encode them as checks/guards and add assertions rather than relying on “it should
  be true” properties.'
repository: facebook/react#b2
label: Algorithms
language: TypeScript
comments_count: 3
repository_stars: 251882
---

When implementing compiler optimizations/analyses (especially transformations over HIR/CFG), treat local structure and dataflow assumptions as *explicit invariants*: encode them as checks/guards and add assertions rather than relying on “it should be true” properties.

Apply this rule:
- **State the assumed invariant** (e.g., “target block has the expected control-flow shape”, “temporaries are in-scope”, “no nested value-block fallthrough hazards”).
- **Add a minimal targeted guard** before rewriting (e.g., verify the target ends with the expected `goto`/fallthrough; verify binding kind and scoping prerequisites).
- **Use fixpoint/multi-pass analysis** when derivations depend on phi nodes / inter-block propagation; stop only when the analysis snapshot stabilizes.
- **Prefer failing fast**: if an invariant isn’t provable cheaply, either (a) skip the transform or (b) add an assert guarded by debug/diagnostic tooling.

Example (structural guard idea):
```ts
// Only constant-fold ternary test when control-flow matches expected shape.
if (branchBlock.terminal.kind !== 'branch') return;
const target = testValue.value ? branchBlock.terminal.consequent
                                : branchBlock.terminal.alternate;
const targetBlock = fn.body.blocks.get(target);
if (!targetBlock || !endsWithGotoToFallthrough(targetBlock, terminal)) return;
// Safe to rewrite to goto.
block.terminal = makeGoto(target, terminal.id, terminal.loc);
```

This prevents incorrect rewrites and avoids subtle miscompilations when IR shape, scoping, or propagated analysis facts differ from what the algorithm assumed.