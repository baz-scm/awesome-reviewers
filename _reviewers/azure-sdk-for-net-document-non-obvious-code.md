---
title: Document non-obvious code
description: Add clarifying comments to code elements whose purpose or behavior may
  not be immediately apparent to other developers. This includes conditional logic
  blocks, empty configuration properties, and any code structures whose intent requires
  context to understand.
repository: Azure/azure-sdk-for-net
label: Documentation
language: Yaml
comments_count: 2
repository_stars: 5809
---

Add clarifying comments to code elements whose purpose or behavior may not be immediately apparent to other developers. This includes conditional logic blocks, empty configuration properties, and any code structures whose intent requires context to understand.

For conditional logic:
```yaml
steps:
  # Restrict the following steps to pull request builds only
  - task: PowerShell@2
    condition: eq(variables['Build.Reason'], 'PullRequest')
    # ... remainder of task
```

For configuration properties:
```yaml
directory: specification/liftrmongodb/MongoDB.Atlas.Management
commit: 6a4f32353ce0eb59d33fd785a512cd487b81814f
repo: Azure/azure-rest-api-specs
# Reserved for specifying additional specification directories if needed
additionalDirectories: 
```

Clear documentation reduces the cognitive load for reviewers and future maintainers, helping them understand the code's purpose without needing to infer it from implementation details.
