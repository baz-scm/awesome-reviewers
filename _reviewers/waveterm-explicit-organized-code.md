---
title: Explicit, organized code
description: 'Write code that is explicit, predictable, and organized to improve readability
  and avoid subtle bugs.


  What to do:

  - Make control flow explicit. In switch statements and other control structures
  always use break/return/continue as appropriate. If fallthrough is intentional,
  annotate it with a clear comment or a lint directive (e.g. // fallthrough). Example...'
repository: wavetermdev/waveterm
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 17328
---

Write code that is explicit, predictable, and organized to improve readability and avoid subtle bugs.

What to do:
- Make control flow explicit. In switch statements and other control structures always use break/return/continue as appropriate. If fallthrough is intentional, annotate it with a clear comment or a lint directive (e.g. // fallthrough). Example (fix missing break):
  switch (action.type) {
    case LayoutTreeActionType.ReplaceNode: {
      // ...handle replace...
      break; // prevent accidental fallthrough
    }
    case LayoutTreeActionType.SplitHorizontal: {
      // ...handle split...
      break;
    }
  }

- Avoid redundant calls and duplicate side-effects. Trust single-responsibility helpers and do not repeat work already performed by a called method. If a method already sets state, do not call the setter again. Example (remove duplication):
  openAIAssistantChat(): void {
    this.setActiveAuxView(appconst.InputAuxView_AIChat);
    // don't also call this.setAuxViewFocus(true) if setActiveAuxView already sets focus
  }

- Organize runtime values and small types where they belong. Place enums, constants, and small runtime-bound types close to the code that uses them unless there's a strong reason to centralize them. If you move a value to a shared file, document why (runtime usage, reuse across modules).

Why this matters:
- Explicit control flow prevents accidental bugs from fallthrough and makes intent clear.
- Removing redundant calls reduces unexpected state changes and simplifies reasoning about code.
- Colocating related runtime values improves discoverability and keeps code meaningfully grouped.

When in doubt, prefer clarity: add a short comment explaining non-obvious choices (intentional fallthrough, why a value is placed in a shared file, or why a duplicate call remains).