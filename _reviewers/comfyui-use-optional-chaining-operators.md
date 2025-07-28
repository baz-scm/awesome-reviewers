---
title: Use optional chaining operators
description: Use optional chaining (`?.`) and nullish coalescing (`??`) operators
  instead of manual null checks to safely access nested properties and provide fallback
  values. These operators prevent runtime errors when dealing with potentially null
  or undefined values and result in cleaner, more readable code.
repository: comfyanonymous/ComfyUI
label: Null Handling
language: JavaScript
comments_count: 2
repository_stars: 83726
---

Use optional chaining (`?.`) and nullish coalescing (`??`) operators instead of manual null checks to safely access nested properties and provide fallback values. These operators prevent runtime errors when dealing with potentially null or undefined values and result in cleaner, more readable code.

Instead of verbose manual checks:
```javascript
if (item.meta && item.meta[key] && item.meta[key].display_node) {
    app.nodeOutputs[item.meta[key].display_node] = value;
} else {
    app.nodeOutputs[key] = value;
}
```

Use optional chaining with nullish coalescing:
```javascript
const realKey = item?.meta?.[key]?.display_node ?? key;
app.nodeOutputs[realKey] = value;
```

For simple property access, replace potentially unsafe access like `input.widget.name` with `input.widget?.name` to handle cases where the parent object might be null or undefined. This approach reduces boilerplate code while providing robust null safety.