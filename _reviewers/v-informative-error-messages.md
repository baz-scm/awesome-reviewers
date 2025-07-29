---
title: informative error messages
description: Error messages should be specific, contextual, and include relevant information
  to aid debugging and user understanding. Avoid generic messages like "invalid syntax"
  in favor of descriptive explanations that specify what was expected, what was found,
  and include the problematic data when helpful.
repository: vlang/v
label: Error Handling
language: Other
comments_count: 7
repository_stars: 36582
---

Error messages should be specific, contextual, and include relevant information to aid debugging and user understanding. Avoid generic messages like "invalid syntax" in favor of descriptive explanations that specify what was expected, what was found, and include the problematic data when helpful.

Key practices:
- Include type information in error messages: `return error('Unsupported data type `${T}` to voidptr')` instead of `return error('Unsupport data type to voidptr')`
- Show both expected and actual values: `return type mismatch, it should be 'int', but it is instead 'string'` rather than just `return type mismatch, it should be 'int'`
- Provide specific context: `return error('strconv.atoi: parsing "${s}": values cannot start or end with underscores')` instead of `return error('strconv.atoi: parsing "${s}": invalid syntax')`
- Include problematic data in the message: `return error('number exceeds 64 digits: ${actual_number}')` to show what caused the issue

Example transformation:
```v
// Before: Generic and unhelpful
if ch > 9 {
    return error('strconv.atoi: parsing "${s}": invalid syntax')
}

// After: Specific and informative  
if ch > 9 {
    return error('strconv.atoi: parsing "${s}": character `${s[i]}` is not a valid digit')
}
```

This approach significantly improves the debugging experience and helps users understand exactly what went wrong and how to fix it.