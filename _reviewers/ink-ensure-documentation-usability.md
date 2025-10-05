---
title: Ensure documentation usability
description: Documentation should be practical and serve its intended audience effectively.
  Examples must be runnable out-of-the-box or include clear setup instructions, while
  API documentation should focus on public interfaces that users actually need.
repository: vadimdemedes/ink
label: Documentation
language: JavaScript
comments_count: 2
repository_stars: 31825
---

Documentation should be practical and serve its intended audience effectively. Examples must be runnable out-of-the-box or include clear setup instructions, while API documentation should focus on public interfaces that users actually need.

For code examples, ensure they can be executed without complex setup. If dependencies are required, either make examples self-contained or provide clear integration guidance in appropriate documentation sections.

For API documentation, document public methods and parameters that users will interact with, but avoid exposing internal implementation details that could confuse or mislead developers.

Example of good practice:
```javascript
// Good: Clear public API documentation
/**
 * Unmounts the component instance
 * @returns {void}
 */
unmount() {
  // Internal error handling hidden from public API
  this.internalUnmount(error);
}
```

Rather than documenting internal parameters like `unmount(error)` that users shouldn't use, keep the public interface clean and move complex examples to dedicated recipe documentation where proper context can be provided.