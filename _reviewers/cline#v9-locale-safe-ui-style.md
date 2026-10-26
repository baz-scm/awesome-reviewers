---
title: Locale-safe UI style
description: 'When adding UI logic, follow three consistency rules: (1) make text
  composition locale-aware (no hardcoded separators/English word order), (2) use semantic
  HTML for interactivity (buttons for actions; anchors for navigation), and (3) design
  overflow behavior for clickability (shrink+truncate rather than clipping/scrolling
  when the layout relies on visual...'
repository: cline/cline#v9
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70868
---

When adding UI logic, follow three consistency rules: (1) make text composition locale-aware (no hardcoded separators/English word order), (2) use semantic HTML for interactivity (buttons for actions; anchors for navigation), and (3) design overflow behavior for clickability (shrink+truncate rather than clipping/scrolling when the layout relies on visual attachment).

How to apply:
- Locale-safe strings
  - Build summary pieces as self-contained phrases, then join with a locale mechanism (e.g., `Intl.ListFormat`).
  - Handle empty-state text via a dedicated localized fallback.
  - Avoid hardcoded separators like `", "` inside formatted sentences.
  - Example:
    ```ts
    const parts = [
      t('chatView:toolGroup.files', { count: counts.read }),
      t('chatView:toolGroup.folders', { count: counts.list }),
    ].filter(Boolean);

    if (parts.length === 0) return t('chatView:toolGroup.contextFallback');

    const items = new Intl.ListFormat(undefined, { style: 'long', type: 'conjunction' })
      .format(parts);

    return t('chatView:toolGroup.summary', { items }); // e.g., "Cline {items}"
    ```
- Accessible interactive controls
  - If it triggers an action (e.g., “choose model”), use a real `<button type="button">` (styled as needed).
  - Keep tests aligned to semantics (assert button role/keyboard behavior).
  - Example:
    ```tsx
    <button
      type="button"
      className="underline cursor-pointer"
      onClick={handleModelButtonClick}
    >
      Choose a model
    </button>
    ```
- Truncation-safe layout
  - Prefer flexbox shrink/truncate patterns so controls remain reachable and the UI doesn’t rely on clipped overflow.
  - Ensure tab label containers use `min-w-0` + `truncate/ellipsis`, and avoid scrolling containers that can clip visual “attached” effects.
  - Example pattern:
    ```tsx
    <div className="flex min-w-0 items-end">
      <div className="min-w-0 truncate">{label}</div>
    </div>
    ```

Outcome: UI summaries read naturally in all locales, keyboard users can activate actions reliably, and overflow no longer breaks visual continuity or click targets.