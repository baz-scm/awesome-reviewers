---
title: Consistent separator conventions
description: 'Use appropriate separators in compound identifiers to improve readability
  and ensure naming consistency across the codebase. Specifically:


  1. Use hyphens to separate words in multi-word paths, repository names, and other
  resources:'
repository: kubeflow/kubeflow
label: Naming Conventions
language: Markdown
comments_count: 2
repository_stars: 15064
---

Use appropriate separators in compound identifiers to improve readability and ensure naming consistency across the codebase. Specifically:

1. Use hyphens to separate words in multi-word paths, repository names, and other resources:
   - Correct: `wg-deployment`, `feature-name`
   - Incorrect: `wgdeployment`, `featurename`

2. For version references, use the "vX.Y" format consistently:
   - Correct: `v1.0`, `v2.3`
   - Avoid: `0.Y`, `1.0` (without v prefix)

This practice makes identifiers more readable, maintains consistency with standard conventions, and helps ensure references remain valid over time as the codebase evolves. Consistent naming patterns reduce the need for future refactoring and make documentation more predictable and easier to navigate.


[
  {
    "discussion_id": "540654806",
    "pr_number": 5430,
    "pr_file": "README.md",
    "created_at": "2020-12-11T03:01:05+00:00",
    "commented_code": "<img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\nKubeflow is a Cloud Native platform for machine learning based on Google\u2019s internal machine learning pipelines.\nKubeflow the cloud-native platform for machine learning operations - pipelines, training and deployment.\n\n---\nPlease refer to the official docs at [kubeflow.org](http://kubeflow.org).\n\n## Working Groups\nThe Kubeflow community is organized into working groups (WGs) with associated repositories, that focus on specific pieces of the ML platform. \n\n* [AutoML](https://github.com/kubeflow/community/tree/master/wg-automl)\n* [Deployment](https://github.com/kubeflow/community/tree/master/wgdeployment)\n* [Manifests](https://github.com/kubeflow/community/tree/master/wg-manifests)",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "540654806",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5430,
        "pr_file": "README.md",
        "discussion_id": "540654806",
        "commented_code": "@@ -1,9 +1,19 @@\n <img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n-Kubeflow is a Cloud Native platform for machine learning based on Google\u2019s internal machine learning pipelines.\n+Kubeflow the cloud-native platform for machine learning operations - pipelines, training and deployment.\n \n ---\n Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n \n+## Working Groups\n+The Kubeflow community is organized into working groups (WGs) with associated repositories, that focus on specific pieces of the ML platform. \n+\n+* [AutoML](https://github.com/kubeflow/community/tree/master/wg-automl)\n+* [Deployment](https://github.com/kubeflow/community/tree/master/wgdeployment)\n+* [Manifests](https://github.com/kubeflow/community/tree/master/wg-manifests)",
        "comment_created_at": "2020-12-11T03:01:05+00:00",
        "comment_author": "PatrickXYS",
        "comment_body": "We need to update those links to make sure they can persist for a long time without going back and forth to fix it.",
        "pr_file_module": null
      },
      {
        "comment_id": "542447900",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5430,
        "pr_file": "README.md",
        "discussion_id": "540654806",
        "commented_code": "@@ -1,9 +1,19 @@\n <img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n-Kubeflow is a Cloud Native platform for machine learning based on Google\u2019s internal machine learning pipelines.\n+Kubeflow the cloud-native platform for machine learning operations - pipelines, training and deployment.\n \n ---\n Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n \n+## Working Groups\n+The Kubeflow community is organized into working groups (WGs) with associated repositories, that focus on specific pieces of the ML platform. \n+\n+* [AutoML](https://github.com/kubeflow/community/tree/master/wg-automl)\n+* [Deployment](https://github.com/kubeflow/community/tree/master/wgdeployment)\n+* [Manifests](https://github.com/kubeflow/community/tree/master/wg-manifests)",
        "comment_created_at": "2020-12-14T14:56:32+00:00",
        "comment_author": "rui-vas",
        "comment_body": "That is a good idea! What would be a good way to do it? ",
        "pr_file_module": null
      },
      {
        "comment_id": "543062959",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5430,
        "pr_file": "README.md",
        "discussion_id": "540654806",
        "commented_code": "@@ -1,9 +1,19 @@\n <img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n-Kubeflow is a Cloud Native platform for machine learning based on Google\u2019s internal machine learning pipelines.\n+Kubeflow the cloud-native platform for machine learning operations - pipelines, training and deployment.\n \n ---\n Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n \n+## Working Groups\n+The Kubeflow community is organized into working groups (WGs) with associated repositories, that focus on specific pieces of the ML platform. \n+\n+* [AutoML](https://github.com/kubeflow/community/tree/master/wg-automl)\n+* [Deployment](https://github.com/kubeflow/community/tree/master/wgdeployment)\n+* [Manifests](https://github.com/kubeflow/community/tree/master/wg-manifests)",
        "comment_created_at": "2020-12-15T05:44:38+00:00",
        "comment_author": "Bobgy",
        "comment_body": "The current links look right. kubeflow/community/master is the long term location",
        "pr_file_module": null
      },
      {
        "comment_id": "551420552",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 5430,
        "pr_file": "README.md",
        "discussion_id": "540654806",
        "commented_code": "@@ -1,9 +1,19 @@\n <img src=\"https://www.kubeflow.org/images/logo.svg\" width=\"100\">\n-Kubeflow is a Cloud Native platform for machine learning based on Google\u2019s internal machine learning pipelines.\n+Kubeflow the cloud-native platform for machine learning operations - pipelines, training and deployment.\n \n ---\n Please refer to the official docs at [kubeflow.org](http://kubeflow.org).\n \n+## Working Groups\n+The Kubeflow community is organized into working groups (WGs) with associated repositories, that focus on specific pieces of the ML platform. \n+\n+* [AutoML](https://github.com/kubeflow/community/tree/master/wg-automl)\n+* [Deployment](https://github.com/kubeflow/community/tree/master/wgdeployment)\n+* [Manifests](https://github.com/kubeflow/community/tree/master/wg-manifests)",
        "comment_created_at": "2021-01-04T16:23:47+00:00",
        "comment_author": "PatrickXYS",
        "comment_body": "> * [Deployment] (https://github.com/kubeflow/community/tree/master/wgdeployment)\r\n\r\nThis is not correct, can we make it with a dash? `wg-deployment`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "375242639",
    "pr_number": 4717,
    "pr_file": "docs_dev/releasing.md",
    "created_at": "2020-02-05T13:05:26+00:00",
    "commented_code": "```\n   * Set the tag to be the correct version for the tag.\n\n## Version the website\n# Version the website\n\nThe main Kubeflow website at [www.kubeflow.org](www.kubeflow.org) points to the\n**master** branch of the `kubeflow/website` repo. Similarly, \n[master.kubeflow.org](https://master.kubeflow.org/) also points to the master\nbranch.\nversion of the website we want users to see.\n\n* Most of the time this will correspond to the **master** branch of the `kubeflow/website` repo\n\n* However, leading up to a minor release (0.Y) [www.kubeflow.org](www.kubeflow.org)",
    "repo_full_name": "kubeflow/kubeflow",
    "discussion_comments": [
      {
        "comment_id": "375242639",
        "repo_full_name": "kubeflow/kubeflow",
        "pr_number": 4717,
        "pr_file": "docs_dev/releasing.md",
        "discussion_id": "375242639",
        "commented_code": "@@ -179,27 +185,47 @@ Alternatively you can use the UI.\n    ```\n    * Set the tag to be the correct version for the tag.\n \n-## Version the website\n+# Version the website\n \n The main Kubeflow website at [www.kubeflow.org](www.kubeflow.org) points to the\n-**master** branch of the `kubeflow/website` repo. Similarly, \n-[master.kubeflow.org](https://master.kubeflow.org/) also points to the master\n-branch.\n+version of the website we want users to see.\n+\n+* Most of the time this will correspond to the **master** branch of the `kubeflow/website` repo\n+\n+* However, leading up to a minor release (0.Y) [www.kubeflow.org](www.kubeflow.org) ",
        "comment_created_at": "2020-02-05T13:05:26+00:00",
        "comment_author": "sarahmaddox",
        "comment_body": "Should we change `0.Y` to `vX.Y`? (Because soon the `0` will not mean much, as we've moving to v1.) Also, `vX.Y` is consistent with the section \"Creating and publishing a website branch for vX.Y\".)",
        "pr_file_module": null
      }
    ]
  }
]
