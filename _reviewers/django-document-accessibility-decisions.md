---
title: Document accessibility decisions
description: When implementing HTML templates, add clear comments documenting accessibility-related
  decisions. Explain the purpose of semantic HTML elements, ARIA attributes, and screen
  reader considerations. This ensures that future developers understand the rationale
  behind these choices and preserves accessibility during code modifications.
repository: django/django
label: Documentation
language: Html
comments_count: 3
repository_stars: 84182
---

When implementing HTML templates, add clear comments documenting accessibility-related decisions. Explain the purpose of semantic HTML elements, ARIA attributes, and screen reader considerations. This ensures that future developers understand the rationale behind these choices and preserves accessibility during code modifications.

For example:
```html
<!-- Using <nav> with aria-labelledby provides better semantic structure for screen readers -->
<!-- Visually hidden heading allows screen reader navigation via headers while remaining invisible -->
<nav class="paginator" aria-labelledby="pagination">
    <h2 id="pagination" class="visually-hidden">{%raw%}{% blocktranslate with name=opts.verbose_name %}Pagination {{ name }} entries{% endblocktranslate %}{%endraw%}</h2>
    <!-- Pagination content... -->
</nav>

<!-- Using title and aria-label attributes to provide full text content to all users -->
<!-- despite visual truncation for layout purposes -->
<a href="..." title="{{ object|to_object_display_value }}" aria-label="{{ object|to_object_display_value }}">
  {{ object|to_object_display_value|truncatechars:"80" }}
</a>
```

This documentation practice helps maintain accessibility standards by explaining design choices, translation considerations, and how both visual and screen reader users will experience the interface.