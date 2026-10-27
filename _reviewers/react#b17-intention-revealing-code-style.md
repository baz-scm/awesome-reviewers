---
title: Intention-Revealing Code Style
description: 'When defining exported/constructed objects or helper APIs, write code
  that is self-contained and makes data flow obvious.


  1) Avoid “placeholder then overwrite” construction'
repository: facebook/react#b17
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251891
---

When defining exported/constructed objects or helper APIs, write code that is self-contained and makes data flow obvious.

1) Avoid “placeholder then overwrite” construction
- If an exported object needs computed values, define them in place (e.g., via accessors/getters) instead of creating an empty object with a temporary type and mutating/replacing it later.

Example pattern:
```ts
const plugin = { /* ... */ };

const recommendedConfig = {
  plugins: {
    get 'react-hooks'() {
      return plugin;
    },
  },
  rules: recommendedRuleConfigs,
};
```

2) Make mutation vs return explicit in helper APIs
- If a function writes to an accumulator (like a `Set`), ensure the signature/body clearly signals that it “adds to deps” (or consider returning a value and merging at the caller). This improves readability and reduces surprise.

Example pattern (return instead of mutating):
```ts
function collectDeps(fn: FunctionExpression | undefined): Array<IdentifierId> {
  if (!fn) return [];
  // compute identifiers...
  return [/* ... */];
}

// caller merges
for (const id of collectDeps(fn)) deps.add(id);
```

Apply this to keep code organized, reduce mental overhead, and make behavior predictable for readers and users of the API.