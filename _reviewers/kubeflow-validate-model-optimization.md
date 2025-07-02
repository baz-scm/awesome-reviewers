---
title: Validate model optimization
description: 'When implementing AI model optimization techniques such as early stopping
  algorithms or hyperparameter tuning, include proper validation mechanisms to help
  users effectively reduce model overfitting and improve accuracy. '
repository: kubeflow/kubeflow
label: AI
language: Markdown
comments_count: 2
repository_stars: 15064
---

When implementing AI model optimization techniques such as early stopping algorithms or hyperparameter tuning, include proper validation mechanisms to help users effectively reduce model overfitting and improve accuracy. 

Validation should include:
1. Pre-execution checks on algorithm settings and configurations
2. Meaningful error messages for incorrect parameter ranges or incompatible settings
3. Documentation that explains the impact of each optimization technique

For example, when implementing early stopping validation for Katib experiments:

```yaml
# Example validation for early stopping settings
algorithm:
  earlyStoppingSettings:
    # Validate these values with appropriate ranges and types
    evaluationInterval: 1  # Validate this is a positive integer
    threshold: 0.01  # Validate this is a positive float
    comparisonType: "smaller"  # Validate this is one of ["smaller", "larger"]
```

This approach helps prevent common errors in machine learning workflows, reduces debugging time, and improves model quality by ensuring optimization techniques are correctly applied.


