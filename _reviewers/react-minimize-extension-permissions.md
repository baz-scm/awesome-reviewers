---
title: Minimize extension permissions
description: 'When developing browser extensions, always follow the principle of least
  privilege by requesting only the minimum permissions necessary for functionality.
  Broad permissions like `http://*/*` and `https://*/*` increase the security surface
  area and potential vulnerability of your extension. '
repository: facebook/react
label: Security
language: Json
comments_count: 1
repository_stars: 236852
---

When developing browser extensions, always follow the principle of least privilege by requesting only the minimum permissions necessary for functionality. Broad permissions like `http://*/*` and `https://*/*` increase the security surface area and potential vulnerability of your extension. 

Instead of:
```json
"permissions": [
  "scripting",
  "storage",
  "tabs",
  "http://*/*",
  "https://*/*"
]
```

Consider more targeted approaches:
```json
"permissions": [
  "scripting",
  "storage",
  "tabs"
],
"host_permissions": [
  "https://specific-domain.com/*"
]
```

Or use the `activeTab` permission when possible, which grants temporary access only when the user invokes your extension. For Manifest v3 extensions, evaluate if broad host permissions can be replaced with more specific declarativeNetRequest rules or host_permissions that target only the domains your extension needs to function.

## Discussions

## packages/react-devtools-extensions/chrome/manifest.json, https://github.com/facebook/react/pull/32471

@@ -43,7 +43,9 @@
   "permissions": [
     "scripting",
     "storage",
-    "tabs"
+    "tabs",
+    "http://*/*",
+    "https://*/*"

### hoxyq

Since we are using Manifest v3, I don't think these are required

### mrunsung7

We included those  because the devtools script needs broad access to interact with any possible user page, especially for debugging across different environments. That said, if this can be scoped down without losing functionality, I’m happy to revisit this! Let me know if there’s a more limited approach you’d prefer.

