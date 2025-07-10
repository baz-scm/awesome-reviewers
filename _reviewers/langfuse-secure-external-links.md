---
title: Secure external links
description: Always add `rel="noopener noreferrer"` to external links that use `target="_blank"`
  to prevent tabnabbing attacks. This security attribute prevents malicious websites
  from gaining access to your window object through the opener property, which could
  be exploited for phishing attacks or other security breaches.
repository: langfuse/langfuse
label: Security
language: TSX
comments_count: 3
repository_stars: 13574
---

Always add `rel="noopener noreferrer"` to external links that use `target="_blank"` to prevent tabnabbing attacks. This security attribute prevents malicious websites from gaining access to your window object through the opener property, which could be exploited for phishing attacks or other security breaches.

Example:

```jsx
// Insecure: vulnerable to tabnabbing
<Link 
  href="https://langfuse.com/docs/analytics/posthog"
  target="_blank"
>
  Integration Docs ↗
</Link>

// Secure: protected against tabnabbing
<Link 
  href="https://langfuse.com/docs/analytics/posthog"
  target="_blank" 
  rel="noopener noreferrer"
>
  Integration Docs ↗
</Link>
```

This security measure should be applied consistently across all external links in the application, especially in components that render user-provided or dynamic URLs.