[
  {
    "discussion_id": "794906792",
    "pr_number": 6266,
    "pr_file": "ROADMAP.md",
    "created_at": "2022-01-28T21:40:42+00:00",
    "commented_code": "# Kubeflow Roadmap\n\n## Kubeflow 1.5 Release, Due: February 2022\n* Kubeflow 1.5 timeline is tracked in [#538](https://github.com/kubeflow/community/pull/538)\n* Additional details will be posted in early 1Q'22\n## Kubeflow 1.5 Release, Due: March 2022\n* Kubeflow 1.5 [milestones and timeline](https://github.com/kubeflow/community/pull/538)\n\n### Themes\n* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime\n* Improve model accuracy and reduce overfitting, especially with hyper parameter tuning\n* Simplify operations and optimize utilization (including spot instance use cases for distributed training) \n* More consistent user experience - UI appearance, features and naming\n* Improved documentation, tutorials and examples\n* Stretch - Support for K8s 1.22 and associated dependencies (cert mgr, istio)\n\n### Major Features from each Working Group (note: Individual WG versions are independent of Kubeflow's)\n\n#### Kubeflow Pipelines, v1.8\n* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime.\n\n#### Katib, v0.13 \n* Hyperparameter leader election for HA operations and faster recovery\n* Validation for Early Stopping algorithm settings improves accuracy, reduces overfitting",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "794906792",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6266,
        "pr_file": "ROADMAP.md",
        "discussion_id": "794906792",
        "commented_code": "@@ -1,10 +1,54 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.5 Release, Due: February 2022\n-* Kubeflow 1.5 timeline is tracked in [#538](https://github.com/kubeflow/community/pull/538)\n-* Additional details will be posted in early 1Q'22\n+## Kubeflow 1.5 Release, Due: March 2022\n+* Kubeflow 1.5 [milestones and timeline](https://github.com/kubeflow/community/pull/538)\n+\n+### Themes\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime\n+* Improve model accuracy and reduce overfitting, especially with hyper parameter tuning\n+* Simplify operations and optimize utilization (including spot instance use cases for distributed training) \n+* More consistent user experience - UI appearance, features and naming\n+* Improved documentation, tutorials and examples\n+* Stretch - Support for K8s 1.22 and associated dependencies (cert mgr, istio)\n+\n+### Major Features from each Working Group (note: Individual WG versions are independent of Kubeflow's)\n+\n+#### Kubeflow Pipelines, v1.8\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime.\n+\n+#### Katib, v0.13 \n+* Hyperparameter leader election for HA operations and faster recovery\n+* Validation for Early Stopping algorithm settings improves accuracy, reduces overfitting",
        "comment_created_at": "2022-01-28T21:40:42+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "Should we modify this @jbottum @tenzen-y @johnugeorge ?\r\n```suggestion\r\n* Validation for Early Stopping algorithm settings helps users to proper reduce model overfitting\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "794989244",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6266,
        "pr_file": "ROADMAP.md",
        "discussion_id": "794906792",
        "commented_code": "@@ -1,10 +1,54 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.5 Release, Due: February 2022\n-* Kubeflow 1.5 timeline is tracked in [#538](https://github.com/kubeflow/community/pull/538)\n-* Additional details will be posted in early 1Q'22\n+## Kubeflow 1.5 Release, Due: March 2022\n+* Kubeflow 1.5 [milestones and timeline](https://github.com/kubeflow/community/pull/538)\n+\n+### Themes\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime\n+* Improve model accuracy and reduce overfitting, especially with hyper parameter tuning\n+* Simplify operations and optimize utilization (including spot instance use cases for distributed training) \n+* More consistent user experience - UI appearance, features and naming\n+* Improved documentation, tutorials and examples\n+* Stretch - Support for K8s 1.22 and associated dependencies (cert mgr, istio)\n+\n+### Major Features from each Working Group (note: Individual WG versions are independent of Kubeflow's)\n+\n+#### Kubeflow Pipelines, v1.8\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime.\n+\n+#### Katib, v0.13 \n+* Hyperparameter leader election for HA operations and faster recovery\n+* Validation for Early Stopping algorithm settings improves accuracy, reduces overfitting",
        "comment_created_at": "2022-01-29T02:59:02+00:00",
        "comment_author": "tenzen-y",
        "comment_body": "It sounds great to me @andreyvelich!",
        "pr_file_module": null
      },
      {
        "comment_id": "795076103",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6266,
        "pr_file": "ROADMAP.md",
        "discussion_id": "794906792",
        "commented_code": "@@ -1,10 +1,54 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.5 Release, Due: February 2022\n-* Kubeflow 1.5 timeline is tracked in [#538](https://github.com/kubeflow/community/pull/538)\n-* Additional details will be posted in early 1Q'22\n+## Kubeflow 1.5 Release, Due: March 2022\n+* Kubeflow 1.5 [milestones and timeline](https://github.com/kubeflow/community/pull/538)\n+\n+### Themes\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime\n+* Improve model accuracy and reduce overfitting, especially with hyper parameter tuning\n+* Simplify operations and optimize utilization (including spot instance use cases for distributed training) \n+* More consistent user experience - UI appearance, features and naming\n+* Improved documentation, tutorials and examples\n+* Stretch - Support for K8s 1.22 and associated dependencies (cert mgr, istio)\n+\n+### Major Features from each Working Group (note: Individual WG versions are independent of Kubeflow's)\n+\n+#### Kubeflow Pipelines, v1.8\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime.\n+\n+#### Katib, v0.13 \n+* Hyperparameter leader election for HA operations and faster recovery\n+* Validation for Early Stopping algorithm settings improves accuracy, reduces overfitting",
        "comment_created_at": "2022-01-29T17:11:39+00:00",
        "comment_author": "jbottum",
        "comment_body": "@andreyvelich do we need the word \"proper\"",
        "pr_file_module": null
      },
      {
        "comment_id": "795191497",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6266,
        "pr_file": "ROADMAP.md",
        "discussion_id": "794906792",
        "commented_code": "@@ -1,10 +1,54 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.5 Release, Due: February 2022\n-* Kubeflow 1.5 timeline is tracked in [#538](https://github.com/kubeflow/community/pull/538)\n-* Additional details will be posted in early 1Q'22\n+## Kubeflow 1.5 Release, Due: March 2022\n+* Kubeflow 1.5 [milestones and timeline](https://github.com/kubeflow/community/pull/538)\n+\n+### Themes\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime\n+* Improve model accuracy and reduce overfitting, especially with hyper parameter tuning\n+* Simplify operations and optimize utilization (including spot instance use cases for distributed training) \n+* More consistent user experience - UI appearance, features and naming\n+* Improved documentation, tutorials and examples\n+* Stretch - Support for K8s 1.22 and associated dependencies (cert mgr, istio)\n+\n+### Major Features from each Working Group (note: Individual WG versions are independent of Kubeflow's)\n+\n+#### Kubeflow Pipelines, v1.8\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime.\n+\n+#### Katib, v0.13 \n+* Hyperparameter leader election for HA operations and faster recovery\n+* Validation for Early Stopping algorithm settings improves accuracy, reduces overfitting",
        "comment_created_at": "2022-01-30T14:38:59+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "@jbottum Basically, validation helps to avoid user's errors and mistakes in APIs when they use Early Stopping.\r\nThat is why I was thinking about this change.",
        "pr_file_module": null
      },
      {
        "comment_id": "795214523",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6266,
        "pr_file": "ROADMAP.md",
        "discussion_id": "794906792",
        "commented_code": "@@ -1,10 +1,54 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.5 Release, Due: February 2022\n-* Kubeflow 1.5 timeline is tracked in [#538](https://github.com/kubeflow/community/pull/538)\n-* Additional details will be posted in early 1Q'22\n+## Kubeflow 1.5 Release, Due: March 2022\n+* Kubeflow 1.5 [milestones and timeline](https://github.com/kubeflow/community/pull/538)\n+\n+### Themes\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime\n+* Improve model accuracy and reduce overfitting, especially with hyper parameter tuning\n+* Simplify operations and optimize utilization (including spot instance use cases for distributed training) \n+* More consistent user experience - UI appearance, features and naming\n+* Improved documentation, tutorials and examples\n+* Stretch - Support for K8s 1.22 and associated dependencies (cert mgr, istio)\n+\n+### Major Features from each Working Group (note: Individual WG versions are independent of Kubeflow's)\n+\n+#### Kubeflow Pipelines, v1.8\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime.\n+\n+#### Katib, v0.13 \n+* Hyperparameter leader election for HA operations and faster recovery\n+* Validation for Early Stopping algorithm settings improves accuracy, reduces overfitting",
        "comment_created_at": "2022-01-30T16:59:53+00:00",
        "comment_author": "jbottum",
        "comment_body": "@jbottum understand but I am not sure this correct - helps users to **proper** reduce model overfitting....shouldn't it read...helps users to reduce model overfitting ?",
        "pr_file_module": null
      },
      {
        "comment_id": "796063923",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6266,
        "pr_file": "ROADMAP.md",
        "discussion_id": "794906792",
        "commented_code": "@@ -1,10 +1,54 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.5 Release, Due: February 2022\n-* Kubeflow 1.5 timeline is tracked in [#538](https://github.com/kubeflow/community/pull/538)\n-* Additional details will be posted in early 1Q'22\n+## Kubeflow 1.5 Release, Due: March 2022\n+* Kubeflow 1.5 [milestones and timeline](https://github.com/kubeflow/community/pull/538)\n+\n+### Themes\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime\n+* Improve model accuracy and reduce overfitting, especially with hyper parameter tuning\n+* Simplify operations and optimize utilization (including spot instance use cases for distributed training) \n+* More consistent user experience - UI appearance, features and naming\n+* Improved documentation, tutorials and examples\n+* Stretch - Support for K8s 1.22 and associated dependencies (cert mgr, istio)\n+\n+### Major Features from each Working Group (note: Individual WG versions are independent of Kubeflow's)\n+\n+#### Kubeflow Pipelines, v1.8\n+* Switching to [Emissary executor](https://www.kubeflow.org/docs/components/pipelines/installation/choose-executor/#emissary-executor) enables Kubeflow Pipelines deployment on Kubernetes >= v1.20, which runs on containerd runtime instead of Docker runtime.\n+\n+#### Katib, v0.13 \n+* Hyperparameter leader election for HA operations and faster recovery\n+* Validation for Early Stopping algorithm settings improves accuracy, reduces overfitting",
        "comment_created_at": "2022-01-31T21:06:12+00:00",
        "comment_author": "jbottum",
        "comment_body": "@andreyvelich I put this in another commit lower down, need to move this forward.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1022650192",
    "pr_number": 6705,
    "pr_file": "ROADMAP.md",
    "created_at": "2022-11-15T11:02:56+00:00",
    "commented_code": "# Kubeflow Roadmap\n\n## Kubeflow 1.7 Release - planning now in process \n* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n## Kubeflow 1.7 Release, Planned: March 2023 \nThe Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n\nNotable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n* Support for Kubernetes 1.25\n* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n* Delivery of KFP V2 beta with its new front-end, backend and SDK \n* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "1022650192",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-15T11:02:56+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "I think, we should remove this part for Katib also.\r\n\r\nMaybe we can add the following:\r\n- Simplified creation of Katib and Training Operator experiments using SDKs.\r\n\r\nAny other items that we certainly will deliver in KF 1.7 @kubeflow/wg-training-leads @tenzen-y @anencore94 ?\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1022881155",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-15T14:45:50+00:00",
        "comment_author": "jbottum",
        "comment_body": "@andreyvelich I have incorporated this update.",
        "pr_file_module": null
      },
      {
        "comment_id": "1023583120",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-16T07:15:52+00:00",
        "comment_author": "tenzen-y",
        "comment_body": "I have no items.",
        "pr_file_module": null
      },
      {
        "comment_id": "1024303442",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-16T17:31:13+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "@jbottum We discussed on today's AutoML community meeting that we want to promote a few Katib UI changes as part of Kubeflow 1.7 ROADMAP. \r\nCan we indicate the most significant improvements/changes for the user that we will deliver in 1.7 ?\r\n@kimwnasptd @johnugeorge What Katib UI changes do we want on the ROADMAP that we deliver ?",
        "pr_file_module": null
      },
      {
        "comment_id": "1024383796",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-16T18:45:55+00:00",
        "comment_author": "johnugeorge",
        "comment_body": "Expose trial logs(https://github.com/kubeflow/katib/issues/971 )\r\nFiltering, Sorting trial list(https://github.com/kubeflow/katib/issues/1441 )",
        "pr_file_module": null
      },
      {
        "comment_id": "1024558646",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-16T22:14:08+00:00",
        "comment_author": "jbottum",
        "comment_body": "@andreyvelich @johnugeorge I have added line 13 to include these feature candidates in the roadmap.   Please provide looks good or comments.   thanks.",
        "pr_file_module": null
      },
      {
        "comment_id": "1025136550",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-17T12:38:21+00:00",
        "comment_author": "andreyvelich",
        "comment_body": "Thank you @jbottum. LGTM",
        "pr_file_module": null
      },
      {
        "comment_id": "1025630075",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 6705,
        "pr_file": "ROADMAP.md",
        "discussion_id": "1022650192",
        "commented_code": "@@ -1,7 +1,18 @@\n # Kubeflow Roadmap\n \n-## Kubeflow 1.7 Release - planning now in process \n-* Please join the Kubeflow Community Meetings on Tuesdays for updates and for opportunities to contribute.  \n+## Kubeflow 1.7 Release, Planned: March 2023 \n+The Kubeflow Community plans to deliver its v1.7 release in March 2023, per this [timeline](https://github.com/kubeflow/community/pull/573).   The high level deliveries are being tracked in this [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1).   The v1.7 release process will be managed by the v1.7 [Release Team](https://github.com/kubeflow/internal-acls/pull/576) using the best practices in the [Release Handbook](https://github.com/kubeflow/community/blob/master/releases/handbook.md)\n+\n+Notable feature candidates in the [Project Board](https://github.com/orgs/kubeflow/projects/50/views/1) are:\n+* Support for Kubernetes 1.25\n+* Improved user isolation especially for the Kubeflow pipelines user interface, database, and artifacts\n+* Update Kubeflow Noteboks naming from Notebooks to Workbenches\n+* Delivery of KFP V2 beta with its new front-end, backend and SDK \n+* New, time saving workflows to simplify data exchange from Katib to Kubeflow Pipelines",
        "comment_created_at": "2022-11-17T19:42:25+00:00",
        "comment_author": "johnugeorge",
        "comment_body": "LGTM ",
        "pr_file_module": null
      }
    ]
  }
]
