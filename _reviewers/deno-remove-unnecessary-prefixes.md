---
title: remove unnecessary prefixes
description: Remove vendor prefixes from CSS properties that have achieved sufficient
  browser support across modern browsers. Before removing prefixes, verify browser
  compatibility using resources like MDN documentation to ensure the unprefixed property
  is well-supported.
repository: denoland/deno
label: Code Style
language: Css
comments_count: 2
repository_stars: 103714
---

Remove vendor prefixes from CSS properties that have achieved sufficient browser support across modern browsers. Before removing prefixes, verify browser compatibility using resources like MDN documentation to ensure the unprefixed property is well-supported.

This practice improves code readability, reduces maintenance overhead, and eliminates redundant code. Focus on commonly supported properties that no longer require vendor-specific implementations.

Example cleanup:
```css
/* Before - unnecessary prefixes */
*:before {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

pre {
  -moz-tab-size: 2;
  -o-tab-size: 2;
  tab-size: 2;
}

/* After - clean, modern CSS */
*:before {
  box-sizing: border-box;
}

pre {
  tab-size: 2;
}
```