---
title: Remove commented code
description: 'Commented-out code should be removed from the codebase rather than left
  as comments. Keeping commented code:


  1. Clutters the codebase and reduces readability'
repository: elie222/inbox-zero
label: Code Style
language: TSX
comments_count: 9
repository_stars: 8267
---

Commented-out code should be removed from the codebase rather than left as comments. Keeping commented code:

1. Clutters the codebase and reduces readability
2. Creates confusion about which code is active and which isn't
3. Often becomes outdated or incompatible as surrounding code evolves
4. Indicates incomplete work or indecision

Modern version control systems like Git provide better ways to preserve code history. If you need to reference previous implementations, use commit history instead of keeping commented code in the active codebase.

Instead of:
```typescript
function onLabelSubmit: SubmitHandler<LabelInputs> = (data) => {
  // onSubmit(data.labelInstructions || "");
  onNext();
};
```

Do:
```typescript
function onLabelSubmit: SubmitHandler<LabelInputs> = (data) => {
  onNext();
};
```

For debug statements like console.log(), ensure they're removed before merging to production:
```diff
-console.log("API Response:", data); // Debug log
-console.log("All rules:", data.allRules); // Debug log
```

If you need to temporarily disable a feature, use feature flags or configuration rather than commenting out the code. For TODOs or explanatory notes, focus on explaining why rather than preserving unused code.