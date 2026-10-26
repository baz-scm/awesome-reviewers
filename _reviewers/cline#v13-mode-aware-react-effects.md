---
title: Mode-aware React Effects
description: 'Adopt a single, explicit “mode” signal that coordinates React state
  and any global/DOM listeners. When entering a temporary mode (e.g., recording, special
  keybinding handling, hidden UI), all related effects must:'
repository: cline/cline#v13
label: React
language: TSX
comments_count: 3
repository_stars: 70874
---

Adopt a single, explicit “mode” signal that coordinates React state and any global/DOM listeners. When entering a temporary mode (e.g., recording, special keybinding handling, hidden UI), all related effects must:

1) **Gate behavior on shared mode state** (e.g., `areShortcutsSuspended()`, `visible/hidden`). If the mode says “do not act,” event handlers should no-op and perform cleanup.
2) **Ensure the owning handler stops other consumers.** When a component owns a matched key/mouse interaction, call `preventDefault()` and `stopImmediatePropagation()` so other capture/bubbling listeners don’t also process it.
3) **Make cleanup restore UI correctness.** For patterns like “keep state but unmount effects” (hidden Activity), effect cleanup must both **cancel in-flight work** and **reset derived UI flags** so showing again restores the correct user state.

Example pattern (keyboard capture + suspension gating):
```ts
useEffect(() => {
  if (!recording) return;

  // Ensure all other shortcut handlers know the mode.
  const release = suspendShortcuts();

  const onKeyDown = (event: KeyboardEvent) => {
    if (areShortcutsSuspended()) {
      // This component owns the key; block other listeners.
      event.preventDefault();
      event.stopImmediatePropagation();
      // ...handle key for recording...
    }
  };

  window.addEventListener('keydown', onKeyDown, { capture: true });
  return () => {
    window.removeEventListener('keydown', onKeyDown, { capture: true } as any);
    release(); // “suspends shortcuts until every suspension is released”
  };
}, [recording]);
```

Practical checklist:
- Any component that installs `window/document` listeners should check a shared mode before acting.
- Any effect that starts timers/recordings/async work should cancel them in cleanup.
- Any effect that influences user-facing flags (e.g., “listening/processing”) must reset those flags in cleanup when effects are unmounted due to visibility changes.