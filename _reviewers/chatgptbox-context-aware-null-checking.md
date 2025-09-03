---
title: Context-aware null checking
description: Choose null checking patterns based on your function's purpose and intended
  behavior with empty values. For functions with fallback strategies, consider whether
  empty strings should trigger alternative methods or be treated as valid results.
repository: ChatGPTBox-dev/chatGPTBox
label: Null Handling
language: Other
comments_count: 2
repository_stars: 10660
---

Choose null checking patterns based on your function's purpose and intended behavior with empty values. For functions with fallback strategies, consider whether empty strings should trigger alternative methods or be treated as valid results.

Use `if (value?.property)` when empty strings should be treated as falsy and trigger fallback logic:
```javascript
// Content extraction with fallbacks
if (article?.textContent) {
  return postProcessText(article.textContent)
}
// Falls through to try other extraction methods
```

Use `if (value?.property != null)` when you need to distinguish null/undefined from empty strings:
```javascript
// When empty string is a valid result
if (article?.textContent != null) {
  return article.textContent // Returns empty string if that's what was parsed
}
```

Consider the downstream impact: will your function benefit from attempting alternative strategies when the primary method yields empty content, or should empty results be preserved and returned immediately?