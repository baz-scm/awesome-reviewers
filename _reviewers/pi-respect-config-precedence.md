---
title: Respect config precedence
description: When configuration can vary by user/environment, resolve it deterministically
  (following documented precedence), keep it configurable instead of hardcoded, and
  apply it dynamically if it may change at runtime.
repository: earendil-works/pi
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 79783
---

When configuration can vary by user/environment, resolve it deterministically (following documented precedence), keep it configurable instead of hardcoded, and apply it dynamically if it may change at runtime.

Practical rules:
- **Env var / credential resolution:** follow the precedence you intend to support (documented behavior beats “guessing”). If you change precedence, call out multi-provider edge cases.
- **Environment-specific constants:** don’t hardcode regions/endpoints when they can differ across deployments—make them configurable (or at least driven by model/endpoint metadata that can evolve).
- **User controls/feature flags:** avoid hardcoded keybindings and similar UX toggles; support config files and sensible defaults.
- **Config schema:** keep settings shapes simple and stable (avoid unnecessary nesting).
- **Runtime settings:** if a setting is user-editable mid-session (e.g., via `/settings`), don’t decide behavior once during session creation—re-evaluate from the session settings manager when converting requests.

Example (dynamic `blockImages` handling):
```ts
// Bad: captures blockImages once at session creation
// const convertToLlmWithBlockImages = blockImages ? filteredConvertToLlm : convertToLlm;

// Good: decide per-use from session manager
function makeConvertToLlm(sessionManager: { getBlockImages(): boolean }) {
  return async function convertToLlm(...args: unknown[]) {
    const shouldBlock = sessionManager.getBlockImages();
    if (shouldBlock) return convertToLlmFilteredImages(...args);
    return convertToLlmUnfilteredImages(...args);
  };
}
```

Following this standard prevents stale configuration behavior, reduces deployment brittleness, and makes feature flags and user settings reliably predictable.