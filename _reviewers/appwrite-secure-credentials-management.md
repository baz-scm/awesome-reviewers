---
title: Secure credentials management
description: Never store sensitive credentials (passwords, API keys, tokens, etc.)
  in plain text within code repositories. This practice poses a significant security
  risk as it can lead to unauthorized access if the repository is compromised or accidentally
  made public.
repository: appwrite/appwrite
label: Security
language: Other
comments_count: 1
repository_stars: 51959
---

Never store sensitive credentials (passwords, API keys, tokens, etc.) in plain text within code repositories. This practice poses a significant security risk as it can lead to unauthorized access if the repository is compromised or accidentally made public.

Instead:
1. Use environment-specific configuration files that are excluded from version control
2. Implement secrets management tools or services
3. Use environment variables for runtime injection of sensitive values
4. Include commented placeholder examples in configuration templates

Example of good practice:
```diff
-DOCKERHUB_PULL_USERNAME=actual_username
-DOCKERHUB_PULL_PASSWORD=actual_password
-DOCKERHUB_PULL_EMAIL=actual_email@example.com
+# DOCKERHUB_PULL_USERNAME=your_username
+# DOCKERHUB_PULL_PASSWORD=your_password  
+# DOCKERHUB_PULL_EMAIL=your_email
```

Make sure to add these sensitive files to your .gitignore file and document the required environment variables in your project documentation.