---
title: Prevent credential exposure
description: Ensure that sensitive authentication data such as API keys, tokens, passwords,
  and other credentials are never exposed in documentation, client-side code, logs,
  or configuration files. This includes both preventing accidental inclusion in documentation
  and implementing proper secure handling in application code.
repository: lobehub/lobe-chat
label: Security
language: TSX
comments_count: 1
repository_stars: 65138
---

Ensure that sensitive authentication data such as API keys, tokens, passwords, and other credentials are never exposed in documentation, client-side code, logs, or configuration files. This includes both preventing accidental inclusion in documentation and implementing proper secure handling in application code.

Key practices:
- Use secure input components (like FormPassword) for sensitive fields in forms
- Set appropriate autoComplete attributes ("new-password" for passwords, "username" for usernames)
- Review documentation and code comments to ensure no actual credentials are included
- Implement proper credential storage and transmission mechanisms
- Avoid logging or displaying sensitive authentication data

Example from authentication form:
```tsx
// Good: Using FormPassword for sensitive data
<FormPassword
  autoComplete="new-password"
  placeholder={t('comfyui.apiKey.placeholder')}
/>

// Good: Using FormPassword for passwords
<FormPassword
  autoComplete="new-password"
  placeholder={t('comfyui.password.placeholder')}
/>
```

This practice prevents credential theft, unauthorized access, and security breaches that can occur when sensitive authentication data is inadvertently exposed through various channels.