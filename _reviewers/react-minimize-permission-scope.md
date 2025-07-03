---
title: Minimize permission scope
description: Always follow the principle of least privilege when requesting permissions
  in browser extensions or any application. Request only the minimum permissions necessary
  for functionality to operate. Broad permissions like `"http://*/*"` and `"https://*/*"`
  significantly increase the security risk profile of your extension and should only
  be used when absolutely...
repository: facebook/react
label: Security
language: Json
comments_count: 1
repository_stars: 236926
---

Always follow the principle of least privilege when requesting permissions in browser extensions or any application. Request only the minimum permissions necessary for functionality to operate. Broad permissions like `"http://*/*"` and `"https://*/*"` significantly increase the security risk profile of your extension and should only be used when absolutely necessary.

For Chrome extensions using Manifest v3:
```json
"permissions": [
  "scripting",
  "storage",
  "tabs"
  // Avoid broad host permissions unless absolutely necessary
]
```

When broad permissions are truly required, document the specific reasoning directly in the code to justify the security trade-off. Consider alternatives such as:
1. Using more specific URL patterns that target only the domains you need
2. Leveraging optional permissions that can be requested at runtime
3. Using activeTab permission instead of broad host permissions where appropriate

If you must use broad permissions, be prepared to demonstrate why more limited permissions would not suffice during security review.