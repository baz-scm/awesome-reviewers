---
title: Add explanatory comments
description: Add explanatory comments for complex logic, special cases, or non-obvious
  code behavior. Comments should explain the "why" behind the code and "what" specific
  conditions or syntax patterns are being handled.
repository: prettier/prettier
label: Documentation
language: JavaScript
comments_count: 5
repository_stars: 50772
---

Add explanatory comments for complex logic, special cases, or non-obvious code behavior. Comments should explain the "why" behind the code and "what" specific conditions or syntax patterns are being handled.

When code involves:
- Complex conditional logic or pattern matching
- Special handling for edge cases
- Non-obvious business rules or technical requirements
- Code that exists for specific external compatibility reasons

Include comments that:
- Explain the purpose and reasoning
- Provide concrete examples when helpful
- Reference external documentation or issues when relevant

Example from the discussions:
```javascript
// Prettier does not officially support stylus.
// But, we need to handle "stylus" here for printing a style block in Vue SFC as stylus code by external plugin.
// https://github.com/prettier/prettier/pull/12707
if (lang === "stylus") {
  return inferParserByLanguage("stylus", options);
}
```

Or for complex conditions:
```javascript
// For example, there is the following key-value pair:
//   "xs-only": "only screen and (max-width: #{map-get($grid-breakpoints, "sm")-1})"
// "only screen and (max-width: #{map-get($grid-breakpoints, " is a "value-string"
// and "sm" is a "value-word"
// We should not insert any spaces and lines here.
if (isMapItemNode) {
  const isPartOfValue = node.groups?.[1]?.type === "value-colon" && i > 1;
  // ...
}
```

Avoid over-commenting simple or self-explanatory code, but err on the side of clarity for complex logic that future maintainers will need to understand.