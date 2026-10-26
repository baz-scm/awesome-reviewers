---
title: Accessible, locale-safe UI
description: 'When writing UI code, treat accessibility, internationalization, and
  usability as part of code style: use native interactive elements (or fully compliant
  custom widgets), build user-facing strings with locale-safe formatting, and choose
  layout behaviors that keep important controls reachable.'
repository: cline/cline#v3
label: Code Style
language: TSX
comments_count: 5
repository_stars: 70863
---

When writing UI code, treat accessibility, internationalization, and usability as part of code style: use native interactive elements (or fully compliant custom widgets), build user-facing strings with locale-safe formatting, and choose layout behaviors that keep important controls reachable.

Apply these rules:
1) Prefer native elements for actions
- Use `<button type="button">` for clickable UI that triggers behavior. Style it like a link if needed, but keep correct semantics.

```tsx
<button
  type="button"
  className="underline cursor-pointer"
  onClick={handleModelButtonClick}
>
  Choose a model
</button>
```

2) For custom controls, add required ARIA + keyboard support
- If you implement a custom interactive widget (e.g., a resize handle), make it focusable and expose the correct role (e.g., `role="separator"`) and keyboard behavior (e.g., ArrowUp/ArrowDown; optionally Shift for larger steps).

3) Avoid hardcoded punctuation/word order in translated strings
- Don’t concatenate strings with manual separators like `", "` unless the translation system handles it.
- Build each part as a complete, localized phrase, then join with `Intl.ListFormat` so separators match the user’s locale.

```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t("chatView:toolGroup.files", { count: counts.read }));
if (counts.list > 0) parts.push(t("chatView:toolGroup.folders", { count: counts.list }));

if (parts.length === 0) return t("chatView:toolGroup.contextFallback");

const list = new Intl.ListFormat(undefined, { style: "long", type: "conjunction" }).format(parts);
return t("chatView:toolGroup.summary", { items: list });
```

4) Use layout patterns that preserve reachability
- Prefer truncation over scrolling/overflow when it would clip attached/active visuals or hide critical controls (e.g., tab labels should truncate so the “+” and hide button remain clickable).
- Cap modal/dialog height to the viewport and enable internal scrolling so key actions remain accessible on short screens.

Following this reduces “word salad” translations, prevents keyboard/a11y regressions, and keeps UI controls usable across different screen sizes and tab counts.