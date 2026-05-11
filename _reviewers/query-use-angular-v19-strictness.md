---
title: Use Angular v19+ Strictness
description: When targeting Angular v19+ (or modernizing to it), align your package
  peer/dependency baselines and update tsconfig to the corresponding strict compiler
  settings—then apply the same policy across all Angular examples.
repository: tanstack/query
label: Angular
language: Json
comments_count: 5
repository_stars: 49380
---

When targeting Angular v19+ (or modernizing to it), align your package peer/dependency baselines and update tsconfig to the corresponding strict compiler settings—then apply the same policy across all Angular examples.

Apply:
- Compatibility baseline: prefer supporting the newer major where feasible (e.g., Angular 20+), and keep peerDependencies/dependency versions consistent across examples.
- tsconfig strictness (Angular v19+): ensure the Angular compiler strict options are enabled, including:
  - `strictTemplates: true`
  - `strictStandalone: true` (new in v19)
- Typecheck/build consistency: keep strict TS mode and recommended compile options used with Angular v19 (e.g., `skipLibCheck: true` and `isolatedModules: true`).

Example tsconfig (pattern):
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "target": "ES2022",
    "module": "ES2022",
    "lib": ["ES2022", "dom"]
  },
  "angularCompilerOptions": {
    "strictInjectionParameters": true,
    "strictInputAccessModifiers": true,
    "strictTemplates": true,
    "strictStandalone": true
  }
}
```

Also update example `package.json` dependencies together (Angular major/minor, `zone.js`, and TypeScript) so the toolchain is coherent.