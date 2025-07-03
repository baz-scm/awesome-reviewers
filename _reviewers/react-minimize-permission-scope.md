---
title: Minimize permission scope
description: Always follow the principle of least privilege by requesting only the
  minimum permissions necessary for your application to function. Overly broad permissions
  increase security risks and potential attack surfaces. When working with browser
  extensions, APIs, or any system requiring explicit permissions, regularly review
  and restrict access scopes.
repository: facebook/react
label: Security
language: Json
comments_count: 1
repository_stars: 236925
---

Always follow the principle of least privilege by requesting only the minimum permissions necessary for your application to function. Overly broad permissions increase security risks and potential attack surfaces. When working with browser extensions, APIs, or any system requiring explicit permissions, regularly review and restrict access scopes.

For example, instead of broad URL patterns like:
```json
"permissions": [
  "http://*/*",
  "https://*/*"
]
```

Consider using more targeted permissions:
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

For Manifest V3 extensions, evaluate whether you can use alternatives like activeTab, declarativeNetRequest, or specific host permissions to achieve the same functionality without requesting broad access to all websites.