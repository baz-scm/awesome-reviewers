---
title: Structured documentation with examples
description: 'Create comprehensive documentation with clear structure and practical
  examples. Documentation should include:


  1. **Standard documentation files** like README.md, CHANGELOG.md, and CONTRIBUTING.md,
  even if they primarily link to external resources. Search engines index these standard
  files, improving project discoverability.'
repository: kubeflow/kubeflow
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 15064
---

Create comprehensive documentation with clear structure and practical examples. Documentation should include:

1. **Standard documentation files** like README.md, CHANGELOG.md, and CONTRIBUTING.md, even if they primarily link to external resources. Search engines index these standard files, improving project discoverability.

2. **Well-organized content** with clear headings, tables for related information, and consistent formatting. For complex projects, organize information hierarchically:

```markdown
# Component Name

## About
Brief description of the component's purpose.

## Table of Components
| Component | Source Repository |
|-----------|-------------------|
| Component A | [`org/repo-a`](https://github.com/org/repo-a) |
| Component B | [`org/repo-b`](https://github.com/org/repo-b) |

## Usage Examples
```

3. **Usage examples** demonstrating common tasks. For instance, when documenting test procedures:

```markdown
**Run all tests**
`make run`

**Run component-specific tests**
`make run-kfp`  # Run Kubeflow Pipelines tests
`make run-katib` # Run Katib tests
```

4. **Active voice** rather than passive voice to improve clarity and directness.

5. **Links to stable versions** rather than development branches to prevent users from accidentally using unstable code.

Following these practices makes documentation more useful, accessible, and maintainable while improving the overall user experience.


