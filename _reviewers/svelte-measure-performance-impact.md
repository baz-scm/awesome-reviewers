---
title: Measure performance impact
description: Before making performance-related changes, measure the actual impact
  with benchmarks and profiling. Many performance assumptions can be misleading without
  data.
repository: sveltejs/svelte
label: Performance Optimization
language: JavaScript
comments_count: 7
repository_stars: 83580
---

Before making performance-related changes, measure the actual impact with benchmarks and profiling. Many performance assumptions can be misleading without data.

When performance concerns arise, create realistic benchmarks that reflect actual usage patterns. For example, when evaluating DOM operations:

```js
function run(n = 1e6) {
  const els = Array(n);
  let i = n;
  while (i--) {
    let div = document.createElement('div');
    document.body.append(div);
    els[i] = div;
  }
  console.time('test');
  i = n;
  while (i--) {
    const div = els[i];
    div.nodeName.includes('-');
    div.namespaceURI === 'http://www.w3.org/1999/xhtml';
  }
  console.timeEnd('test');
}
```

Consider algorithmic complexity when choosing data structures. For operations like array lookups, analyze whether `O(n*m)` approaches like `array.indexOf()` should be replaced with `O(n+m)` alternatives using `Set`:

```js
// O(select.options.length * value.length)
option.selected = ~value.indexOf(get_option_value(option));

// O(select.options.length + value.length)  
const values = new Set(value);
option.selected = values.has(get_option_value(option));
```

Add performance guards for expensive operations, but validate they're actually needed. Avoid premature optimization while ensuring real bottlenecks are addressed with measurable improvements.