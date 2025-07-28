---
title: organize accessibility attributes
description: Systematically organize HTML elements by adding appropriate accessibility
  attributes (aria-label, role) to improve code structure and semantic clarity. Place
  accessibility attributes immediately after class attributes for consistent code
  organization and enhanced readability.
repository: nuxt/nuxt
label: Code Style
language: Html
comments_count: 2
repository_stars: 57769
---

Systematically organize HTML elements by adding appropriate accessibility attributes (aria-label, role) to improve code structure and semantic clarity. Place accessibility attributes immediately after class attributes for consistent code organization and enhanced readability.

When working with semantic HTML elements like headings and images, ensure each element includes descriptive accessibility attributes that clearly identify their purpose and content. This creates more organized, self-documenting code that follows accessibility best practices.

Example:
```html
<!-- Before -->
<h1 class="flex flex-col gap-y-4 items-center justify-center">
<svg class="h-8 sm:h-12" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 800 200">

<!-- After -->
<h1 class="flex flex-col gap-y-4 items-center justify-center" aria-label="Nuxt {{ version }}">
<svg role="img" aria-label="Nuxt" class="h-8 sm:h-12" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 800 200">
```

This approach ensures consistent attribute organization while making the code more accessible and maintainable.