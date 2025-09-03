---
title: Respect browser behavior
description: Always consider and respect browser native behaviors when implementing
  web application features. Avoid conflicts with built-in browser shortcuts and choose
  appropriate client vs server-side approaches based on the execution environment.
repository: lobehub/lobe-chat
label: Networking
language: TSX
comments_count: 2
repository_stars: 65138
---

Always consider and respect browser native behaviors when implementing web application features. Avoid conflicts with built-in browser shortcuts and choose appropriate client vs server-side approaches based on the execution environment.

Key considerations:
- Don't override browser native shortcuts (like cmd+1 for tab switching) with application hotkeys
- Use client-side redirects when server-side redirects cause production issues
- Test cross-platform behavior differences (Windows vs Mac keyboard shortcuts)

Example from hotkey implementation:
```typescript
// Avoid: Using 'mod' which maps to 'cmd' on Mac, conflicting with browser tabs
useHotkeys(list.slice(0, 9).map((e, i) => `mod+${i + 1}`), handler);

// Prefer: Use 'ctrl' explicitly to avoid browser shortcut conflicts
useHotkeys(list.slice(0, 9).map((e, i) => `ctrl+${i + 1}`), handler);
```

Example from navigation:
```typescript
// Avoid: Server redirect that fails in production
return redirect(urlJoin('/settings', searchParams.tab));

// Prefer: Client-side redirect for better compatibility
// Use client-side navigation instead
```

This ensures better user experience by respecting established browser conventions and avoiding runtime errors in production environments.