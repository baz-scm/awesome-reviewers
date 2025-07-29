---
title: state boundary management
description: Ensure proper state management when passing reactive values across component
  and function boundaries. State reactivity can be lost when values are read at the
  point of return rather than through getters, setters, or object properties.
repository: sveltejs/svelte
label: React
language: Markdown
comments_count: 4
repository_stars: 83580
---

Ensure proper state management when passing reactive values across component and function boundaries. State reactivity can be lost when values are read at the point of return rather than through getters, setters, or object properties.

When passing state between components or extracting logic into functions, maintain reactivity by:

1. **Use object properties or class instances** - Objects and classes maintain "live" references to their properties
2. **Use getters/setters or functions** - These preserve the reactive connection by deferring the read/write
3. **Avoid direct value extraction** - Reading reactive values at return time fixes them to that moment

```js
// ❌ Loses reactivity - values are read at return time
function createState(initial) {
  let count = $state(initial);
  return { count }; // count is fixed at return time
}

// ✅ Maintains reactivity - using getter/setter
function createState(initial) {
  let count = $state(initial);
  return {
    get count() { return count },
    set count(v) { count = v }
  };
}

// ✅ Maintains reactivity - returning the whole object
function createState(initial) {
  const state = $state({ count: initial });
  return state; // object properties remain reactive
}
```

Props passed from parent components maintain their reactivity only if the parent passed reactive state. Fallback values and non-reactive objects will not trigger updates when mutated. Avoid updating state inside effects as this creates unpredictable behavior and difficult-to-debug applications.