---
title: Improve code readability
description: Structure code to match logical flow and extract intermediate variables
  to improve readability. When dealing with multiple discrete cases, prefer switch
  statements over if/else chains for better extensibility. Replace magic numbers with
  named constants for self-documentation.
repository: discourse/discourse
label: Code Style
language: JavaScript
comments_count: 5
repository_stars: 44898
---

Structure code to match logical flow and extract intermediate variables to improve readability. When dealing with multiple discrete cases, prefer switch statements over if/else chains for better extensibility. Replace magic numbers with named constants for self-documentation.

Examples:

**Restructure conditionals to match logical flow:**
```js
// Instead of complex nested logic, make structure follow the logic
if (isDark) {
  load(…, true);
} else {
  load(…, false);
  load(…, true);
}
```

**Extract intermediate variables:**
```js
// Extract complex expressions into named variables
const paramsString = transformedParams.join(", ");
return `[quote="${paramsString}"]\n${contents.trim()}\n[/quote]\n\n`;
```

**Use switch for multiple cases:**
```js
// Switch statements are more extensible than if/else chains
switch (this.typeFilter) {
  case "user_selectable":
    schemes = schemes.filter((scheme) => scheme.user_selectable);
    break;
  case "from_theme":
    schemes = schemes.filter((scheme) => scheme.theme_id);
    break;
}
```

**Replace magic numbers:**
```js
// Use named constants instead of magic numbers
const MAX_RESULTS = 20;
const MIN_ITEMS_FOR_FILTER = 8;
```