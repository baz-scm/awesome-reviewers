---
title: Handle errors explicitly
description: Always provide explicit error handling instead of allowing silent failures
  or blank screens. Any place where an error can occur but is not handled explicitly
  is a bug. When errors occur, communicate clearly to users what went wrong and suggest
  recovery actions when possible.
repository: microsoft/playwright
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 76113
---

Always provide explicit error handling instead of allowing silent failures or blank screens. Any place where an error can occur but is not handled explicitly is a bug. When errors occur, communicate clearly to users what went wrong and suggest recovery actions when possible.

Example of problematic silent failure:
```tsx
{!!report && <TestCaseViewLoader report={report} tests={filteredTests.tests} />}
```

Better approach with explicit error handling:
```tsx
{!!report ? 
  <TestCaseViewLoader report={report} tests={filteredTests.tests} /> :
  <div className='error'>Report data could not be found</div>}
```

Even better with recovery guidance:
```tsx
{!!report ? 
  <TestCaseViewLoader report={report} tests={filteredTests.tests} /> :
  <div className='error'>
    Report data could not be found. Try refreshing the page or check your connection.
  </div>}
```

This principle ensures users understand when something has gone wrong rather than being left with confusing blank screens or unresponsive interfaces.