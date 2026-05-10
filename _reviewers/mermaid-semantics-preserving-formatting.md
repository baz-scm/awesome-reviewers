---
title: Semantics-Preserving Formatting
description: 'Code-style changes (formatting, spacing, selector tweaks, spell/lint
  adjustments) must not alter semantics or intended content.


  - CSS: scope styling to the minimal element needed (avoid global or overly broad
  selectors). Prefer targeted selectors like:'
repository: mermaid-js/mermaid
label: Code Style
language: Html
comments_count: 2
repository_stars: 87952
---

Code-style changes (formatting, spacing, selector tweaks, spell/lint adjustments) must not alter semantics or intended content.

- CSS: scope styling to the minimal element needed (avoid global or overly broad selectors). Prefer targeted selectors like:
  ```css
  div.mermaid svg:first-of-type {
    border: 2px solid darkred;
  }
  ```
- Strings/markup: preserve exact characters across line breaks and escaping. If a split token is intentional (e.g., for XSS test payload construction), don’t “join”/reformat it in a way that changes the resulting string.
- Tooling noise: if spellcheck/lint flags intentionally split/obfuscated content, suppress it explicitly (e.g., via a dedicated `codespell-ignore` pragma) rather than changing the underlying payload.

This prevents unintended styling regressions and avoids subtle bugs from formatting-induced content changes.