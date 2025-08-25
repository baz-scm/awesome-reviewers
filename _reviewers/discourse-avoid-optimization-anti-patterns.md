---
title: Avoid optimization anti-patterns
description: 'Identify and eliminate code patterns that appear to be performance optimizations
  but actually hurt performance or negate their intended benefits. Common anti-patterns
  include:'
repository: discourse/discourse
label: Performance Optimization
language: Other
comments_count: 3
repository_stars: 44898
---

Identify and eliminate code patterns that appear to be performance optimizations but actually hurt performance or negate their intended benefits. Common anti-patterns include:

1. **Ineffective debouncing**: Cancelling debounce timers immediately before setting new ones defeats the purpose of debouncing and can lead to excessive function calls.

2. **Misused performance decorators**: Using decorators like `@cached` when a native getter would suffice can introduce negative performance implications in modern frameworks.

3. **Excessive component instantiation**: Rendering patterns that create unnecessary component instances (e.g., rendering every placeholder in every position) waste resources and hurt performance.

**Example of debouncing anti-pattern:**
```javascript
// Anti-pattern: Cancelling debounce immediately
if (this.searchTimer) {
  cancel(this.searchTimer); // This negates debouncing benefits
}
this.searchTimer = discourseDebounce(this, this._performSearch, 300);

// Better: Let debounce handle the timing
this.searchTimer = discourseDebounce(this, this._performSearch, 300);
```

Before implementing performance optimizations, verify they actually provide the intended benefit and don't introduce overhead that outweighs their advantages. Profile and measure the impact of optimization patterns to ensure they deliver real performance improvements.