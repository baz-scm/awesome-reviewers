---
title: Standardize style scripts
description: Maintain consistent code style enforcement scripts across all projects
  by standardizing linting and formatting configurations in package.json. Use modern,
  supported tools instead of deprecated ones (like tslint).
repository: kubeflow/kubeflow
label: Code Style
language: Json
comments_count: 2
repository_stars: 15064
---

Maintain consistent code style enforcement scripts across all projects by standardizing linting and formatting configurations in package.json. Use modern, supported tools instead of deprecated ones (like tslint).

Every frontend project should include these standard scripts:

```json
{
  "scripts": {
    "lint-check": "ng lint",
    "lint": "ng lint --fix",
    "format:check": "prettier --check 'src/**/*.{js,ts,html,scss,css}' || node scripts/check-format-error.js"
  }
}
```

This approach ensures:
1. Consistent style enforcement across repositories
2. Both checking capabilities (`lint-check`, `format:check`) and auto-fixing options (`lint`)
3. Developer-friendly error messages when formatting fails
4. Alignment with established patterns in other repositories like Katib

When adding these scripts, make appropriate configurations in angular.json as needed to support them.
