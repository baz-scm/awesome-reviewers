---
title: Naming consistency rules
description: 'When naming or rewriting identifiers (including compiler output), preserve
  meaning and avoid unnecessary renames.


  Apply these rules:

  1) Don’t rename what’s already explicitly named.'
repository: facebook/react#b11
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 251894
---

When naming or rewriting identifiers (including compiler output), preserve meaning and avoid unnecessary renames.

Apply these rules:
1) Don’t rename what’s already explicitly named.
   - If a function has a real name in source, keep it.
   - Only generate/adjust names when the function is truly anonymous but moved/assigned into a named binding or property path.
2) Use correct external key names, but consistent local identifiers.
   - For destructuring, match the exact property/key. If the key contains characters not valid as an identifier (e.g., kebab-case), use a quoted key.
   - If the variable name matches the property name, prefer shorthand.
3) Keep generated names concise for known framework patterns.
   - For built-in React hooks/patterns, avoid redundant index noise in naming if the pattern can be represented more directly.

Examples:
```js
// Prefer shorthand when names match
const { disabled } = t0;

// Quote external keys when needed, but keep local naming consistent
const { 'aria-label': ariaLabel } = t0;

// Rename/adjust anonymous functions only when necessary
// Keep explicitly named functions unchanged.
function named() {
  /* ... */
}

// If an inner function is anonymous but attached via a variable/property context,
// give it a stable name derived from that context.
const x = () => {
  const y = () => props.named;
  return y();
};
```

Outcome: stable, readable identifiers; fewer noisy diffs; and correct mapping between external API names (props/keys) and internal variable names.