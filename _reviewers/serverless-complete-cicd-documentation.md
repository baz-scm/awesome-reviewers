---
title: Complete CI/CD documentation
description: Ensure all CI/CD documentation is comprehensive and technically accurate,
  covering complete workflows and tooling capabilities. Incomplete or incorrect documentation
  leads to deployment failures, misconfigurations, and developer confusion.
repository: serverless/serverless
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 46810
---

Ensure all CI/CD documentation is comprehensive and technically accurate, covering complete workflows and tooling capabilities. Incomplete or incorrect documentation leads to deployment failures, misconfigurations, and developer confusion.

Documentation should include:
- All deployment scenarios (initial deployment, rollbacks, parameter retrieval)
- Accurate build tool configurations and supported formats
- Complete feature coverage without assumptions

For example, when documenting deployment buckets, include all use cases:
```markdown
# Deployment Bucket
Storage for Lambda code, CloudFormation templates, and other resources 
required for service deployment, service rollback, and efficient parameter retrieval.
```

When documenting build configurations, verify technical accuracy:
```markdown
**Note:** Build output format can be configured for both CommonJS and ESM. 
See esbuild documentation for format options.
```

This prevents developers from making incorrect assumptions that could cause deployment issues or require workarounds.