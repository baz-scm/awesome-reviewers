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


[
  {
    "discussion_id": "2143887259",
    "pr_number": 50587,
    "pr_file": "eng/common/pipelines/templates/steps/detect-api-changes.yml",
    "created_at": "2025-06-13T00:09:46+00:00",
    "commented_code": "Condition: true\n\nsteps:",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2143887259",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50587,
        "pr_file": "eng/common/pipelines/templates/steps/detect-api-changes.yml",
        "discussion_id": "2143887259",
        "commented_code": "@@ -5,24 +5,25 @@ parameters:\n   Condition: true\n \n steps:",
        "comment_created_at": "2025-06-13T00:09:46+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider adding an inline comment here to clarify that this conditional wrapper restricts the following steps to pull request builds only.\n```suggestion\nsteps:\n  # Restrict the following steps to pull request builds only\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2106854958",
    "pr_number": 50267,
    "pr_file": "sdk/mongodbatlas/Azure.ResourceManager.MongoDBAtlas/tsp-location.yaml",
    "created_at": "2025-05-26T08:44:05+00:00",
    "commented_code": "directory: specification/liftrmongodb/MongoDB.Atlas.Management\ncommit: 6a4f32353ce0eb59d33fd785a512cd487b81814f\nrepo: Azure/azure-rest-api-specs\nadditionalDirectories:",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2106854958",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50267,
        "pr_file": "sdk/mongodbatlas/Azure.ResourceManager.MongoDBAtlas/tsp-location.yaml",
        "discussion_id": "2106854958",
        "commented_code": "@@ -0,0 +1,4 @@\n+directory: specification/liftrmongodb/MongoDB.Atlas.Management\n+commit: 6a4f32353ce0eb59d33fd785a512cd487b81814f\n+repo: Azure/azure-rest-api-specs\n+additionalDirectories: ",
        "comment_created_at": "2025-05-26T08:44:05+00:00",
        "comment_author": "Copilot",
        "comment_body": "The 'additionalDirectories' property is left empty; please either remove it if not needed or add a comment/documentation to clarify its intended usage.",
        "pr_file_module": null
      }
    ]
  }
]
