---
title: Manage bindings and state
description: Ensure components explicitly initialize reactive state, manage input/keybinding
  lifecycle, and decide whether children should subscribe to live atoms or use a stable
  snapshot.
repository: wavetermdev/waveterm
label: React
language: TSX
comments_count: 9
repository_stars: 17328
---

Ensure components explicitly initialize reactive state, manage input/keybinding lifecycle, and decide whether children should subscribe to live atoms or use a stable snapshot.

Why: Discussions repeatedly show bugs from missing MobX setup, duplicated or double-registered keybindings, accidental live updates that change UI unexpectedly, and inconsistent key handling logic. This guideline makes component behavior predictable and prevents leaks, duplicate handlers, and surprising re-renders.

How to apply (practical checklist):
- Initialize MobX observables in class components. In the constructor call mobx.makeObservable(this, { /* annotations */ }).
  Example:
  constructor(props) {
      super(props);
      mobx.makeObservable(this, { someState: mobx.observable, someAction: mobx.action });
  }

- Guard per-instance keybinding registration and always clean up. Use a per-instance domain name and a boolean observable to avoid double registration. Unregister the domain on unmount.
  Example pattern:
  keybindsRegistered = mobx.observable.box(false);

  componentDidMount() {
      if (!this.keybindsRegistered.get()) {
          mobx.action(() => this.keybindsRegistered.set(true))();
          const domain = `datepicker-${this.uuid}-${part}`;
          GlobalModel.keybindManager.registerKeybinding("control", domain, "generic:selectLeft", () => { /*...*/; return true; });
          // register other keys
      }
  }

  componentWillUnmount() {
      GlobalModel.keybindManager.unregisterDomain(`datepicker-${this.uuid}`);
      mobx.action(() => this.keybindsRegistered.set(false))();
  }

- Decide snapshot vs subscription intentionally:
  - If a modal or view must remain stable once opened (should not disappear mid-use), read a snapshot once (e.g., store initial value in a ref) and avoid subscribing to live updates.
    Example: initialVersionRef.current = clientData.meta?.["onboarding:lastversion"] ?? "v0.0.0";
  - If you pass atoms/observable values to children, ensure the child subscribes to the atom (or expose a stable derived value) so changes propagate correctly. If passing an atom, the child must read/subscribe to it.

- Use centralized key-check utilities for consistent cross-platform modifier handling instead of ad-hoc e.code and getModifierState checks.
  Example: if (GlobalModel.checkKeyPressed(e, GlobalModel.KeyPressModifierControl + ":g")) { /* ... */ }

- When using props with reactive frameworks (Preact/MobX quirks), if direct access triggers warnings, copy props into component fields/observables in the constructor to stabilize access.
  Example: this.props_ = props; // or makeObservable-backed copy if needed

- Prefer reuse of components/resources (keybinding modules, shared UI pieces) rather than duplicating logic across similar views. Extract shared keybinding registration or UI into a reusable component or hook.

- Always document domain naming and lifecycle expectations for keybinding consumers to avoid collisions and duplicate registrations.

Benefits: predictable lifecycle, fewer memory leaks or double-registrations, clearer intent about subscription semantics, consistent key handling, and easier reuse of UI and logic across components.