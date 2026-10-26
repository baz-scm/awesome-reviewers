---
title: Document Config Overrides
description: When configuration or feature flags change behavior across build/channel/environment
  (including rollout loaders) or across packaging/toolchains, ensure the code, docs,
  and packaging rules align with the *effective* behavior.
repository: cline/cline#v28
label: Configurations
language: Other
comments_count: 2
repository_stars: 70893
---

When configuration or feature flags change behavior across build/channel/environment (including rollout loaders) or across packaging/toolchains, ensure the code, docs, and packaging rules align with the *effective* behavior.

Apply this in two parts:
1) **Config/feature-flag documentation must be build-aware**
- State which setting overrides which behavior/build.
- Include how to select explicitly (and whether a reload is required).
- Don’t introduce “silent wrongness” for specific channels (e.g., Nightly/legacy identities); ensure the documented keys map correctly.

Example (docs for a rollout override):
```ts
// VS Code setting used to pick a specific extension bundle
// cline.rollout.bundleOverride: "next" | "legacy" | "auto"
// Setting to "next" or "legacy" requires reloading the window.
```

2) **Packaging configuration should be validated against the actual tool defaults**
- If you change ignore files (like `.vscodeignore`), verify what ends up in the packaged artifact using the packaging tool’s listing/behavior.
- Remove redundant ignore entries when the tool already excludes the same patterns.

Practical rule of thumb: after any change to config/rollout behavior or packaging ignore rules, run a quick “effective behavior” check (e.g., packaging listing) and update docs only after you confirm the real mapping.