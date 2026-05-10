---
title: Consistent Style And Diffs
description: 'Apply a consistent, tool-friendly coding style to reduce formatting
  churn and improve readability.


  **Rules**

  - **Keep diffs stable:** Don’t apply formatting-only changes to existing tests/cases
  unless the PR’s purpose is explicitly formatting coverage. Revert incidental alignment/whitespace
  changes; add new focused cases instead.'
repository: mermaid-js/mermaid
label: Code Style
language: JavaScript
comments_count: 8
repository_stars: 87952
---

Apply a consistent, tool-friendly coding style to reduce formatting churn and improve readability.

**Rules**
- **Keep diffs stable:** Don’t apply formatting-only changes to existing tests/cases unless the PR’s purpose is explicitly formatting coverage. Revert incidental alignment/whitespace changes; add new focused cases instead.
- **Respect formatter/tool expectations:** e.g., avoid adding/removing whitespace in import groups if your tooling depends on it.
- **String/concatenation consistency:** build class/name strings consistently (no mixed whitespace prefixes like ` ' ' + a` sometimes vs `a + ' '` other times). Prefer a single consistent pattern.
- **Use clearer JS constructs:**
  - Prefer **template literals/backticks** for readability when composing multi-line strings or larger literals.
  - Use **`===` / `!==`** everywhere (avoid `==`).
  - Prefer **early returns** to simplify nested conditionals.
  - Avoid **magic numbers** in new code; use named constants if values affect layout/logic.

**Example (test string readability + stable diffs)**
```js
it('should parse bidirectional arrow', async () => {
  const str = `sequenceDiagram\nAlice-><Bob:Hello Bob, how are you?`;
  await mermaidAPI.parse(str);
  const messages = diagram.db.getMessages();
  expect(messages).toHaveLength(1);
});
```

**Example (avoid magic numbers)**
```js
const TODAY_LINE_WIDTH = 30;
line.attr('y2', conf.titleTopMargin + TODAY_LINE_WIDTH);
```

Use this checklist when preparing commits: if a change is purely formatting, isolate it (or revert it) and keep PR intent behavior-focused.