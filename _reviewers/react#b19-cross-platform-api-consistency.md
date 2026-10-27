---
title: Cross-platform API consistency
description: 'When an API has multiple platform- or bundler-specific implementations
  (browser vs. server, different host environments, different bundlers), verify its
  contract against the actual external specification or compatibility table rather
  than assuming behavior based on convention or copy-pasted code. Two concrete practices
  follow from this:'
repository: facebook/react#b19
label: API
language: JavaScript
comments_count: 4
repository_stars: 251893
---

When an API has multiple platform- or bundler-specific implementations (browser vs. server, different host environments, different bundlers), verify its contract against the actual external specification or compatibility table rather than assuming behavior based on convention or copy-pasted code. Two concrete practices follow from this:

1. Match the real spec/compat data, not assumptions. For example, the DOM Living Standard defines an event listener's identity as the `(type, callback, capture)` tuple — `passive` and `once` are not part of the key — so `normalizeListenerOptions` must only encode `capture` in the identifier, otherwise `addEventListener`/`removeEventListener` semantics silently diverge from the spec. Similarly, before gating a feature behind "is this API supported," check the authoritative compatibility table (e.g. MDN's `ElementsPanel.createSidebarPane` entry) instead of reusing a check copied from an unrelated feature.

2. Keep multi-implementation entrypoints and parameters consistent. If prior art ships separate browser/server entrypoints to avoid bundling unnecessary code (e.g. `*.browser.js` / `*.node.js`), new APIs in the same family should follow that convention rather than introducing a single shared entrypoint with runtime branching, unless there's a documented reason to diverge. Likewise, when a config function accepts optional parameters that some implementations don't use (e.g. `integrity`, `fetchPriority` in `preinitModuleForSSR`), decide whether they should be required so every implementation makes an explicit choice, instead of allowing silent, inconsistent defaults across platforms.

In short: before writing or reviewing code that targets multiple runtime/platform targets, confirm the behavior against the real spec or compatibility reference, and make cross-implementation contracts explicit and uniform.