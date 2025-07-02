---
title: Externalize configuration values
description: Store configuration values (URLs, demands, pool names) in centralized
  variables rather than hardcoding them inline. This improves maintainability, ensures
  consistency across the codebase, and simplifies future updates. When possible, group
  related configurations in dedicated template files or variable groups.
repository: Azure/azure-sdk-for-net
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 5809
---

Store configuration values (URLs, demands, pool names) in centralized variables rather than hardcoding them inline. This improves maintainability, ensures consistency across the codebase, and simplifies future updates. When possible, group related configurations in dedicated template files or variable groups.

Example:
```yaml
# Instead of:
pool:
  name: $(WINDOWSPOOL)
  demands: ImageOverride -equals $(WINDOWSVMIMAGE)

# Prefer:
pool:
  name: $(WINDOWSPOOL)
  demands: $(IMAGE_DEMAND)

variables:
  - name: IMAGE_DEMAND
    value: ImageOverride -equals $(WINDOWSVMIMAGE)
```

For API endpoints, pipeline definitions, and other configuration values that may change over time, always use variables rather than hardcoding values directly in scripts or pipeline definitions.


[
  {
    "discussion_id": "2162710383",
    "pr_number": 50802,
    "pr_file": "eng/pipelines/docindex.yml",
    "created_at": "2025-06-24T00:00:40+00:00",
    "commented_code": "- job: UpdateDocsMsBuildConfig\n    pool:\n      name: $(LINUXPOOL)\n      demands: $(LinuxImageDemand)\n      demands: ImageOverride -equals $(LINUXVMIMAGE)",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2162710383",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50802,
        "pr_file": "eng/pipelines/docindex.yml",
        "discussion_id": "2162710383",
        "commented_code": "@@ -34,7 +34,7 @@ jobs:\n   - job: UpdateDocsMsBuildConfig\n     pool:\n       name: $(LINUXPOOL)\n-      demands: $(LinuxImageDemand)\n+      demands: ImageOverride -equals $(LINUXVMIMAGE)",
        "comment_created_at": "2025-06-24T00:00:40+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider centralizing the inline image demand expression in a shared variable to improve consistency and ease future maintenance.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2162710385",
    "pr_number": 50802,
    "pr_file": "eng/pipelines/aggregate-reports.yml",
    "created_at": "2025-06-24T00:00:41+00:00",
    "commented_code": "pool:\n  name: $(WINDOWSPOOL)\n  demands: $(WindowsImageDemand)\n  demands: ImageOverride -equals $(WINDOWSVMIMAGE)\n\nvariables:",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2162710385",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50802,
        "pr_file": "eng/pipelines/aggregate-reports.yml",
        "discussion_id": "2162710385",
        "commented_code": "@@ -11,7 +11,7 @@ pr:\n \n pool:\n   name: $(WINDOWSPOOL)\n-  demands: $(WindowsImageDemand)\n+  demands: ImageOverride -equals $(WINDOWSVMIMAGE)\n \n variables:",
        "comment_created_at": "2025-06-24T00:00:41+00:00",
        "comment_author": "Copilot",
        "comment_body": "Consider centralizing the inline image demand expression in a shared variable to improve consistency and ease future maintenance.\n```suggestion\n  demands: $(IMAGE_DEMAND)\n\nvariables:\n  - name: IMAGE_DEMAND\n    value: ImageOverride -equals $(WINDOWSVMIMAGE)\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2113092739",
    "pr_number": 50316,
    "pr_file": "eng/common/pipelines/templates/steps/detect-api-changes.yml",
    "created_at": "2025-05-29T03:12:50+00:00",
    "commented_code": "steps:\n  - pwsh: |\n      $apiChangeDetectRequestUrl = \"https://apiview.dev/PullRequest/DetectApiChanges\"\n      $apiChangeDetectRequestUrl = \"https://apiview.dev/api/PullRequests/CreateAPIRevisionIfAPIHasChanges\"",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2113092739",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50316,
        "pr_file": "eng/common/pipelines/templates/steps/detect-api-changes.yml",
        "discussion_id": "2113092739",
        "commented_code": "@@ -6,7 +6,7 @@ parameters:\n \n steps:\n   - pwsh: |\n-      $apiChangeDetectRequestUrl = \"https://apiview.dev/PullRequest/DetectApiChanges\"\n+      $apiChangeDetectRequestUrl = \"https://apiview.dev/api/PullRequests/CreateAPIRevisionIfAPIHasChanges\"",
        "comment_created_at": "2025-05-29T03:12:50+00:00",
        "comment_author": "Copilot",
        "comment_body": "It may be beneficial to extract this hardcoded URL into a pipeline variable group or template parameter to ensure consistency and simplify future updates.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2103307241",
    "pr_number": 50221,
    "pr_file": "eng/pipelines/docindex.yml",
    "created_at": "2025-05-22T19:58:29+00:00",
    "commented_code": "- job: UpdateDocsMsBuildConfig\n    pool:\n      name: $(LINUXPOOL)\n      name: azsdk-pool",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2103307241",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50221,
        "pr_file": "eng/pipelines/docindex.yml",
        "discussion_id": "2103307241",
        "commented_code": "@@ -33,7 +33,8 @@ jobs:\n \n   - job: UpdateDocsMsBuildConfig\n     pool:\n-      name: $(LINUXPOOL)\n+      name: azsdk-pool",
        "comment_created_at": "2025-05-22T19:58:29+00:00",
        "comment_author": "weshaggard",
        "comment_body": "Why not use the variables? It might also be interesting to add the demand to the image.yml variables. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2103738606",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50221,
        "pr_file": "eng/pipelines/docindex.yml",
        "discussion_id": "2103307241",
        "commented_code": "@@ -33,7 +33,8 @@ jobs:\n \n   - job: UpdateDocsMsBuildConfig\n     pool:\n-      name: $(LINUXPOOL)\n+      name: azsdk-pool",
        "comment_created_at": "2025-05-23T03:52:28+00:00",
        "comment_author": "danieljurek",
        "comment_body": "Tested and the demand can be placed in a variable and it can reference variables (when the values are defined before job run time). ",
        "pr_file_module": null
      }
    ]
  }
]
