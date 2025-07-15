---
title: Defense in depth
description: Always implement multiple layers of security controls, even when they
  might seem redundant. This strategy ensures protection remains effective even if
  one security measure fails or is bypassed.
repository: grafana/grafana
label: Security
language: TypeScript
comments_count: 2
repository_stars: 68825
---

Always implement multiple layers of security controls, even when they might seem redundant. This strategy ensures protection remains effective even if one security measure fails or is bypassed.

For external links:
```typescript
// Always add rel="noopener" to links with target="_blank"
DOMPurify.addHook('afterSanitizeAttributes', function (node) {
  if (node.tagName === 'A' && node.getAttribute('target') === '_blank') {
    const currentRel = node.getAttribute('rel') || '';
    const relValues = new Set(currentRel.split(/\s+/).filter(Boolean));
    relValues.add('noopener');
    // Apply even if browsers may handle this implicitly
  }
});
```

For input validation:
```typescript
// Be thorough when escaping special characters
function escapeInput(value: string): string {
  // Apply comprehensive escaping that covers all edge cases
  return typeof value === 'string' 
    ? value.replace(/\\/g, '\\\\\\\\').replace(/[$^*{}\[\]'+?.()|\/]/g, '\\$&') 
    : value;
}
```

This principle applies to all security contexts: authentication, authorization, input validation, and output encoding. By incorporating overlapping protections, you create a more robust security posture that doesn't rely on any single control being perfect.