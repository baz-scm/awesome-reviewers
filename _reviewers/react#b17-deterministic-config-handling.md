---
title: Deterministic Config Handling
description: 'Configuration-like controls (compiler pragmas, feature flags, and UI/config
  state) must behave deterministically: apply directives in the correct place, avoid
  relying on implicit defaults without intent, and ensure reset flows explicitly clear
  any configuration-like state.'
repository: facebook/react#b17
label: Configurations
language: TSX
comments_count: 3
repository_stars: 251891
---

Configuration-like controls (compiler pragmas, feature flags, and UI/config state) must behave deterministically: apply directives in the correct place, avoid relying on implicit defaults without intent, and ensure reset flows explicitly clear any configuration-like state.

Practical rules:
- Compiler/feature pragmas: place all `@...` directives at the very top of the file so tooling can reliably detect them.
- Be explicit about defaults: if a validation/feature is enabled by default, placement mistakes can surface as confusing errors—fix the directive location first.
- Reset semantics: when the user triggers a “force reset,” don’t preserve configuration-like toggles unless that persistence is intentional.
- Build/import config: keep import conventions consistent across workspaces; introduce aliases only via an intentional, standardized change.

Example (top-of-file pragmas + force reset clearing flags):
```ts
// @enableInferEventHandlers
// @validateRefAccessDuringRender

// ...rest of file
```
```ts
dispatchStore({
  type: 'setStore',
  payload: { store: defaultStore }, // ensure defaultStore doesn’t carry over showInternals
});
```