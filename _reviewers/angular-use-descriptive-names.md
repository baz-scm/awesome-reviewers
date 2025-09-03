---
title: Use descriptive names
description: Choose names that clearly and unambiguously describe their purpose rather
  than being overly generic or technical. Names should be self-documenting and immediately
  convey what the entity does or represents.
repository: angular/angular
label: Naming Conventions
language: TypeScript
comments_count: 7
repository_stars: 98611
---

Choose names that clearly and unambiguously describe their purpose rather than being overly generic or technical. Names should be self-documenting and immediately convey what the entity does or represents.

**Key principles:**
- Prefer descriptive names over generic ones: `MAX_ANIMATION_DURATION` instead of `ANIMATION_TIMEOUT`
- Choose contextual names for user-facing types: `IgnoreUnknownProps` instead of `DeepStripStringIndexUnknown`
- Method names should clearly indicate behavior: `trackClasses` instead of `addClasses` (which implies DOM manipulation)
- Follow the philosophy: "choose the shortest name that unambiguously and meaningfully describes a thing"

**Examples:**
```typescript
// ❌ Generic or misleading names
const ANIMATION_TIMEOUT = 4000;
export type DeepStripStringIndexUnknown<T> = ...;
addClasses(details: AnimationDetails, classes: string[]): void;

// ✅ Descriptive and clear names  
const MAX_ANIMATION_DURATION = 4000;
export type IgnoreUnknownProps<T> = ...;
trackClasses(details: AnimationDetails, classes: string[]): void;
```

Avoid names that could confuse developers about the actual functionality. When in doubt, err on the side of being more descriptive rather than more concise.