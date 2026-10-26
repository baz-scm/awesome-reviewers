---
title: Minimize Verbosity
description: 'Write UI/style code to be correct without becoming noisy:


  - **Preserve intentional inline spacing.** If you remove whitespace nodes, ensure
  the rendered text still has separation via an explicit space or a CSS rule.'
repository: microsoft/VSCode
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 194303
---

Write UI/style code to be correct without becoming noisy:

- **Preserve intentional inline spacing.** If you remove whitespace nodes, ensure the rendered text still has separation via an explicit space or a CSS rule.
  ```ts
  // Good: explicit separator without relying on removed whitespace nodes
  titleEl.appendChild(document.createTextNode(' '));
  DOM.append(titleEl, $('a.section-title-link.migration-learn-more-link'));
  // Or prefer CSS-driven spacing on the link element.
  ```

- **Avoid repetitive inline styles in render loops.** If the renderer emits the same inline declarations per character/item, move them to a CSS class (or a shared styling mechanism) and keep only truly data-specific values inline.
  ```ts
  // Prefer:
  // .fullWidthCharacter { display:inline-block; box-sizing:border-box; text-align:center; }
  // then set width via inline style only
  sb.appendString('class="fullWidthCharacter" style="width:');
  sb.appendString(String(fullWidthCharacterWidth));
  sb.appendString('px"');
  ```

- **Don’t introduce “one-off” abstractions/files.** If a helper/class is only used in one place, inline it or keep it co-located; avoid extra indirection that obscures intent.

- **Keep imports single-sourced.** Don’t re-export constants just to change import paths—import from the canonical module.

- **Keep comments tight.** Prefer short comments that add constraints not immediately obvious from the code; remove lengthy “restating what the code does” text.

These practices keep code readable, reduce generated UI markup noise, and prevent subtle rendering regressions.