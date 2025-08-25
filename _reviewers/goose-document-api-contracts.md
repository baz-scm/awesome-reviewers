---
title: Document API contracts
description: Ensure all API interfaces have clearly documented contracts specifying
  expected request/response formats, data encoding standards, and return types. This
  prevents integration issues and enables reliable external consumption.
repository: block/goose
label: API
language: TSX
comments_count: 2
repository_stars: 19037
---

Ensure all API interfaces have clearly documented contracts specifying expected request/response formats, data encoding standards, and return types. This prevents integration issues and enables reliable external consumption.

When designing callback functions or data exchange formats, explicitly document:
- Expected response structure and types
- Data encoding methods (e.g., base64 variants, URL encoding)
- Backwards compatibility requirements

Example from callback responses:
```typescript
const handleUIAction = useCallback(async (result: UIActionResult) => {
  // Process the action...
  
  // IMPORTANT: Always return documented response format
  const response = {
    type: 'ui-message-response',
    payload: result,
  };
  return response;
}, []);
```

Consider adding TypeScript interfaces or runtime validation to enforce documented contracts. For data formats like deeplinks, establish official standards (e.g., "use URL_SAFE_NO_PAD base64") and implement backwards-compatible decoding to handle legacy formats during transitions.