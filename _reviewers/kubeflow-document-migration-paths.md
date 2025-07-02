---
title: Document migration paths
description: 'When implementing version changes or migrations, provide comprehensive
  documentation and tools to support users through the transition process. This includes:'
repository: kubeflow/kubeflow
label: Migrations
language: Markdown
comments_count: 2
repository_stars: 15064
---

When implementing version changes or migrations, provide comprehensive documentation and tools to support users through the transition process. This includes:

1. Clearly identify and document breaking changes between versions
2. List specific dependencies required before and after migration
3. Provide step-by-step upgrade instructions with realistic expectations
4. Create migration tools with concrete usage examples

For example, when creating a version converter tool:

```
# KfDef version converter

## Overview
This is a simple helper CLI that converts KfDef between versions.

## Usage
A simple CLI to convert KfDef from v1alpha1 to v1beta1

Usage:
  kfdef-converter [command]

Available Commands:
  help        Help about any command
  tov1beta1   Convert a KfDef config in v1alpha1 into v1beta1 format.

## Example
# Convert a config file from v1alpha1 to v1beta1
kfdef-converter tov1beta1 --input=/path/to/old-config.yaml --output=/path/to/new-config.yaml
```

When planning roadmaps that include migrations, be specific about upgrade capabilities rather than making general promises. If complete migration support isn't feasible, consider defining limited scope migrations or marking them as stretch goals.


[
  {
    "discussion_id": "1194039704",
    "pr_number": 7132,
    "pr_file": "ROADMAP.md",
    "created_at": "2023-05-15T15:55:13+00:00",
    "commented_code": "# Kubeflow Roadmap\n\n## Kubeflow 1.8 Release, Planned: May 2023\nThe Kubeflow Community plans to deliver its v1.8 release in Oct 2023 per this timeline(pending link). The high level deliverables are tracked in the [v1.8 Release](https://github.com/orgs/kubeflow/projects/58/) Github project board. The v1.8 release process will be managed by the v1.8 [release team](https://github.com/kubeflow/community/blob/a956b3f6f15c49f928e37eaafec40d7f73ee1d5b/releases/release-team.md) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n\n### Themes\n* Kubernetes 1.26 and 1.27 support\n* Kubeflow Pipelines v2.0 release\n* Kubeflow security (TBD)\n* Kubeflow upgrade process (TBD)",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1194039704",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7132,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1194039704",
        "commented_code": "@@ -1,5 +1,38 @@\n # Kubeflow Roadmap\n \n+## Kubeflow 1.8 Release, Planned: May 2023\n+The Kubeflow Community plans to deliver its v1.8 release in Oct 2023 per this timeline(pending link). The high level deliverables are tracked in the [v1.8 Release](https://github.com/orgs/kubeflow/projects/58/) Github project board. The v1.8 release process will be managed by the v1.8 [release team](https://github.com/kubeflow/community/blob/a956b3f6f15c49f928e37eaafec40d7f73ee1d5b/releases/release-team.md) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+### Themes\n+* Kubernetes 1.26 and 1.27 support\n+* Kubeflow Pipelines v2.0 release\n+* Kubeflow security (TBD)\n+* Kubeflow upgrade process (TBD)",
        "comment_created_at": "2023-05-15T15:55:13+00:00",
        "comment_author": "jbottum",
        "comment_body": "We have listed upgrades on the roadmap before and have not delivered.   I am cautious to list upgrades without qualifier (stretch goal) or some well defined step towards upgrade i.e. list breaking changes, identify to/from dependencies and statements for upgrading a limited part of KF.   The documentation for an upgrade could be extensive as there are potentially a lot of choices.",
        "pr_file_module": null
      },
      {
        "comment_id": "1209421928",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7132,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1194039704",
        "commented_code": "@@ -1,5 +1,38 @@\n # Kubeflow Roadmap\n \n+## Kubeflow 1.8 Release, Planned: May 2023\n+The Kubeflow Community plans to deliver its v1.8 release in Oct 2023 per this timeline(pending link). The high level deliverables are tracked in the [v1.8 Release](https://github.com/orgs/kubeflow/projects/58/) Github project board. The v1.8 release process will be managed by the v1.8 [release team](https://github.com/kubeflow/community/blob/a956b3f6f15c49f928e37eaafec40d7f73ee1d5b/releases/release-team.md) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+### Themes\n+* Kubernetes 1.26 and 1.27 support\n+* Kubeflow Pipelines v2.0 release\n+* Kubeflow security (TBD)\n+* Kubeflow upgrade process (TBD)",
        "comment_created_at": "2023-05-29T15:36:50+00:00",
        "comment_author": "DnPlas",
        "comment_body": "Agree, after some discussion with the release team, I think I can narrow this down. I'll update this.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "334699694",
    "pr_number": 4298,
    "pr_file": "bootstrap/cmd/kfdefConverter/README.md",
    "created_at": "2019-10-14T23:28:37+00:00",
    "commented_code": "# KfDef version converter\n\n## Overview\n\nThis is a simple helper CLI that converts KfDef between versions.\n\n## Usage\n\n```\nA simple CLI to convert KfDef from v1alpha1 to v1beta1\n\nUsage:\n  kfdef-converter [command]\n\nAvailable Commands:\n  help        Help about any command\n  tov1beta1   Convert a KfDef config in v1alpha1 into v1beta1 format.",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "334699694",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4298,
        "pr_file": "bootstrap/cmd/kfdefConverter/README.md",
        "discussion_id": "334699694",
        "commented_code": "@@ -0,0 +1,23 @@\n+# KfDef version converter\n+\n+## Overview\n+\n+This is a simple helper CLI that converts KfDef between versions.\n+\n+## Usage\n+\n+```\n+A simple CLI to convert KfDef from v1alpha1 to v1beta1\n+\n+Usage:\n+  kfdef-converter [command]\n+\n+Available Commands:\n+  help        Help about any command\n+  tov1beta1   Convert a KfDef config in v1alpha1 into v1beta1 format.\n+",
        "comment_created_at": "2019-10-14T23:28:37+00:00",
        "comment_author": "lluunn",
        "comment_body": "probably add an example usage of kfdef-converter tov1beta1",
        "pr_file_module": null
      },
      {
        "comment_id": "334743542",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4298,
        "pr_file": "bootstrap/cmd/kfdefConverter/README.md",
        "discussion_id": "334699694",
        "commented_code": "@@ -0,0 +1,23 @@\n+# KfDef version converter\n+\n+## Overview\n+\n+This is a simple helper CLI that converts KfDef between versions.\n+\n+## Usage\n+\n+```\n+A simple CLI to convert KfDef from v1alpha1 to v1beta1\n+\n+Usage:\n+  kfdef-converter [command]\n+\n+Available Commands:\n+  help        Help about any command\n+  tov1beta1   Convert a KfDef config in v1alpha1 into v1beta1 format.\n+",
        "comment_created_at": "2019-10-15T03:59:01+00:00",
        "comment_author": "gabrielwen",
        "comment_body": "Added.",
        "pr_file_module": null
      }
    ]
  }
]
