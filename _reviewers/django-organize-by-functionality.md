---
title: Organize by functionality
description: Place code in files that match its functionality. When functionality
  applies to multiple components, use a general-purpose file rather than component-specific
  ones. This improves maintainability and makes the codebase easier to navigate.
repository: django/django
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 84182
---

Place code in files that match its functionality. When functionality applies to multiple components, use a general-purpose file rather than component-specific ones. This improves maintainability and makes the codebase easier to navigate.

For example, instead of:
```javascript
// In inlines.js
$('.js-inline-admin-formset fieldset.module.collapse:not(.open) details[open]').each(function() {
    this.removeAttribute('open');
});
```

Prefer:
```javascript
// In a more general file like change_form.js
document.querySelectorAll('fieldset.module.collapse:not(.open) details[open]').forEach(details => {
    details.removeAttribute('open');
});
```

Additionally, use modern JavaScript patterns where appropriate to improve code consistency and readability.