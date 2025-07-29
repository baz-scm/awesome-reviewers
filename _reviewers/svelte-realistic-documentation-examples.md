---
title: realistic documentation examples
description: Use practical, complete examples in documentation rather than oversimplified
  or contrived ones that cut corners. Documentation examples should reflect real-world
  usage patterns and include necessary context, edge cases, and limitations.
repository: sveltejs/svelte
label: Documentation
language: Markdown
comments_count: 15
repository_stars: 83580
---

Use practical, complete examples in documentation rather than oversimplified or contrived ones that cut corners. Documentation examples should reflect real-world usage patterns and include necessary context, edge cases, and limitations.

Avoid examples that:
- Cut corners for brevity (like localStorage without SSR checks)
- Are overly contrived or artificial
- Omit important details or error handling
- Don't show realistic usage patterns

Instead, provide examples that:
- Include necessary context and setup
- Show proper error handling and edge cases
- Demonstrate realistic usage scenarios
- Explain limitations and considerations

For example, when documenting state management, instead of a simple localStorage example that ignores SSR concerns:

```js
// Avoid: Oversimplified example
let data = $state([], {
  onchange() {
    localStorage.setItem('data', JSON.stringify(data));
  }
});
```

Provide a more complete example or choose a simpler concept:

```js
// Better: Realistic validation example
let email = $state('', {
  onchange() {
    if (email && !email.includes('@')) {
      console.warn('Invalid email format');
    }
  }
});
```

This ensures developers can apply the concepts correctly in their own projects without encountering unexpected issues or missing critical implementation details.