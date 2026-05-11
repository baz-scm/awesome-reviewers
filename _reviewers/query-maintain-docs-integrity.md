---
title: Maintain Docs Integrity
description: 'Documentation should be kept correct and maintainable like code: ensure
  pages are registered, links are stable/valid, and shared doc sections follow the
  adapter conventions.'
repository: tanstack/query
label: Documentation
language: Markdown
comments_count: 9
repository_stars: 49380
---

Documentation should be kept correct and maintainable like code: ensure pages are registered, links are stable/valid, and shared doc sections follow the adapter conventions.

Apply these rules:
- Register docs pages: when adding a new reference/guide entry, add the corresponding `id` to `docs/config.json` so it appears in the site navigation.
- Use correct relative links: verify relative paths (including required `.md` extensions) so builds don’t break.
- Keep source links stable: if you link to GitHub source, point to the correct repository and use a commit-hash permalink (avoid `main` and fragile line-number URLs).
- Follow adapter overwrite conventions: use the established block markers so other framework adapters can safely overwrite sections (e.g., maintain React/Vue marker keyword conventions like `Info` vs `Example`).
- Avoid brittle, non-exhaustive explanations: when describing behavior triggers, link to the canonical guide (e.g., “important-defaults”) instead of listing a possibly incomplete set.

Example pattern for adapter-overwritable sections:
```md
[//]: # 'Info2'

:::tip
React-specific note...
:::

[//]: # 'Info2'
```

Example pattern for canonical cross-linking:
- Don’t write “it happens on X/Y/Z triggers” unless X/Y/Z is guaranteed exhaustive; instead link to the canonical defaults doc that defines the trigger list.