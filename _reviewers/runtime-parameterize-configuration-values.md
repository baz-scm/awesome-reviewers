---
title: Parameterize configuration values
description: Extract hard-coded configuration values into variables, parameters, or
  templates to improve reusability and simplify maintenance. When the same value is
  used in multiple places or might need to change in the future, define it once and
  reference it throughout your configuration files.
repository: dotnet/runtime
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 16578
---

Extract hard-coded configuration values into variables, parameters, or templates to improve reusability and simplify maintenance. When the same value is used in multiple places or might need to change in the future, define it once and reference it throughout your configuration files.

Examples:
1. For build scripts with multiple parameters:
```yaml
# Instead of:
- script: make run TARGET_ARCH=arm64 DEPLOY_AND_RUN=false RUNTIME_FLAVOR=CoreCLR STATIC_LINKING=true

# Use:
- script: make run TARGET_ARCH=${{ parameters.targetArch }} DEPLOY_AND_RUN=${{ parameters.deployAndRun }} RUNTIME_FLAVOR=${{ parameters.runtimeFlavor }} STATIC_LINKING=${{ parameters.staticLinking }}
```

2. For repeated configuration values:
```yaml
# Define once:
variables:
  timeoutPerTestCollection: 180

# Reference where needed:
jobParameters:
  timeoutInMinutes: ${{ variables.timeoutPerTestCollection }}
```

This practice reduces duplication, centralizes configuration management, and makes future updates more efficient and less error-prone.


[
  {
    "discussion_id": "2113837584",
    "pr_number": 116093,
    "pr_file": "eng/pipelines/performance/templates/build-perf-sample-apps.yml",
    "created_at": "2025-05-29T12:24:08+00:00",
    "commented_code": "workingDirectory: $(Build.SourcesDirectory)/artifacts/bin\n        displayName: clean bindir\n\n      # CoreCLR JIT static linking build\n      - script: make run TARGET_ARCH=arm64 DEPLOY_AND_RUN=false RUNTIME_FLAVOR=CoreCLR STATIC_LINKING=true",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2113837584",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116093,
        "pr_file": "eng/pipelines/performance/templates/build-perf-sample-apps.yml",
        "discussion_id": "2113837584",
        "commented_code": "@@ -78,6 +78,29 @@ steps:\n         workingDirectory: $(Build.SourcesDirectory)/artifacts/bin\n         displayName: clean bindir\n \n+      # CoreCLR JIT static linking build\n+      - script: make run TARGET_ARCH=arm64 DEPLOY_AND_RUN=false RUNTIME_FLAVOR=CoreCLR STATIC_LINKING=true",
        "comment_created_at": "2025-05-29T12:24:08+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider externalizing build configuration options (such as TARGET_ARCH, RUNTIME_FLAVOR, and STATIC_LINKING) into variables or a template to improve reusability and clarity for similar build steps.\n```suggestion\n      - script: make run TARGET_ARCH=${{ parameters.targetArch }} DEPLOY_AND_RUN=${{ parameters.deployAndRun }} RUNTIME_FLAVOR=${{ parameters.runtimeFlavor }} STATIC_LINKING=${{ parameters.staticLinking }}\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2114710936",
    "pr_number": 116114,
    "pr_file": "eng/pipelines/runtime.yml",
    "created_at": "2025-05-29T20:36:40+00:00",
    "commented_code": "- name: timeoutPerTestCollectionInMinutes\n            value: 180\n          jobParameters:\n            timeoutInMinutes: 120\n            timeoutInMinutes: 180",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2114710936",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116114,
        "pr_file": "eng/pipelines/runtime.yml",
        "discussion_id": "2114710936",
        "commented_code": "@@ -531,7 +531,7 @@ extends:\n           - name: timeoutPerTestCollectionInMinutes\n             value: 180\n           jobParameters:\n-            timeoutInMinutes: 120\n+            timeoutInMinutes: 180",
        "comment_created_at": "2025-05-29T20:36:40+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] Consider extracting the repeated timeout value into a template variable or parameter to avoid duplication and simplify future adjustments.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2114710947",
    "pr_number": 116114,
    "pr_file": "eng/pipelines/runtime.yml",
    "created_at": "2025-05-29T20:36:41+00:00",
    "commented_code": "value: 180\n          jobParameters:\n            testGroup: innerloop\n            timeoutInMinutes: 120\n            timeoutInMinutes: 180",
    "repo_full_name": "dotnet/runtime",
    "discussion_comments": [
      {
        "comment_id": "2114710947",
        "repo_full_name": "dotnet/runtime",
        "pr_number": 116114,
        "pr_file": "eng/pipelines/runtime.yml",
        "discussion_id": "2114710947",
        "commented_code": "@@ -614,7 +614,7 @@ extends:\n             value: 180\n           jobParameters:\n             testGroup: innerloop\n-            timeoutInMinutes: 120\n+            timeoutInMinutes: 180",
        "comment_created_at": "2025-05-29T20:36:41+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] This timeout value is duplicated; using a shared variable would reduce repetition and make updates easier.\n```suggestion\n            timeoutInMinutes: ${{ variables['timeoutPerTestCollectionInMinutes'] }}\n```",
        "pr_file_module": null
      }
    ]
  }
]
