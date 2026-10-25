---
title: Locale-Aware UI Text
description: 'When formatting UI output, treat localization/wording and interactive
  semantics as part of code style:


  - Build user-facing summaries from self-contained, fully translated phrases (avoid
  assembling with hardcoded “read/search/folder” fragments and manual punctuation).'
repository: cline/CLINE
label: Code Style
language: TSX
comments_count: 3
repository_stars: 70839
---

When formatting UI output, treat localization/wording and interactive semantics as part of code style:

- Build user-facing summaries from self-contained, fully translated phrases (avoid assembling with hardcoded “read/search/folder” fragments and manual punctuation).
- Use locale-aware list/joining (e.g., Intl.ListFormat) and localized verb phrases so languages with different grammar (e.g., Korean) don’t produce unnatural text.
- Preserve semantic correctness for controls: use the right HTML element for the action (e.g., a real button for click/keyboard activation) even if it’s styled like a link.
- Prefer shared UI primitives/components (e.g., standard icon components/imports) to keep style consistent and easy to verify.

Example (pattern):
```ts
const parts: string[] = [];
if (counts.read > 0) parts.push(t('chatView:toolGroup.files', { count: counts.read }));
if (counts.list > 0) parts.push(t('chatView:toolGroup.folders', { count: counts.list }));
// ...
if (parts.length === 0) return t('chatView:toolGroup.contextFallback');
return t('chatView:toolGroup.summary', { items: new Intl.ListFormat(locale).format(parts) });
```
And for interactivity:
```tsx
<button type="button" onClick={handleModelButtonClick}>Choose model</button>
```