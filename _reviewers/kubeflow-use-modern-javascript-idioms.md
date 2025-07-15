---
title: Use modern JavaScript idioms
description: 'Favor modern JavaScript syntax and clean code practices to improve readability
  and maintainability. This includes:


  1. **Use template literals** instead of string concatenation for clearer string
  interpolation:'
repository: kubeflow/kubeflow
label: Code Style
language: JavaScript
comments_count: 5
repository_stars: 15064
---

Favor modern JavaScript syntax and clean code practices to improve readability and maintainability. This includes:

1. **Use template literals** instead of string concatenation for clearer string interpolation:
```javascript
// Preferred
window.open(`/${namespace}/${notebook}`, "_blank");

// Avoid
window.open("/" + namespace + "/" + notebook, "_blank");
```

2. **Apply object destructuring** to reduce repetition and improve readability:
```javascript
// Preferred
const {contentDocument} = iframe;
contentDocument.addEventListener('click', handleEvent);

// Avoid
iframe.contentDocument.addEventListener('click', handleEvent);
```

3. **Flatten nested conditionals** when possible to reduce complexity:
```javascript
// Preferred
if (!queryParams || !queryParams["ns"]) {
  return this.buildHref(href, this.queryParams);
}
return this.buildHref(href.replace('{ns}', queryParams["ns"]), queryParams);

// Avoid
if (queryParams) {
  if (queryParams["ns"]) {
    if (queryParams["ns"] !== null) {
      // ...
    }
  }
}
```

4. **Remove unused code** including imports, commented-out code, and debug logging statements:
```javascript
// Remove before committing
console.log({own: (owned||[]).namespace, namespaces, ns: this.selected});
```

Maintaining these practices will lead to more consistent, readable, and maintainable code across the codebase.
