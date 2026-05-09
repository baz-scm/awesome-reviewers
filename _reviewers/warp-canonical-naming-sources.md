---
title: Canonical Naming Sources
description: Use canonical, source-verified naming for identifiers and for artifact
  locations. Avoid guesses, stale references, or incidental structure (like username
  folders).
repository: warpdotdev/warp
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 56893
---

Use canonical, source-verified naming for identifiers and for artifact locations. Avoid guesses, stale references, or incidental structure (like username folders).

Apply:
- **Action/UI names and shortcuts in docs**: Only reference action IDs and default bindings that are confirmed against the source of truth. If the correct name can’t be discovered from disk, don’t invent one—either direct users to the correct settings page for lookup or require explicit confirmation.
- **Spec/artifact file placement**: Place specs in the prescribed directory scheme based on the **linear ticket id** (not usernames or ad-hoc nesting).

Example (action naming rule):
- Good: point users to the actual editor action (e.g., `workspace:show_keybinding_settings`) rather than a similarly named page action.
- Bad: reference `cmd-k` / `workspace:toggle_keybindings_page` if source verification shows the canonical editor shortcut/action is different.

Example (path naming rule):
- Good: `specs/<linear-ticket-id>/...`.
- Bad: `specs/<username>/<linear-ticket-id>/...` or any structure that doesn’t match the ticket-id convention.