---
title: Add interactive element roles
description: When adding event handlers like `onClick` to non-interactive elements
  such as `div`, always include appropriate ARIA roles and keyboard event handlers.
  This prevents accessibility issues and reduces security vulnerabilities by ensuring
  all interactive elements are properly identified and managed.
repository: shadcn-ui/ui
label: Security
language: TSX
comments_count: 1
repository_stars: 90568
---

When adding event handlers like `onClick` to non-interactive elements such as `div`, always include appropriate ARIA roles and keyboard event handlers. This prevents accessibility issues and reduces security vulnerabilities by ensuring all interactive elements are properly identified and managed.

Non-interactive elements with click handlers but without proper roles can be overlooked in security audits and create potential attack vectors through inconsistent input validation.

**Bad:**
```jsx
<div 
  className="stepper__vertical-step"
  onClick={() => handleStepClick(index)}
>
  {content}
</div>
```

**Good:**
```jsx
<div 
  className="stepper__vertical-step"
  role="button"
  tabIndex={0}
  onClick={() => handleStepClick(index)}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleStepClick(index);
    }
  }}
>
  {content}
</div>
```

Better yet, use a semantic element when possible:
```jsx
<button 
  className="stepper__vertical-step"
  onClick={() => handleStepClick(index)}
>
  {content}
</button>
```

This approach ensures both accessibility compliance and proper security by ensuring all interactive elements are consistently implemented and validated.