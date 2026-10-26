---
title: Consistent UI Style
description: 'When writing UI code, apply consistent patterns that keep both layout
  and user-facing text correct across edge cases and locales.


  - For horizontally constrained components (tabs, chips, toolbars):'
repository: cline/cline#v21
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70886
---

When writing UI code, apply consistent patterns that keep both layout and user-facing text correct across edge cases and locales.

- For horizontally constrained components (tabs, chips, toolbars):
  - Use flex overflow-safe sizing: apply `min-w-0` to wrappers/labels and use truncation (ellipsis) rather than scrolling strips when the UI must visually “attach” to another region.
  - Ensure essential controls (e.g., add/close buttons) remain visible and clickable even with many items.

  Example pattern:
  ```tsx
  <div className="flex min-w-0 items-center">
    <span className="min-w-0 truncate">{label}</span>
  </div>
  ```

- For localized summary strings (counts/lists):
  - Don’t hardcode grammar or separators (e.g., `", "`); build each segment as a self-contained verb phrase and join using `Intl.ListFormat` for the current locale.

  Example pattern:
  ```ts
  const parts: string[] = [];
  if (countA > 0) parts.push(t('key.a', { count: countA }));
  if (countB > 0) parts.push(t('key.b', { count: countB }));

  if (parts.length === 0) return t('key.fallback');
  return new Intl.ListFormat(locale, { style: 'long', type: 'conjunction' }).format(parts);
  ```

- For shared UI primitives (icons, components):
  - Prefer the established import/usage pattern from the common UI package so icon choice and styling are easy to audit and consistent across the repo.