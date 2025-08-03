---
title: Actionable error messages
description: 'When designing APIs, provide error messages that are contextually accurate,
  descriptive, and actionable. Generic error suggestions can confuse users when they
  don''t apply to the specific situation. Instead, tailor error responses to include:'
repository: microsoft/typescript
label: API
language: JavaScript
comments_count: 2
repository_stars: 105378
---

When designing APIs, provide error messages that are contextually accurate, descriptive, and actionable. Generic error suggestions can confuse users when they don't apply to the specific situation. Instead, tailor error responses to include:

1. The precise reason for the failure
2. Context-aware suggestions that are applicable to the specific error case
3. Clear steps for resolution when possible

For example, instead of a generic message like:
```
Could not find a declaration file for module 'bar'. Try `npm i --save-dev @types/bar` if it exists or add a new declaration (.d.ts) file containing `declare module 'bar';`
```

A more contextually aware message might be:
```
Could not find a declaration file for module 'bar' at '/path/to/bar.js'. This file is being treated as a JavaScript module. Consider one of the following:
- If this is your own module, add type definitions with a matching .d.ts file
- If using a third-party module, check if @types/bar exists and is compatible with your version
- If neither applies, verify the module path is correct
```

Error messages that adapt to the specific situation help API consumers resolve issues more efficiently and reduce support burden.