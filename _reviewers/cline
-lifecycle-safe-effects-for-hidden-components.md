---
title: Lifecycle-safe effects for hidden components
description: When a component can be hidden and later shown again without a true unmount
  (e.g. wrapped in React's `<Activity>`, or swapped behind a conditional render while
  state refs survive), its effects will be torn down and re-run on every visibility
  change, but any state held in refs or module scope persists. Cleanup and setup logic
  written only for a final unmount...
repository: "cline/cline\r\n"
label: React
language: TSX
comments_count: 6
repository_stars: 70946
---

When a component can be hidden and later shown again without a true unmount (e.g. wrapped in React's `<Activity>`, or swapped behind a conditional render while state refs survive), its effects will be torn down and re-run on every visibility change, but any state held in refs or module scope persists. Cleanup and setup logic written only for a final unmount will silently break the resumed instance. Audit every effect in such components for these failure modes:

- **Timers/intervals**: cleanup must clear the handle and also reset the ref to its "idle" sentinel (e.g. `null`), not just call `clearTimeout`. Otherwise the scheduler on remount sees a stale non-null ref and refuses to arm a new timer, silently dropping pending work (e.g. a buffered stream flush that never gets re-scheduled).
- **In-flight async/UI state**: if cleanup cancels an underlying operation (a recording, a request), it must also reset the associated state flags (`isListening`, `isProcessing`, etc.) to their idle values and notify any callback that depends on them. Otherwise the resumed component shows inconsistent UI even though the operation was actually cancelled.
- **"Run once" bootstrap effects**: separate work that must happen only once per logical session (e.g. initial navigation/selection) from work that should re-run on every mount (e.g. refreshing data on reconnect). Guard the once-only part with a ref, since refs are preserved across hide/show cycles even though the effect itself re-executes.
- **Overlays/dialogs during hide**: prefer replacing a component with its fallback (e.g. a startup/error screen) rather than rendering the fallback on top of it. A covered-but-still-mounted component can keep a dialog's focus trap or body-level side effects (e.g. `pointer-events: none`, `inert`) active, blocking the visible screen.

Add regression tests that explicitly hide and re-show the component (e.g. via `<Activity mode="hidden">` then `"visible"`) while an operation is pending, and assert the resumed state is correct — this class of bug does not show up in tests that only mount and unmount once.