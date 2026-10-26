---
title: Reproducible Docs With Guarantees
description: 'When updating technical docs, write them as executable, environment-aware
  workflows and as reliable behavioral descriptions.


  **1) Encode real constraints/workarounds**'
repository: microsoft/VSCode
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 194303
---

When updating technical docs, write them as executable, environment-aware workflows and as reliable behavioral descriptions.

**1) Encode real constraints/workarounds**
- Call out tool/platform limitations explicitly and include the safe alternative patterns.
  - Example patterns to document:
    - Trusted Types restrictions: prefer `document.createElement(...)` + `textContent` over `innerHTML`.
    - UI/selector quirks: specify how to interact when accessible names/roles are missing.

**2) Make workflows deterministic**
- State and enforce preconditions so “what you’ll see” matches the docs:
  - Clean state before starting (clear tabs/toasts/modals in a separate step).
  - Use a safe git strategy so examples don’t depend on uncommitted local state.

  ```bash
  # Example doc pattern
  git commit -am "Update for demo"   # ensure clean state
  git switch --detach "$(git merge-base HEAD origin/main)"  # base build
  npm run build-fast -- --client-only
  # record "before"
  git switch -  # restore demo change
  npm run build-fast -- --client-only
  # record "after" with an in-script assertion (e.g., toast appears only after change)
  ```

**3) Prevent misleading outputs**
- For demos/comparisons, include verification in the scripted workflow (assert expected outcome before/after) so the recording can’t silently show the wrong state.

**4) Describe behavior with stable guarantees, not brittle constants**
- If exact operational numbers (intervals/attempt counts) aren’t part of a stable contract, document the guarantees/bounds and triggers instead of hardcoding exact values—keeping the docs resilient while tests still validate correctness.

Applying this consistently will make documentation both actionable for developers and trustworthy over time.