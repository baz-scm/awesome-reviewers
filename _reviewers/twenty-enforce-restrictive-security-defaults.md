---
title: Enforce restrictive security defaults
description: Always start with the most restrictive security settings and only grant
  additional permissions when absolutely necessary. This principle applies to user
  authorization, iframe sandboxing, API access, and any security-sensitive features.
repository: twentyhq/twenty
label: Security
language: TSX
comments_count: 2
repository_stars: 35477
---

Always start with the most restrictive security settings and only grant additional permissions when absolutely necessary. This principle applies to user authorization, iframe sandboxing, API access, and any security-sensitive features.

For user permissions, implement proper hierarchy validation rather than simple boolean checks. Users should only be able to perform actions on resources at their permission level or below.

For iframe embedding, use minimal sandbox attributes and allow policies:
```typescript
// Restrictive approach - only grant necessary permissions
<iframe
  sandbox="allow-scripts allow-forms allow-popups"
  allow="encrypted-media"
  allowFullScreen
/>

// Avoid overly permissive settings
<iframe
  sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
/>
```

This approach reduces attack surface, prevents privilege escalation, and follows security best practices by defaulting to deny rather than allow.