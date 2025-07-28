---
title: CSS comment standards
description: Always use proper CSS comment syntax (`/* */`) instead of inline comments
  (`//`) for better cross-browser compatibility and code consistency. Additionally,
  rely on autoprefixer configuration for vendor prefixes rather than manually adding
  them, which reduces code duplication and maintenance overhead.
repository: logseq/logseq
label: Code Style
language: Css
comments_count: 2
repository_stars: 37695
---

Always use proper CSS comment syntax (`/* */`) instead of inline comments (`//`) for better cross-browser compatibility and code consistency. Additionally, rely on autoprefixer configuration for vendor prefixes rather than manually adding them, which reduces code duplication and maintenance overhead.

Example of proper CSS commenting:
```css
/* Good: Proper CSS comment syntax */
right: 10px; /* Allows clicking on the scrollbar */

/* Avoid: Inline comment syntax */
right: 10px; // Allows clicking on the scrollbar
```

For vendor prefixes, configure autoprefixer at the project level instead of manually adding prefixes:
```css
/* Good: Let autoprefixer handle this */
user-select: none;

/* Avoid: Manual vendor prefixes when autoprefixer is available */
-webkit-user-select: none;
-khtml-user-select: none;
-moz-user-select: none;
-ms-user-select: none;
user-select: none;
```

This approach ensures consistent formatting, reduces maintenance burden, and leverages build tools effectively for better code organization.