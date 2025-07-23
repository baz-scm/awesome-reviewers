---
title: Accessible security controls
description: Security controls and interactive elements must be accessible to all
  users to prevent unequal security access. When non-standard elements (like divs)
  are used for interaction, they must include proper accessibility attributes to ensure
  users with disabilities can access security features.
repository: continuedev/continue
label: Security
language: TSX
comments_count: 1
repository_stars: 27819
---

Security controls and interactive elements must be accessible to all users to prevent unequal security access. When non-standard elements (like divs) are used for interaction, they must include proper accessibility attributes to ensure users with disabilities can access security features.

For any clickable element:
1. Add role="button" for screen reader identification 
2. Include tabIndex="0" for keyboard focus
3. Implement keyboard event handlers (onKeyDown) for activation via keyboard

Code example (fixing the accessibility issue):

```tsx
return (
  <div
    role="button"
    tabIndex={0}
    onClick={handleClick}
    onKeyDown={(e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        handleClick();
      }
    }}
    className={`flex cursor-pointer items-center gap-1 ${className}`}
    onMouseEnter={() => setIsHovered(true)}
    onMouseLeave={() => setIsHovered(false)}
  >
    {renderIcon()}
    {children}
  </div>
);
```

This prevents security vulnerabilities for users who rely on assistive technologies by ensuring they have equal access to security-related controls and features.