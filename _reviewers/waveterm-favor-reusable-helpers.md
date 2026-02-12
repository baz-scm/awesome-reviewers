---
title: Favor reusable helpers
description: Centralize repeated UI logic and prefer modern, consistent JS style.
  When you see duplicated logic, ad-hoc class strings, local copies of global state,
  or repeated boolean checks, extract them into small, well-named helpers (or model/computed
  methods) and apply consistent ES/React idioms.
repository: wavetermdev/waveterm
label: Code Style
language: TSX
comments_count: 8
repository_stars: 17328
---

Centralize repeated UI logic and prefer modern, consistent JS style. When you see duplicated logic, ad-hoc class strings, local copies of global state, or repeated boolean checks, extract them into small, well-named helpers (or model/computed methods) and apply consistent ES/React idioms.

Why: centralization improves readability, reduces bugs from divergence, and makes code easier to test and reuse. Using modern patterns (const, for-of, classname helpers) keeps code concise and consistent.

Actionable checklist:
- Use a class-name helper (cn/clsx) to compose classes and avoid manual string concatenation:
  // from discussion
  // bad: className={`tab-bar-wrapper${autoHideTabsBar ? '-auto-hide' : ''}`}
  // better:
  className={cn('tab-bar-wrapper', { 'tab-bar-wrapper-auto-hide': autoHideTabsBar })}
  // and avoid unnecessary fallbacks:
  className={cn('wave-dropdown', className)}

- Extract repeated UI/focus/keybinding logic into model methods or computed helpers so callers just ask the model for intent:
  // suggested pattern
  // inputModel.ts
  isAuxViewFocused(auxView: InputAuxViewType) {
    return GlobalModel.inputModel.hasFocus() ||
           (GlobalModel.getActiveScreen().getFocusType() === 'input' &&
            GlobalModel.activeMainView.get() === 'session' &&
            GlobalModel.inputModel.getActiveAuxView() === auxView);
  }

  // consumer
  const isHistoryFocused = GlobalModel.inputModel.isAuxViewFocused(InputAuxView_History);

- Prefer modern, immutable declarations and iteration:
  - Use const for variables that are not reassigned (e.g., `const tab = ...`, `const elem = this.iconRef.current`).
  - Prefer `for (const item of array)` or array helpers over C-style loops.

- Don’t merge arrays when handling logic differs. Either iterate separately or normalize behavior first; merging is fine only when the processing is identical.

- Keep local component state minimal. If global/shared state already tracks a value (focus, mode, etc.), reuse it instead of duplicating.

Examples from discussions:
- Class composition: className={cn('wave-dropdown', className)} (no `|| ''`)
- Focus logic: move to inputModel.isAuxViewFocused(auxView)
- Iteration/style: use `for (const tab of this.options)` and `const` instead of `let` and C-style loops

Apply this rule in reviews: if you see repeated logic, ad-hoc string building, or duplicated state, request extraction to a helper or model and enforce `const`/`for-of`/cn usage for consistency.