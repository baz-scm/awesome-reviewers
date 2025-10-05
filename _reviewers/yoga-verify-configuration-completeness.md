---
title: verify configuration completeness
description: Always verify that configuration files completely and accurately specify
  their requirements. This includes ensuring all related files are included and using
  appropriate minimum versions or glob patterns.
repository: facebook/yoga
label: Configurations
language: Json
comments_count: 2
repository_stars: 18255
---

Always verify that configuration files completely and accurately specify their requirements. This includes ensuring all related files are included and using appropriate minimum versions or glob patterns.

For package configurations, use glob patterns to include all related files rather than listing them individually:
```json
"files": [
  "dist/binaries/**",
  "dist/src/**", 
  "src/**",
  "load.*"
]
```

For framework configurations, specify the minimum required version that supports your needs:
```json
"frameworks": {
  "netstandard1.1": {}
}
```

Before finalizing configuration changes, double-check that all necessary artifacts, dependencies, and version requirements are properly captured to avoid missing components or compatibility issues.