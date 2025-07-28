---
title: Never ignore errors silently
description: All errors must be explicitly handled through catching, logging, or user
  feedback. Silent error suppression makes debugging impossible and creates poor user
  experiences.
repository: google-gemini/gemini-cli
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 65062
---

All errors must be explicitly handled through catching, logging, or user feedback. Silent error suppression makes debugging impossible and creates poor user experiences.

**Always do one of the following:**
- Add `.catch()` handlers to promises to prevent unhandled rejections
- Log errors with appropriate detail (error.message for users, error.stack in debug mode)  
- Show error feedback to users even in minimal UI modes
- Set up global unhandled rejection handlers for critical failures

**Example of proper error handling:**
```javascript
// Bad: Silent failure
checkForUpdates().then((info) => {
  // handle success
});

// Good: Explicit error handling  
checkForUpdates().then((info) => {
  // handle success
}).catch((error) => {
  console.error('Update check failed:', error.message);
});

// Bad: Removing error logs
} catch (error) {
  // Ignore clipboard image errors
}

// Good: Maintain error visibility
} catch (error) {
  console.error('Error handling clipboard image:', error);
}
```

This ensures errors are visible to developers during debugging and users understand when operations fail, enabling proper troubleshooting and recovery.