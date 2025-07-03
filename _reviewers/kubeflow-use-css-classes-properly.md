---
title: Use CSS classes properly
description: Avoid inline styles and `!important` declarations in your HTML templates.
  Instead, define and use CSS classes that encapsulate styling needs. This improves
  code maintainability, readability, and reduces CSS specificity issues.
repository: kubeflow/kubeflow
label: Code Style
language: Html
comments_count: 2
repository_stars: 15064
---

Avoid inline styles and `!important` declarations in your HTML templates. Instead, define and use CSS classes that encapsulate styling needs. This improves code maintainability, readability, and reduces CSS specificity issues.

Bad example:
```html
<mat-icon style="height:72px !important; width:200px !important;" svgIcon="jupyterlab"></mat-icon>
```

Good example:
```html
<!-- In your HTML -->
<mat-icon class="server-type" svgIcon="jupyterlab"></mat-icon>

<!-- In your CSS -->
.server-type {
  height: 32px;
  width: 150px;
}

.server-type-wrapper {
  margin-bottom: 1rem;
}
```

This approach makes your styles more maintainable, easier to debug, and allows for better responsiveness. CSS classes can be reused across components and modified centrally rather than hunting through templates for inline styles.
