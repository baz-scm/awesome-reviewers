---
title: extract repeated expressions
description: When the same expression or computation appears multiple times within
  a code block, extract it to a variable to improve maintainability and readability.
  This reduces the risk of inconsistencies when the logic needs to be updated and
  makes the code's intent clearer.
repository: cloudflare/workerd
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 6989
---

When the same expression or computation appears multiple times within a code block, extract it to a variable to improve maintainability and readability. This reduces the risk of inconsistencies when the logic needs to be updated and makes the code's intent clearer.

Example:
```javascript
// Before - repeated computation
switch (event.event.type) {
  case 'spanOpen':
    spans.set(event.invocationId + event.spanId, { name: event.event.name });
    break;
  case 'attributes':
    let span = spans.get(event.invocationId + event.spanId);
    break;
}

// After - extract to variable
const spanKey = event.invocationId + event.spanId;
switch (event.event.type) {
  case 'spanOpen':
    spans.set(spanKey, { name: event.event.name });
    break;
  case 'attributes':
    let span = spans.get(spanKey);
    break;
}
```

This practice also applies to formatting consistency - use clear, readable formats like `10_000` instead of `10000` for large numbers to improve code readability.