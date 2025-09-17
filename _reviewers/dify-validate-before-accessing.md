---
title: Validate before accessing
description: Always validate preconditions before performing operations that could
  throw runtime errors. This includes checking object property existence, verifying
  context validity, and ensuring required data is available before proceeding.
repository: langgenius/dify
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 114231
---

Always validate preconditions before performing operations that could throw runtime errors. This includes checking object property existence, verifying context validity, and ensuring required data is available before proceeding.

When validation fails, handle the situation gracefully rather than allowing the operation to throw. Options include:
- Providing user feedback or prompts when context is invalid
- Using conditional checks to prevent undefined property access
- Implementing fallback behavior for missing data

Example of defensive property access:
```javascript
// Instead of direct access that could throw:
created_at__after: dayjs().subtract(TIME_PERIOD_MAPPING[period].value, 'day')

// Add validation first:
...((period !== '9' && TIME_PERIOD_MAPPING[period])
  ? {
    created_at__after: dayjs().subtract(TIME_PERIOD_MAPPING[period].value, 'day')
  }
  : {})
```

This approach prevents runtime crashes and provides better user experience by handling edge cases proactively rather than reactively.