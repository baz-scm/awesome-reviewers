---
title: I18n Translation Policy
description: 'Treat every newly added user-facing string key as a documentation/UX
  contract for all supported locales.


  When you add `t()` keys:

  1) Classify the keys against the project’s translation policy (e.g., `MUST_TRANSLATE_KEYS`).'
repository: QwenLM/qwen-code
label: Documentation
language: JavaScript
comments_count: 2
repository_stars: 26407
---

Treat every newly added user-facing string key as a documentation/UX contract for all supported locales.

When you add `t()` keys:
1) Classify the keys against the project’s translation policy (e.g., `MUST_TRANSLATE_KEYS`).
2) If the key is required: add translations in all required locale files in the same PR.
3) If the key is intentionally allowed to fall back (not in `MUST_TRANSLATE_KEYS`): don’t rely on “CI is green” silently—add an explicit maintainer note and create/track a follow-up “translation pass” issue (prioritize locales, define a quality gate, and link it in the PR).
4) Double-check the locales that are expected to be complete (e.g., full parity locales). Untranslated strings there should be fixed immediately.

This prevents users from seeing raw English fallback text (even though it won’t crash), while still supporting deliberate rollout decisions.

Example (process pattern):
```ts
// 1) Add new keys to the i18n source
export default {
  'Set Default Model': 'Set Default Model',
  // ...
}

// 2) In the PR description / follow-up tracking, state which case applies:
// - Required locales: <list> (translations added)
// - Optional fallback: <list> (link a follow-up translation pass)
// - Rationale: key intentionally excluded from MUST_TRANSLATE_KEYS
```

Rule of thumb: if users in a locale will see English instead of the intended language, the PR must either include the translations or explicitly schedule a translation pass with owners and scope.