[
  {
    "discussion_id": "1746924443",
    "pr_number": 7642,
    "pr_file": "CHANGELOG.md",
    "created_at": "2024-09-06T10:48:58+00:00",
    "commented_code": "# Change Log\n# Changelog\n\nThe [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1746924443",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T10:48:58+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "Does it make sense to list which components that release page covers (e.g. Central Dashboard, Notebooks, etc.)?",
        "pr_file_module": null
      },
      {
        "comment_id": "1747526308",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T18:03:24+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "It covers everything, so that is probably not that useful.\r\n\r\nIt's the overall \"platform version\" so by proxy includes everything.",
        "pr_file_module": null
      },
      {
        "comment_id": "1747580441",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T18:51:51+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "@thesuperzapper Are we planing to remove this changelog from `kubeflow/kubeflow` once we split the repos ?",
        "pr_file_module": null
      },
      {
        "comment_id": "1747736618",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T21:27:38+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "This changelog is only here for historical reasons, it only includes stuff from 0.5 and earlier.\r\n\r\nWe may as well leave it once we split the repo, and leave the top section which links to the more modern changelogs. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1747743581",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T21:36:36+00:00",
        "comment_author": "andreyvelich",
        "comment_body": ">We may as well leave it once we split the repo, and leave the top section which links to the more modern changelogs.\r\n\r\nYeah, but in that case you have to constantly update this changelog which links to changelogs of every Kubeflow components after Kubeflow release.\r\nDo we want to do it in the future ?",
        "pr_file_module": null
      },
      {
        "comment_id": "1747744882",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T21:38:31+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "We should 100% have a page under this section of the website which includes those links:\r\n\r\n- https://www.kubeflow.org/docs/releases/\r\n\r\nAnd just link to that page.",
        "pr_file_module": null
      },
      {
        "comment_id": "1747746000",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T21:40:01+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "Should we just use section in README for it to minimize number of files in `kubeflow/kubeflow` repo ?",
        "pr_file_module": null
      },
      {
        "comment_id": "1747753171",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CHANGELOG.md",
        "discussion_id": "1746924443",
        "commented_code": "@@ -1,4 +1,10 @@\n-# Change Log\n+# Changelog\n+\n+The [GitHub Releases](https://github.com/kubeflow/kubeflow/releases) page covers newer versions of `kubeflow/kubeflow` components.",
        "comment_created_at": "2024-09-06T21:50:17+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "As I was saying, google loves CHANGELOG.md files, so even a largely empty file which just links to the website is good.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1746925519",
    "pr_number": 7642,
    "pr_file": "CONTRIBUTING.md",
    "created_at": "2024-09-06T10:50:06+00:00",
    "commented_code": "# Kubeflow Contributor Guide",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1746925519",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CONTRIBUTING.md",
        "discussion_id": "1746925519",
        "commented_code": "@@ -1,13 +1,6 @@\n # Kubeflow Contributor Guide",
        "comment_created_at": "2024-09-06T10:50:06+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "@thesuperzapper Would it be easier to remove this file and just add the `## Contributing` section to the README where we link the https://www.kubeflow.org/docs/about/contributing/ page ?",
        "pr_file_module": null
      },
      {
        "comment_id": "1747527963",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CONTRIBUTING.md",
        "discussion_id": "1746925519",
        "commented_code": "@@ -1,13 +1,6 @@\n # Kubeflow Contributor Guide",
        "comment_created_at": "2024-09-06T18:04:35+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "We should probably have both, because google loves to index files like `CONTRIBUTING.md`.",
        "pr_file_module": null
      },
      {
        "comment_id": "1747540602",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "CONTRIBUTING.md",
        "discussion_id": "1746925519",
        "commented_code": "@@ -1,13 +1,6 @@\n # Kubeflow Contributor Guide",
        "comment_created_at": "2024-09-06T18:15:19+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "I added `& Contributing` to the final README heading in https://github.com/kubeflow/kubeflow/pull/7642/commits/5513f05f5a67250aeb152b4154f1bb1ed523b727",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1746931065",
    "pr_number": 7642,
    "pr_file": "README.md",
    "created_at": "2024-09-06T10:55:58+00:00",
    "commented_code": "<img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n# Kubeflow\n\n[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n[![Join Kubeflow Slack](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n[![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/kubeflow/badge)](https://clomonitor.io/projects/cncf/kubeflow)\n[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/2660/badge)](https://www.bestpractices.dev/projects/2660)\n\nThe Kubeflow makes AI/ML on Kubernetes simple, portable and scalable.\n<img src=\"./logo/icon.svg\" width=\"120\">\n\n---\n## About Kubeflow\n\n## Documentation\n[Kubeflow](https://www.kubeflow.org/) makes artificial intelligence and machine learning simple, portable, and scalable.\nWe are an _ecosystem_ of [Kubernetes](https://kubernetes.io/) based components for each stage in the [AI/ML Lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle) with support for best-in-class open source [tools and frameworks](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem).\n\nPlease refer to the official docs at [kubeflow.org](http://kubeflow.org).\nPlease refer to the official [documentation](https://www.kubeflow.org/docs/) for more information.\n\n## Kubeflow Components\n\nThe Kubeflow ecosystem is composed of multiple open-source projects for each stage in\n[the ML lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle).\nThe [Kubeflow Ecosystem](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem) is composed of several projects known as [Kubeflow Components](https://www.kubeflow.org/docs/components/).\n\nLearn more about each project in [the Kubeflow documentation](https://www.kubeflow.org/docs/components/).\nThe following table lists the components and their respective source code repositories:\n\nPlease use the following GitHub repositories to open issues and pull requests for\n[the different Kubeflow components](https://www.kubeflow.org/docs/started/introduction/#what-are-standalone-kubeflow-components):\n| Component                                                                           | Source Code                                                                   |\n|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|\n| [KServe](https://www.kubeflow.org/docs/external-add-ons/kserve/)                    | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n| [Kubeflow Katib](https://www.kubeflow.org/docs/components/katib/)                   | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n| [Kubeflow Model Registry](https://www.kubeflow.org/docs/components/model-registry/) | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n| Kubeflow MPI Operator                                                               | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n| [Kubeflow Notebooks](https://www.kubeflow.org/docs/components/notebooks/)           | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n| [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)           | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n| [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/) | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n| [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/training/)    | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n\n| Component                  | Source Code                                                                   |\n| -------------------------- | ----------------------------------------------------------------------------- |\n| KServe                     | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n| Kubeflow Katib             | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n| Kubeflow Model Registry    | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n| Kubeflow MPI Operator      | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n| Kubeflow Notebooks         | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n| Kubeflow Pipelines         | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n| Kubeflow Spark Operator    | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n| Kubeflow Training Operator | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n## Kubeflow Platform\n\nIf you want to open issue or pull request for the\n[Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform)\ncomponents:\nThe [Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform) refers to the full suite of Kubeflow Components bundled together with additional integration and management tools.\n\n- Use the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) GitHub repository for\n  the Kubeflow Manifests.\n- Use the [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) GitHub repository for\n  the Kubeflow Profile Controller, Central Dashboard, CRUD Web Apps, PVC Viewer, PodDefault, and\n  Access Management components.\nThe following table lists the platform components and their respective source code repositories:\n\nIf you have questions about Kubeflow community or Kubeflow ecosystem, please use the\n[`kubeflow/community`](https://github.com/kubeflow/community) GitHub repository.\n| Component                                                                             | Source Code                                                   |\n|---------------------------------------------------------------------------------------|---------------------------------------------------------------|\n| [Central Dashboard](https://www.kubeflow.org/docs/components/central-dash/)           | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n| [Profile Controller](https://www.kubeflow.org/docs/components/central-dash/profiles/) | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n| Kubeflow Manifests                                                                    | [`kubeflow/manifests`](https://github.com/kubeflow/manifests) |",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1746931065",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "README.md",
        "discussion_id": "1746931065",
        "commented_code": "@@ -1,52 +1,49 @@\n-<img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n+# Kubeflow\n \n-[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n+[![Join Kubeflow Slack](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n [![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/kubeflow/badge)](https://clomonitor.io/projects/cncf/kubeflow)\n+[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/2660/badge)](https://www.bestpractices.dev/projects/2660)\n \n-The Kubeflow makes AI/ML on Kubernetes simple, portable and scalable.\n+<img src=\"./logo/icon.svg\" width=\"120\">\n \n----\n+## About Kubeflow\n \n-## Documentation\n+[Kubeflow](https://www.kubeflow.org/) makes artificial intelligence and machine learning simple, portable, and scalable.\n+We are an _ecosystem_ of [Kubernetes](https://kubernetes.io/) based components for each stage in the [AI/ML Lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle) with support for best-in-class open source [tools and frameworks](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem).\n \n-Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n+Please refer to the official [documentation](https://www.kubeflow.org/docs/) for more information.\n \n ## Kubeflow Components\n \n-The Kubeflow ecosystem is composed of multiple open-source projects for each stage in\n-[the ML lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle).\n+The [Kubeflow Ecosystem](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem) is composed of several projects known as [Kubeflow Components](https://www.kubeflow.org/docs/components/).\n \n-Learn more about each project in [the Kubeflow documentation](https://www.kubeflow.org/docs/components/).\n+The following table lists the components and their respective source code repositories:\n \n-Please use the following GitHub repositories to open issues and pull requests for\n-[the different Kubeflow components](https://www.kubeflow.org/docs/started/introduction/#what-are-standalone-kubeflow-components):\n+| Component                                                                           | Source Code                                                                   |\n+|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|\n+| [KServe](https://www.kubeflow.org/docs/external-add-ons/kserve/)                    | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n+| [Kubeflow Katib](https://www.kubeflow.org/docs/components/katib/)                   | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n+| [Kubeflow Model Registry](https://www.kubeflow.org/docs/components/model-registry/) | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n+| Kubeflow MPI Operator                                                               | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n+| [Kubeflow Notebooks](https://www.kubeflow.org/docs/components/notebooks/)           | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n+| [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)           | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n+| [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/) | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n+| [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/training/)    | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n \n-| Component                  | Source Code                                                                   |\n-| -------------------------- | ----------------------------------------------------------------------------- |\n-| KServe                     | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n-| Kubeflow Katib             | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n-| Kubeflow Model Registry    | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n-| Kubeflow MPI Operator      | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n-| Kubeflow Notebooks         | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n-| Kubeflow Pipelines         | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n-| Kubeflow Spark Operator    | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n-| Kubeflow Training Operator | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n+## Kubeflow Platform\n \n-If you want to open issue or pull request for the\n-[Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform)\n-components:\n+The [Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform) refers to the full suite of Kubeflow Components bundled together with additional integration and management tools.\n \n-- Use the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) GitHub repository for\n-  the Kubeflow Manifests.\n-- Use the [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) GitHub repository for\n-  the Kubeflow Profile Controller, Central Dashboard, CRUD Web Apps, PVC Viewer, PodDefault, and\n-  Access Management components.\n+The following table lists the platform components and their respective source code repositories:\n \n-If you have questions about Kubeflow community or Kubeflow ecosystem, please use the\n-[`kubeflow/community`](https://github.com/kubeflow/community) GitHub repository.\n+| Component                                                                             | Source Code                                                   |\n+|---------------------------------------------------------------------------------------|---------------------------------------------------------------|\n+| [Central Dashboard](https://www.kubeflow.org/docs/components/central-dash/)           | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| [Profile Controller](https://www.kubeflow.org/docs/components/central-dash/profiles/) | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| Kubeflow Manifests                                                                    | [`kubeflow/manifests`](https://github.com/kubeflow/manifests) |",
        "comment_created_at": "2024-09-06T10:55:58+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "Should we link the README for Kubeflow Manifests: https://github.com/kubeflow/manifests?tab=readme-ov-file#overview-of-the-kubeflow-platform ?",
        "pr_file_module": null
      },
      {
        "comment_id": "1747534477",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "README.md",
        "discussion_id": "1746931065",
        "commented_code": "@@ -1,52 +1,49 @@\n-<img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n+# Kubeflow\n \n-[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n+[![Join Kubeflow Slack](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n [![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/kubeflow/badge)](https://clomonitor.io/projects/cncf/kubeflow)\n+[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/2660/badge)](https://www.bestpractices.dev/projects/2660)\n \n-The Kubeflow makes AI/ML on Kubernetes simple, portable and scalable.\n+<img src=\"./logo/icon.svg\" width=\"120\">\n \n----\n+## About Kubeflow\n \n-## Documentation\n+[Kubeflow](https://www.kubeflow.org/) makes artificial intelligence and machine learning simple, portable, and scalable.\n+We are an _ecosystem_ of [Kubernetes](https://kubernetes.io/) based components for each stage in the [AI/ML Lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle) with support for best-in-class open source [tools and frameworks](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem).\n \n-Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n+Please refer to the official [documentation](https://www.kubeflow.org/docs/) for more information.\n \n ## Kubeflow Components\n \n-The Kubeflow ecosystem is composed of multiple open-source projects for each stage in\n-[the ML lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle).\n+The [Kubeflow Ecosystem](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem) is composed of several projects known as [Kubeflow Components](https://www.kubeflow.org/docs/components/).\n \n-Learn more about each project in [the Kubeflow documentation](https://www.kubeflow.org/docs/components/).\n+The following table lists the components and their respective source code repositories:\n \n-Please use the following GitHub repositories to open issues and pull requests for\n-[the different Kubeflow components](https://www.kubeflow.org/docs/started/introduction/#what-are-standalone-kubeflow-components):\n+| Component                                                                           | Source Code                                                                   |\n+|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|\n+| [KServe](https://www.kubeflow.org/docs/external-add-ons/kserve/)                    | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n+| [Kubeflow Katib](https://www.kubeflow.org/docs/components/katib/)                   | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n+| [Kubeflow Model Registry](https://www.kubeflow.org/docs/components/model-registry/) | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n+| Kubeflow MPI Operator                                                               | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n+| [Kubeflow Notebooks](https://www.kubeflow.org/docs/components/notebooks/)           | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n+| [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)           | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n+| [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/) | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n+| [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/training/)    | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n \n-| Component                  | Source Code                                                                   |\n-| -------------------------- | ----------------------------------------------------------------------------- |\n-| KServe                     | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n-| Kubeflow Katib             | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n-| Kubeflow Model Registry    | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n-| Kubeflow MPI Operator      | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n-| Kubeflow Notebooks         | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n-| Kubeflow Pipelines         | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n-| Kubeflow Spark Operator    | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n-| Kubeflow Training Operator | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n+## Kubeflow Platform\n \n-If you want to open issue or pull request for the\n-[Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform)\n-components:\n+The [Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform) refers to the full suite of Kubeflow Components bundled together with additional integration and management tools.\n \n-- Use the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) GitHub repository for\n-  the Kubeflow Manifests.\n-- Use the [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) GitHub repository for\n-  the Kubeflow Profile Controller, Central Dashboard, CRUD Web Apps, PVC Viewer, PodDefault, and\n-  Access Management components.\n+The following table lists the platform components and their respective source code repositories:\n \n-If you have questions about Kubeflow community or Kubeflow ecosystem, please use the\n-[`kubeflow/community`](https://github.com/kubeflow/community) GitHub repository.\n+| Component                                                                             | Source Code                                                   |\n+|---------------------------------------------------------------------------------------|---------------------------------------------------------------|\n+| [Central Dashboard](https://www.kubeflow.org/docs/components/central-dash/)           | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| [Profile Controller](https://www.kubeflow.org/docs/components/central-dash/profiles/) | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| Kubeflow Manifests                                                                    | [`kubeflow/manifests`](https://github.com/kubeflow/manifests) |",
        "comment_created_at": "2024-09-06T18:09:59+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "It's the same link as the repo, also, we need to be careful about linking people directly to the `master` of manifests, as they might try and install from there, rather than an actual version like `v1.9.0` tag.",
        "pr_file_module": null
      },
      {
        "comment_id": "1747578150",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "README.md",
        "discussion_id": "1746931065",
        "commented_code": "@@ -1,52 +1,49 @@\n-<img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n+# Kubeflow\n \n-[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n+[![Join Kubeflow Slack](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n [![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/kubeflow/badge)](https://clomonitor.io/projects/cncf/kubeflow)\n+[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/2660/badge)](https://www.bestpractices.dev/projects/2660)\n \n-The Kubeflow makes AI/ML on Kubernetes simple, portable and scalable.\n+<img src=\"./logo/icon.svg\" width=\"120\">\n \n----\n+## About Kubeflow\n \n-## Documentation\n+[Kubeflow](https://www.kubeflow.org/) makes artificial intelligence and machine learning simple, portable, and scalable.\n+We are an _ecosystem_ of [Kubernetes](https://kubernetes.io/) based components for each stage in the [AI/ML Lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle) with support for best-in-class open source [tools and frameworks](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem).\n \n-Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n+Please refer to the official [documentation](https://www.kubeflow.org/docs/) for more information.\n \n ## Kubeflow Components\n \n-The Kubeflow ecosystem is composed of multiple open-source projects for each stage in\n-[the ML lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle).\n+The [Kubeflow Ecosystem](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem) is composed of several projects known as [Kubeflow Components](https://www.kubeflow.org/docs/components/).\n \n-Learn more about each project in [the Kubeflow documentation](https://www.kubeflow.org/docs/components/).\n+The following table lists the components and their respective source code repositories:\n \n-Please use the following GitHub repositories to open issues and pull requests for\n-[the different Kubeflow components](https://www.kubeflow.org/docs/started/introduction/#what-are-standalone-kubeflow-components):\n+| Component                                                                           | Source Code                                                                   |\n+|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|\n+| [KServe](https://www.kubeflow.org/docs/external-add-ons/kserve/)                    | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n+| [Kubeflow Katib](https://www.kubeflow.org/docs/components/katib/)                   | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n+| [Kubeflow Model Registry](https://www.kubeflow.org/docs/components/model-registry/) | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n+| Kubeflow MPI Operator                                                               | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n+| [Kubeflow Notebooks](https://www.kubeflow.org/docs/components/notebooks/)           | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n+| [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)           | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n+| [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/) | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n+| [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/training/)    | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n \n-| Component                  | Source Code                                                                   |\n-| -------------------------- | ----------------------------------------------------------------------------- |\n-| KServe                     | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n-| Kubeflow Katib             | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n-| Kubeflow Model Registry    | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n-| Kubeflow MPI Operator      | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n-| Kubeflow Notebooks         | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n-| Kubeflow Pipelines         | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n-| Kubeflow Spark Operator    | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n-| Kubeflow Training Operator | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n+## Kubeflow Platform\n \n-If you want to open issue or pull request for the\n-[Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform)\n-components:\n+The [Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform) refers to the full suite of Kubeflow Components bundled together with additional integration and management tools.\n \n-- Use the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) GitHub repository for\n-  the Kubeflow Manifests.\n-- Use the [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) GitHub repository for\n-  the Kubeflow Profile Controller, Central Dashboard, CRUD Web Apps, PVC Viewer, PodDefault, and\n-  Access Management components.\n+The following table lists the platform components and their respective source code repositories:\n \n-If you have questions about Kubeflow community or Kubeflow ecosystem, please use the\n-[`kubeflow/community`](https://github.com/kubeflow/community) GitHub repository.\n+| Component                                                                             | Source Code                                                   |\n+|---------------------------------------------------------------------------------------|---------------------------------------------------------------|\n+| [Central Dashboard](https://www.kubeflow.org/docs/components/central-dash/)           | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| [Profile Controller](https://www.kubeflow.org/docs/components/central-dash/profiles/) | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| Kubeflow Manifests                                                                    | [`kubeflow/manifests`](https://github.com/kubeflow/manifests) |",
        "comment_created_at": "2024-09-06T18:50:25+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "Sure, @kubeflow/wg-manifests-leads any comments there ?\r\nI am fine to make this as a followup change when we have dedicated website section that explains Kubeflow Manifests. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1747739190",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "README.md",
        "discussion_id": "1746931065",
        "commented_code": "@@ -1,52 +1,49 @@\n-<img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n+# Kubeflow\n \n-[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n+[![Join Kubeflow Slack](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n [![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/kubeflow/badge)](https://clomonitor.io/projects/cncf/kubeflow)\n+[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/2660/badge)](https://www.bestpractices.dev/projects/2660)\n \n-The Kubeflow makes AI/ML on Kubernetes simple, portable and scalable.\n+<img src=\"./logo/icon.svg\" width=\"120\">\n \n----\n+## About Kubeflow\n \n-## Documentation\n+[Kubeflow](https://www.kubeflow.org/) makes artificial intelligence and machine learning simple, portable, and scalable.\n+We are an _ecosystem_ of [Kubernetes](https://kubernetes.io/) based components for each stage in the [AI/ML Lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle) with support for best-in-class open source [tools and frameworks](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem).\n \n-Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n+Please refer to the official [documentation](https://www.kubeflow.org/docs/) for more information.\n \n ## Kubeflow Components\n \n-The Kubeflow ecosystem is composed of multiple open-source projects for each stage in\n-[the ML lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle).\n+The [Kubeflow Ecosystem](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem) is composed of several projects known as [Kubeflow Components](https://www.kubeflow.org/docs/components/).\n \n-Learn more about each project in [the Kubeflow documentation](https://www.kubeflow.org/docs/components/).\n+The following table lists the components and their respective source code repositories:\n \n-Please use the following GitHub repositories to open issues and pull requests for\n-[the different Kubeflow components](https://www.kubeflow.org/docs/started/introduction/#what-are-standalone-kubeflow-components):\n+| Component                                                                           | Source Code                                                                   |\n+|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|\n+| [KServe](https://www.kubeflow.org/docs/external-add-ons/kserve/)                    | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n+| [Kubeflow Katib](https://www.kubeflow.org/docs/components/katib/)                   | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n+| [Kubeflow Model Registry](https://www.kubeflow.org/docs/components/model-registry/) | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n+| Kubeflow MPI Operator                                                               | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n+| [Kubeflow Notebooks](https://www.kubeflow.org/docs/components/notebooks/)           | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n+| [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)           | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n+| [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/) | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n+| [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/training/)    | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n \n-| Component                  | Source Code                                                                   |\n-| -------------------------- | ----------------------------------------------------------------------------- |\n-| KServe                     | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n-| Kubeflow Katib             | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n-| Kubeflow Model Registry    | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n-| Kubeflow MPI Operator      | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n-| Kubeflow Notebooks         | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n-| Kubeflow Pipelines         | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n-| Kubeflow Spark Operator    | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n-| Kubeflow Training Operator | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n+## Kubeflow Platform\n \n-If you want to open issue or pull request for the\n-[Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform)\n-components:\n+The [Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform) refers to the full suite of Kubeflow Components bundled together with additional integration and management tools.\n \n-- Use the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) GitHub repository for\n-  the Kubeflow Manifests.\n-- Use the [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) GitHub repository for\n-  the Kubeflow Profile Controller, Central Dashboard, CRUD Web Apps, PVC Viewer, PodDefault, and\n-  Access Management components.\n+The following table lists the platform components and their respective source code repositories:\n \n-If you have questions about Kubeflow community or Kubeflow ecosystem, please use the\n-[`kubeflow/community`](https://github.com/kubeflow/community) GitHub repository.\n+| Component                                                                             | Source Code                                                   |\n+|---------------------------------------------------------------------------------------|---------------------------------------------------------------|\n+| [Central Dashboard](https://www.kubeflow.org/docs/components/central-dash/)           | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| [Profile Controller](https://www.kubeflow.org/docs/components/central-dash/profiles/) | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| Kubeflow Manifests                                                                    | [`kubeflow/manifests`](https://github.com/kubeflow/manifests) |",
        "comment_created_at": "2024-09-06T21:30:57+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "@andreyvelich I don't think we need more than we already have on the \"Installing Kubeflow\" page: \r\n- https://www.kubeflow.org/docs/started/installing-kubeflow/#kubeflow-manifests\r\n\r\nAs I keep highlighting, the manifests are intended to be used as the base of distribution, and by advanced users wanting to test Kubeflow out.\r\n\r\nFor almost everyone else, they will have a bad experience trying to use the manifests in production. We already get a lot of spam issues from people asking for help on issues that are unrelated to our Kubeflow and are more about their specific platform, I don't want to increase the amount of that.",
        "pr_file_module": null
      },
      {
        "comment_id": "1747755050",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7642,
        "pr_file": "README.md",
        "discussion_id": "1746931065",
        "commented_code": "@@ -1,52 +1,49 @@\n-<img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n+# Kubeflow\n \n-[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n+[![Join Kubeflow Slack](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://www.kubeflow.org/docs/about/community/#kubeflow-slack-channels)\n [![CLOMonitor](https://img.shields.io/endpoint?url=https://clomonitor.io/api/projects/cncf/kubeflow/badge)](https://clomonitor.io/projects/cncf/kubeflow)\n+[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/2660/badge)](https://www.bestpractices.dev/projects/2660)\n \n-The Kubeflow makes AI/ML on Kubernetes simple, portable and scalable.\n+<img src=\"./logo/icon.svg\" width=\"120\">\n \n----\n+## About Kubeflow\n \n-## Documentation\n+[Kubeflow](https://www.kubeflow.org/) makes artificial intelligence and machine learning simple, portable, and scalable.\n+We are an _ecosystem_ of [Kubernetes](https://kubernetes.io/) based components for each stage in the [AI/ML Lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle) with support for best-in-class open source [tools and frameworks](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem).\n \n-Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n+Please refer to the official [documentation](https://www.kubeflow.org/docs/) for more information.\n \n ## Kubeflow Components\n \n-The Kubeflow ecosystem is composed of multiple open-source projects for each stage in\n-[the ML lifecycle](https://www.kubeflow.org/docs/started/architecture/#kubeflow-components-in-the-ml-lifecycle).\n+The [Kubeflow Ecosystem](https://www.kubeflow.org/docs/started/architecture/#kubeflow-ecosystem) is composed of several projects known as [Kubeflow Components](https://www.kubeflow.org/docs/components/).\n \n-Learn more about each project in [the Kubeflow documentation](https://www.kubeflow.org/docs/components/).\n+The following table lists the components and their respective source code repositories:\n \n-Please use the following GitHub repositories to open issues and pull requests for\n-[the different Kubeflow components](https://www.kubeflow.org/docs/started/introduction/#what-are-standalone-kubeflow-components):\n+| Component                                                                           | Source Code                                                                   |\n+|-------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|\n+| [KServe](https://www.kubeflow.org/docs/external-add-ons/kserve/)                    | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n+| [Kubeflow Katib](https://www.kubeflow.org/docs/components/katib/)                   | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n+| [Kubeflow Model Registry](https://www.kubeflow.org/docs/components/model-registry/) | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n+| Kubeflow MPI Operator                                                               | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n+| [Kubeflow Notebooks](https://www.kubeflow.org/docs/components/notebooks/)           | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n+| [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)           | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n+| [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/) | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n+| [Kubeflow Training Operator](https://www.kubeflow.org/docs/components/training/)    | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n \n-| Component                  | Source Code                                                                   |\n-| -------------------------- | ----------------------------------------------------------------------------- |\n-| KServe                     | [`kserve/kserve`](https://github.com/kserve/kserve)                           |\n-| Kubeflow Katib             | [`kubeflow/katib`](https://github.com/kubeflow/katib)                         |\n-| Kubeflow Model Registry    | [`kubeflow/model-registry`](https://github.com/kubeflow/model-registry)       |\n-| Kubeflow MPI Operator      | [`kubeflow/mpi-operator`](https://github.com/kubeflow/mpi-operator)           |\n-| Kubeflow Notebooks         | [`kubeflow/notebooks`](https://github.com/kubeflow/notebooks)                 |\n-| Kubeflow Pipelines         | [`kubeflow/pipelines`](https://github.com/kubeflow/pipelines)                 |\n-| Kubeflow Spark Operator    | [`kubeflow/spark-operator`](https://github.com/kubeflow/spark-operator)       |\n-| Kubeflow Training Operator | [`kubeflow/training-operator`](https://github.com/kubeflow/training-operator) |\n+## Kubeflow Platform\n \n-If you want to open issue or pull request for the\n-[Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform)\n-components:\n+The [Kubeflow Platform](https://www.kubeflow.org/docs/started/introduction/#what-is-kubeflow-platform) refers to the full suite of Kubeflow Components bundled together with additional integration and management tools.\n \n-- Use the [`kubeflow/manifests`](https://github.com/kubeflow/manifests) GitHub repository for\n-  the Kubeflow Manifests.\n-- Use the [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) GitHub repository for\n-  the Kubeflow Profile Controller, Central Dashboard, CRUD Web Apps, PVC Viewer, PodDefault, and\n-  Access Management components.\n+The following table lists the platform components and their respective source code repositories:\n \n-If you have questions about Kubeflow community or Kubeflow ecosystem, please use the\n-[`kubeflow/community`](https://github.com/kubeflow/community) GitHub repository.\n+| Component                                                                             | Source Code                                                   |\n+|---------------------------------------------------------------------------------------|---------------------------------------------------------------|\n+| [Central Dashboard](https://www.kubeflow.org/docs/components/central-dash/)           | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| [Profile Controller](https://www.kubeflow.org/docs/components/central-dash/profiles/) | [`kubeflow/dashboard`](https://github.com/kubeflow/dashboard) |\n+| Kubeflow Manifests                                                                    | [`kubeflow/manifests`](https://github.com/kubeflow/manifests) |",
        "comment_created_at": "2024-09-06T21:53:12+00:00",
        "comment_author": "thesuperzapper",
        "comment_body": "I have added the link above in https://github.com/kubeflow/kubeflow/pull/7642/commits/7abcd7727c4611076aa22c4d63eced167e14b619",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1186256926",
    "pr_number": 7123,
    "pr_file": "conformance/1.7/README.md",
    "created_at": "2023-05-05T15:55:30+00:00",
    "commented_code": "# Kubeflow conformance program (WIP)\n\nBefore running the conformance tests, you need to configure kubectl default context to point to the k8s cluster that is hosting Kubeflow.\n\nTODO: Make the kubeflow namespace configurable.\n\nTo run version <x.y> of the conformance test.\n\n`cd kubeflow/conformance/<x.y>`\n\n**Run conformance test**\n\n`make run`",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1186256926",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7123,
        "pr_file": "conformance/1.7/README.md",
        "discussion_id": "1186256926",
        "commented_code": "@@ -0,0 +1,27 @@\n+# Kubeflow conformance program (WIP)\n+\n+Before running the conformance tests, you need to configure kubectl default context to point to the k8s cluster that is hosting Kubeflow.\n+\n+TODO: Make the kubeflow namespace configurable.\n+\n+To run version <x.y> of the conformance test.\n+\n+`cd kubeflow/conformance/<x.y>`\n+\n+**Run conformance test**\n+\n+`make run`",
        "comment_created_at": "2023-05-05T15:55:30+00:00",
        "comment_author": "gkcalat",
        "comment_body": "NIT: add brief comments on how to run component-specific tests (e.g. `make run-kfp`)",
        "pr_file_module": null
      },
      {
        "comment_id": "1186512090",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 7123,
        "pr_file": "conformance/1.7/README.md",
        "discussion_id": "1186256926",
        "commented_code": "@@ -0,0 +1,27 @@\n+# Kubeflow conformance program (WIP)\n+\n+Before running the conformance tests, you need to configure kubectl default context to point to the k8s cluster that is hosting Kubeflow.\n+\n+TODO: Make the kubeflow namespace configurable.\n+\n+To run version <x.y> of the conformance test.\n+\n+`cd kubeflow/conformance/<x.y>`\n+\n+**Run conformance test**\n+\n+`make run`",
        "comment_created_at": "2023-05-05T21:27:39+00:00",
        "comment_author": "james-jwu",
        "comment_body": "Done.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "596651177",
    "pr_number": 5694,
    "pr_file": "components/example-notebook-servers/README.md",
    "created_at": "2021-03-18T08:41:34+00:00",
    "commented_code": "# Example Notebook Servers\n\n**DISCLAIMER:** The Notebooks Working Group provides these Dockerfiles and\ntheir images as examples only, they are not tested with our CI/CD pipelines\nand are not certified to work in every situation. As such, issues related to\nthese images will be dealt with in a best efforts approach. The Notebooks\nWorking Group will work on officially supporting some of these Notebook\nServer images in the near future. If you do encounter a problem in one of\nthese images, contributions and issue reports are greatly appreciated.\n\n## Introduction",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "596651177",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5694,
        "pr_file": "components/example-notebook-servers/README.md",
        "discussion_id": "596651177",
        "commented_code": "@@ -0,0 +1,139 @@\n+# Example Notebook Servers\n+\n+**DISCLAIMER:** The Notebooks Working Group provides these Dockerfiles and\n+their images as examples only, they are not tested with our CI/CD pipelines\n+and are not certified to work in every situation. As such, issues related to\n+these images will be dealt with in a best efforts approach. The Notebooks\n+Working Group will work on officially supporting some of these Notebook\n+Server images in the near future. If you do encounter a problem in one of\n+these images, contributions and issue reports are greatly appreciated.\n+\n+## Introduction",
        "comment_created_at": "2021-03-18T08:41:34+00:00",
        "comment_author": "StefanoFioravanzo",
        "comment_body": "I would suggest trying to remove the passive voice in favour for an active voice. This is a general comment for the entire document.",
        "pr_file_module": null
      },
      {
        "comment_id": "596679316",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5694,
        "pr_file": "components/example-notebook-servers/README.md",
        "discussion_id": "596651177",
        "commented_code": "@@ -0,0 +1,139 @@\n+# Example Notebook Servers\n+\n+**DISCLAIMER:** The Notebooks Working Group provides these Dockerfiles and\n+their images as examples only, they are not tested with our CI/CD pipelines\n+and are not certified to work in every situation. As such, issues related to\n+these images will be dealt with in a best efforts approach. The Notebooks\n+Working Group will work on officially supporting some of these Notebook\n+Server images in the near future. If you do encounter a problem in one of\n+these images, contributions and issue reports are greatly appreciated.\n+\n+## Introduction",
        "comment_created_at": "2021-03-18T09:20:21+00:00",
        "comment_author": "davidspek",
        "comment_body": "Yeah, I will look into this. I'm used to scientific writing so tend to default to the passive voice. ",
        "pr_file_module": null
      }
    ]
  }
]
