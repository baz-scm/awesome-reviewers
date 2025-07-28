---
title: Optimize React hooks
description: Avoid unnecessary useCallback and useEffect dependencies to improve performance
  and code clarity. When event handlers are only used within a useEffect, define them
  locally inside the effect rather than using useCallback. This eliminates the need
  for the callback hook and reduces re-renders. Additionally, understand that refs
  don't need to be included in...
repository: mastodon/mastodon
label: React
language: JSX
comments_count: 2
repository_stars: 48691
---

Avoid unnecessary useCallback and useEffect dependencies to improve performance and code clarity. When event handlers are only used within a useEffect, define them locally inside the effect rather than using useCallback. This eliminates the need for the callback hook and reduces re-renders. Additionally, understand that refs don't need to be included in useEffect dependency arrays since they maintain stable references across renders.

Example of optimization:
```javascript
// Instead of this:
const handleDocumentClick = useCallback(() => {
  onClose();
}, [onClose]);

useEffect(() => {
  document.addEventListener('click', handleDocumentClick);
  return () => document.removeEventListener('click', handleDocumentClick);
}, [handleDocumentClick]);

// Do this:
useEffect(() => {
  const handleDocumentClick = () => {
    onClose();
  };
  
  document.addEventListener('click', handleDocumentClick);
  return () => document.removeEventListener('click', handleDocumentClick);
}, [onClose]); // refs like nodeRef don't need to be dependencies
```

This approach reduces unnecessary re-renders and makes the code more readable by keeping related logic together.