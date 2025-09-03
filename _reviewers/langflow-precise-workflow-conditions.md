---
title: precise workflow conditions
description: When implementing conditional logic in CI workflows, ensure boolean expressions
  are precise and comprehensive to avoid unintended workflow execution or bypassing.
  Use multiple filter conditions combined with logical operators to create accurate
  triggers based on file changes.
repository: langflow-ai/langflow
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 111046
---

When implementing conditional logic in CI workflows, ensure boolean expressions are precise and comprehensive to avoid unintended workflow execution or bypassing. Use multiple filter conditions combined with logical operators to create accurate triggers based on file changes.

For example, when creating a docs-only bypass condition, verify that documentation files changed AND no code files changed:

```yaml
docs-only: ${{ steps.filter.outputs.docs == 'true' && steps.filter.outputs.python != 'true' && steps.filter.outputs.frontend != 'true' }}
```

Then use this condition in workflow steps:
```yaml
elif [[ "${{ needs.check-nightly-status.outputs.should-proceed }}" != "true" && "${{ github.event_name }}" != "workflow_dispatch" && "$DOCS_ONLY" != "true" ]]; then
```

This prevents workflows from running unnecessarily on documentation-only changes while ensuring they still execute for any code modifications. Always test conditional logic thoroughly to ensure workflows behave as expected across different change scenarios.