---
title: Extract Shared Helpers
description: When review finds repeated or “very similar” logic patterns, don’t leave
  copy-paste growth—refactor into a shared helper, and follow local file conventions
  so future edits don’t diverge.
repository: warpdotdev/warp
label: Code Style
language: Rust
comments_count: 7
repository_stars: 56893
---

When review finds repeated or “very similar” logic patterns, don’t leave copy-paste growth—refactor into a shared helper, and follow local file conventions so future edits don’t diverge.

Apply these rules:
1) DRY similar control-flow blocks
- If two (or more) match arms / branches perform the same orchestration/config/picker-sync steps, extract a helper and call it from each site.
- Keep helper boundaries aligned with ownership (pass only the state/handles needed to avoid accidental drift).

Example pattern (from the style of the suggested refactors):
```rust
// 1 helper used by multiple match arms
fn apply_harness_change<A, V>(
    state: &mut OrchestrationEditState,
    memory: &mut PerHarnessModelMemory,
    handles: &OrchestrationPickerHandles<A>,
    new_harness_type: &str,
    fallback_base_model_id: impl FnOnce(&mut ViewContext<V>) -> Option<String>,
    ctx: &mut ViewContext<V>,
) {
    // ... shared harness-switch logic ...
    // ... update picker/model selections ...
    ctx.notify();
}

// called from different arms
apply_harness_change(
    &mut self.state.orch,
    &mut self.saved_model_per_harness,
    &self.handles.pickers,
    harness_type,
    |ctx| block_model.base_model(ctx).map(|id| id.to_string()),
    ctx,
);
```

2) Avoid duplication for readability
a) Don’t call the same query method in both sides of an if/else—compute once before branching when it’s the same value.
b) If match arms differ only by a small behavior, consider grouping them (or a shared function) rather than duplicating the surrounding scaffolding.

3) Keep file conventions consistent
- Imports: prefer explicit imports at the top of the file over repeated inline qualification.
- Tests: follow the codebase convention (e.g., place test modules/`#[cfg(test)]` blocks at the bottom of the file).

These changes should be “small refactors that prevent future drift”: they improve consistency without altering behavior.