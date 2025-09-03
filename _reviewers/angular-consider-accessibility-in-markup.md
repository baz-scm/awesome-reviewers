---
title: Consider accessibility in markup
description: When writing HTML markup, consider the accessibility implications of
  your formatting and structural choices. This includes avoiding text formatting that
  may negatively impact screen readers and ensuring proper semantic HTML usage.
repository: angular/angular
label: Code Style
language: Html
comments_count: 2
repository_stars: 98611
---

When writing HTML markup, consider the accessibility implications of your formatting and structural choices. This includes avoiding text formatting that may negatively impact screen readers and ensuring proper semantic HTML usage.

Key considerations:
- Avoid ALL CAPS text in content as screen readers may spell out each letter individually ("E-V-E-N" instead of "even")
- Use semantic HTML elements appropriately - for example, `nav` elements should contain navigation links, not standalone buttons
- Consider whether container elements serve a semantic purpose or if they can be simplified

Example of problematic markup:
```html
<nav>
  <button type="button" (click)="toggle()">Toggle Element</button>
</nav>
<div class="indicator">
  EVEN
</div>
```

Better approach:
```html
<button type="button" (click)="toggle()">Toggle Element</button>
<div class="indicator">
  Even
</div>
```

This ensures better screen reader compatibility and cleaner semantic structure while maintaining the same functionality.