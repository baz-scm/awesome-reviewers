---
title: Consistent Snippet Style
description: All code snippets, hints, seed code, and automated checks must follow
  a single, consistent formatting and style contract—especially around quote usage
  and basic JS/TS syntax.
repository: freeCodeCamp/freeCodeCamp
label: Code Style
language: Markdown
comments_count: 8
repository_stars: 444449
---

All code snippets, hints, seed code, and automated checks must follow a single, consistent formatting and style contract—especially around quote usage and basic JS/TS syntax.

Apply these rules:
- **Formatting:** use the team’s standard indentation (e.g., 2 spaces) and include semicolons consistently.
- **No broken snippets:** seed code examples must compile/parse; avoid syntax errors and duplicate declarations.
- **Quote-robust tests/hints:** when matching user code, support **both** single and double quotes and (when relevant) ensure the same quote type is used via backreferences.
- **Pattern consistency:** hints should prefer the same DOM/API patterns the seed uses (to avoid ambiguity), unless there’s an explicit reason to allow alternatives.

Example (quote-robust hint regex):
```js
// Matches: document.getElementById('income') or document.getElementById("income")
assert.match(code, /document\.getElementById\(\s*(['"])income\1\s*\)/);
```

Example (style-correct TS):
```ts
function f(): void {
  const x = 1;
  console.log(x);
}
```

Example (avoid duplicate seed declarations):
```ts
const cardDisplay = document.querySelector<HTMLElement>("#current-card")!; 
// (don’t redeclare cardDisplay again)
```