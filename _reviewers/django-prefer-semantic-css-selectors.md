---
title: Prefer semantic CSS selectors
description: Use semantic attribute-based selectors instead of structural or overly
  specific class names when the semantic meaning is already captured in HTML attributes.
  This makes CSS more maintainable by connecting styles to the actual meaning of elements
  rather than their position in the DOM.
repository: django/django
label: Code Style
language: Css
comments_count: 3
repository_stars: 84182
---

Use semantic attribute-based selectors instead of structural or overly specific class names when the semantic meaning is already captured in HTML attributes. This makes CSS more maintainable by connecting styles to the actual meaning of elements rather than their position in the DOM.

For example, instead of:
```css
.paginator .this-page {
    padding: 2px 6px;
}

/* or */

ol.breadcrumbs li:last-child a {
    color: var(--breadcrumbs-fg);
    text-decoration: none !important;
    cursor: default;
}
```

Prefer:
```css
.paginator a[aria-current="page"] {
    padding: 2px 6px;
}
```

Also, ensure interactive elements have complete selector sets that include all relevant states:
```css
.datetimeshortcuts button:hover, .datetimeshortcuts button:focus {
    /* styles */
}
```

This approach improves code maintainability, better communicates intent, and naturally supports accessibility by leveraging semantic HTML attributes.