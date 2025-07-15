---
title: "Balance constraints with flexibility"
description: "When designing APIs, carefully evaluate constraints imposed on consumers. Each limitation should serve a clear purpose; otherwise, favor flexibility. Instead of rigid enforcement, consider more adaptable interfaces with documentation about recommended usage patterns."
repository: "facebook/react"
label: "API"
language: "JavaScript"
comments_count: 4
repository_stars: 237000
---

When designing APIs, carefully evaluate constraints imposed on consumers. Each limitation should serve a clear purpose; otherwise, favor flexibility. Instead of rigid enforcement, consider more adaptable interfaces with documentation about recommended usage patterns.

For example, in discussion #4, an initial API design restricted objects to a single observer:

```js
if (this._observer !== null && this._observer !== observer) {
  throw new Error(
    'You are attaching an observer to a fragment instance that already has one. Fragment instances ' +
      'can only have one observer. Use multiple fragment instances or first call unobserveUsing() to ' +
      'remove the previous observer.',
  );
}
```

After review, this constraint was questioned: "What's the reason for this limitation?" The developer decided to "extend it to handle multiple and drop this error" since it "doesn't really take away anything to make it more flexible."

Similarly, in discussion #5, assumptions about mouse events were challenged with a suggestion to handle more edge cases:

```js
case 'mousedown': {
  if (((nativeEvent: any): MouseEvent).button === 0) {
    isMouseDown = true;
  }
  break;
}
case 'mouseup':
case 'dragend': {
  if (((nativeEvent: any): MouseEvent).button === 0) {
    isMouseDown = false;
  }
  break;
}
```

When designing APIs that must work across different versions or environments, use fallback patterns rather than rigid requirements. As seen in discussion #1, compatibility can be preserved with approaches like:

```js
const sourceCode = context.sourceCode ?? context.getSourceCode();
```

This approach enables your API to adapt to varying contexts while maintaining a consistent interface for consumers.