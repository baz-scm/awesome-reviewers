---
title: validate input rigorously
description: Always validate and sanitize input data against established standards
  to prevent injection attacks and ensure consistent behavior. This includes validating
  ARIA attributes according to W3C specifications and encoding potentially dangerous
  content in CSS or HTML contexts.
repository: microsoft/playwright
label: Security
language: TypeScript
comments_count: 2
repository_stars: 76113
---

Always validate and sanitize input data against established standards to prevent injection attacks and ensure consistent behavior. This includes validating ARIA attributes according to W3C specifications and encoding potentially dangerous content in CSS or HTML contexts.

For ARIA attributes, ensure they follow W3C standards - aria-disabled should only apply to elements with suitable roles as defined in the specification. For CSS content, encode URLs that could break HTML parsing:

```typescript
// Validate ARIA attributes against standards
if (isAncestor || kAriaDisabledRoles.includes(getAriaRole(element) || '')) {
  // Only apply aria-disabled to elements with suitable roles
}

// Encode dangerous CSS URLs to prevent HTML injection
function escapeURLsInStyleSheet(text: string): string {
  const replacer = (match: string, url: string) => {
    // Conservatively encode only urls with a closing tag
    if (url.includes('</')) {
      return `url('${encodeURIComponent(url)}')`;
    }
    return match;
  };
  return text.replace(urlToEscapeRegex, replacer);
}
```

This prevents both accessibility bypasses and XSS attacks through malformed input that doesn't conform to expected standards.