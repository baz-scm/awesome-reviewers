---
title: "Verify workflow configuration integrity"
description: "Carefully review GitHub Actions workflow configurations to prevent subtle errors that can cause CI/CD pipeline failures or unexpected behavior."
repository: "vercel/next.js"
label: "CI/CD"
language: "Yaml"
comments_count: 3
repository_stars: 133000
---

Carefully review GitHub Actions workflow configurations to prevent subtle errors that can cause CI/CD pipeline failures or unexpected behavior:

1. Ensure correct syntax in workflow triggers, especially avoiding nested quotes in branch names:
```yaml
# Incorrect
branches:
  - '"canary"'
  
# Correct
branches:
  - "canary"
```

2. Always provide explicit IDs for steps that will be referenced by subsequent steps:
```yaml
# Missing ID that will cause reference failure
- name: 'Deploy to Cloud Run'
  uses: 'google-github-actions/deploy-cloudrun@v2'
  
# Correct with ID
- name: 'Deploy to Cloud Run'
  id: deploy
  uses: 'google-github-actions/deploy-cloudrun@v2'
```

3. Use appropriate conditions for workflow execution, considering job skip scenarios:
```yaml
# May cause issues when dependency is skipped
if: ${{ always() && needs.deploy-target.outputs.value != '' }}

# More robust handling of skipped jobs
if: ${{ always() && needs.deploy-target.result != 'skipped' }}
```