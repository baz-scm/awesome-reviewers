---
title: Semantic HTML usage
description: 'Use HTML elements according to their semantic purpose to ensure proper
  accessibility and code organization. Choose elements based on their intended role,
  not just how they appear visually:'
repository: rails/rails
label: Code Style
language: Other
comments_count: 3
repository_stars: 57027
---

Use HTML elements according to their semantic purpose to ensure proper accessibility and code organization. Choose elements based on their intended role, not just how they appear visually:

1. Use `<nav>` only for sections containing navigation links, not for containers with single links or static content
2. Place `<footer>` appropriately within document structure (can be inside `<article>` or `<section>`)
3. Use `role="button"` for links that behave like buttons rather than navigation

Example of proper semantic structure:
```html
<main>
  <article>
    <header id="feature">
      <!-- article introduction -->
      <!-- chapter index / toc -->
    </header>   

    <!-- article contents with headings -->    

    <footer>
      <h2>Feedback</h2>
      <!-- feedback explanation -->
    </footer>
  </article>
</main>
```

When HTML semantics aren't consistently recognized by screen readers, add explicit ARIA roles and attributes to enhance accessibility. This improves both code organization and the experience for users of assistive technologies.
