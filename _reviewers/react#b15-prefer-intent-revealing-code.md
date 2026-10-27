---
title: Prefer intent-revealing code
description: 'When improving readability, avoid patterns that obscure intent: (1)
  don’t build placeholder objects and patch them later, and (2) don’t mix redundant
  type checks into logic when dataflow/analysis already determines behavior.'
repository: facebook/react#b15
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When improving readability, avoid patterns that obscure intent: (1) don’t build placeholder objects and patch them later, and (2) don’t mix redundant type checks into logic when dataflow/analysis already determines behavior.

Apply these rules:
- Prefer self-contained exported structures: define the final config directly (e.g., via getters) instead of assigning `{}` and mutating/replacing later.
- Keep logic single-source-of-truth: if an analysis is already driven by dataflow/state, remove redundant typing/guard checks that add branching without improving correctness.

Example (self-contained config via getter):
```ts
const plugin = /* ... */;

const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'() {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
};
```

Example (logic cleanup):
```ts
// Instead of mixing typing with dataflow,
// rely on the dataflow signal already available in context.
maybeRecordSetState(instr, context.setStateLoads, effectSetStateUsages);

for (const operand of eachInstructionOperand(instr)) {
  // Remove redundant isSetStateType checks if the dataflow/cache
  // conditions already capture which operands matter.
}
```