---
title: Test critical branches
description: When code adds/changes behavior (UI logic, URL rewriting, state-merge
  rules, keyboard/pointer guards, or error-recovery flows), ensure tests cover (1)
  the behavior itself (not just indirectly), (2) the negative guard cases that prevent
  regressions, and (3) the full interaction path users trigger.
repository: QwenLM/qwen-code
label: Testing
language: TSX
comments_count: 20
repository_stars: 26407
---

When code adds/changes behavior (UI logic, URL rewriting, state-merge rules, keyboard/pointer guards, or error-recovery flows), ensure tests cover (1) the behavior itself (not just indirectly), (2) the negative guard cases that prevent regressions, and (3) the full interaction path users trigger.

Practical rules:
1) **Lock shipped behavior with direct tests**
- If a function mirrors an already-tested guard, **add the same tests** for the new function.
- If a UI behavior changes (e.g., right-panel close behavior), add a component/App test that reproduces the open→act→close→reopen flow and asserts the invariant.
- If wiring changes (e.g., base-path pathname rewriting), test the resulting effect at the boundary where it’s used.

2) **Add negative tests for safety guards**
- For pointer/keyboard/mode gates, test both allowed and disallowed inputs (e.g., non-primary button, wrong `pointerId`, `event.detail` guard, tap-vs-hold mode).

3) **For UI, test “click/trigger → menu/content/action”**
- Don’t stop at asserting a trigger exists; simulate the user interaction that opens the menu and verify the menu items’ labels/content and that the intended callback fires.

4) **Keep test selectors unique and stable**
- Avoid duplicating `data-testid` values within the same query scope; use distinct ids for container vs. inner components to prevent E2E query cardinality failures.

Example (Vitest):
```ts
import { describe, it, expect, vi } from 'vitest';

// Ensure both guard paths and the interaction path are tested.
describe('Pointer guard + action', () => {
  it('ignores non-primary pointer in hold mode', () => {
    // render component with hold mode; use user-event/pointer helper
    // pointer(button, 'pointerdown', pointerId=1, mouseButton=2)
    // expect(start).not.toHaveBeenCalled();
    expect(true).toBe(true);
  });

  it('opens overflow menu and executes host action', async () => {
    const onShare = vi.fn();
    // render PaneHeaderActions with a host action
    // force collapse widths
    // click overflow trigger
    // expect(menu items include 'Share')
    // click menu item -> expect(onShare).toHaveBeenCalledTimes(1)
    expect(onShare).toHaveBeenCalledTimes(0);
  });
});
```

Adopting this standard prevents the recurring issues seen across discussions: untested shipped branches, missing guard negatives, interaction paths that stop short of what users do, and fragile test selector collisions.