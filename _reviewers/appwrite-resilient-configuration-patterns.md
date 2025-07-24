---
title: Resilient configuration patterns
description: When modifying or defining configuration values, use patterns that are
  resistant to future changes and silent failures. For configuration files, scripts,
  and environment variables, implement approaches that remain valid when underlying
  values change.
repository: appwrite/appwrite
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 51959
---

When modifying or defining configuration values, use patterns that are resistant to future changes and silent failures. For configuration files, scripts, and environment variables, implement approaches that remain valid when underlying values change.

For sed-based file modifications, target the configuration key rather than specific values:
```diff
-sed -i 's/_APP_BROWSER_HOST=http:\/\/appwrite-browser:3000\/v1/_APP_BROWSER_HOST=http:\/\/invalid-browser\/v1/' .env
+# Force an invalid browser host irrespective of its previous value
+sed -i 's|^_APP_BROWSER_HOST=.*|_APP_BROWSER_HOST=http://invalid-browser/v1|' .env
```

For environment variable names and values, ensure correct spelling and valid defaults:
```diff
-OPR_EXECUTOR_INACTIVE_TRESHOLD=$_APP_COMPUTE_INACTIVE_THRESHOLD
+OPR_EXECUTOR_INACTIVE_THRESHOLD=$_APP_COMPUTE_INACTIVE_THRESHOLD
```

```diff
if [ -z "$PLATFORM" ]; then
-  PLATFORM="console"
+  PLATFORM="client"  # Using a value from the defined options
fi
```

These practices prevent silent failures, ensure configuration changes work reliably across environments, and improve maintainability as projects evolve.