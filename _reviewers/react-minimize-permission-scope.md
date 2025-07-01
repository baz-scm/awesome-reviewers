---
title: Minimize permission scope
description: Always apply the principle of least privilege by requesting only the
  minimum permissions necessary for your application to function. Overly broad permissions
  increase the attack surface and potential security risks. Regularly review permission
  requests to ensure they are appropriately scoped.
repository: facebook/react
label: Security
language: Json
comments_count: 1
repository_stars: 236861
---

Always apply the principle of least privilege by requesting only the minimum permissions necessary for your application to function. Overly broad permissions increase the attack surface and potential security risks. Regularly review permission requests to ensure they are appropriately scoped.

For example, instead of using broad URL patterns in browser extensions:
```
"permissions": [
  "http://*/*",
  "https://*/*"
]
```

Consider more specific permissions or use the `host_permissions` field with only the domains you need:
```
"host_permissions": [
  "https://specific-domain.com/*"
]
```

When adding new permissions, document the specific functionality that requires them and consider if there are alternatives that would require fewer privileges. During code reviews, challenge broad permission requests and evaluate if they can be further limited.


[
  {
    "discussion_id": "1977288088",
    "pr_number": 32471,
    "pr_file": "packages/react-devtools-extensions/chrome/manifest.json",
    "created_at": "2025-03-03T10:43:53+00:00",
    "commented_code": "\"permissions\": [\n    \"scripting\",\n    \"storage\",\n    \"tabs\"\n    \"tabs\",\n    \"http://*/*\",\n    \"https://*/*\"",
    "repo_full_name": "facebook/react",
    "discussion_comments": [
      {
        "comment_id": "1977288088",
        "repo_full_name": "facebook/react",
        "pr_number": 32471,
        "pr_file": "packages/react-devtools-extensions/chrome/manifest.json",
        "discussion_id": "1977288088",
        "commented_code": "@@ -43,7 +43,9 @@\n   \"permissions\": [\n     \"scripting\",\n     \"storage\",\n-    \"tabs\"\n+    \"tabs\",\n+    \"http://*/*\",\n+    \"https://*/*\"",
        "comment_created_at": "2025-03-03T10:43:53+00:00",
        "comment_author": "hoxyq",
        "comment_body": "Since we are using Manifest v3, I don't think these are required",
        "pr_file_module": null
      },
      {
        "comment_id": "1977373931",
        "repo_full_name": "facebook/react",
        "pr_number": 32471,
        "pr_file": "packages/react-devtools-extensions/chrome/manifest.json",
        "discussion_id": "1977288088",
        "commented_code": "@@ -43,7 +43,9 @@\n   \"permissions\": [\n     \"scripting\",\n     \"storage\",\n-    \"tabs\"\n+    \"tabs\",\n+    \"http://*/*\",\n+    \"https://*/*\"",
        "comment_created_at": "2025-03-03T11:49:24+00:00",
        "comment_author": "mrunsung7",
        "comment_body": "We included those  because the devtools script needs broad access to interact with any possible user page, especially for debugging across different environments. That said, if this can be scoped down without losing functionality, I\u2019m happy to revisit this! Let me know if there\u2019s a more limited approach you\u2019d prefer.",
        "pr_file_module": null
      }
    ]
  }
]
