---
title: Scope and document configurations
description: 'When designing and implementing configuration options, carefully consider
  two key aspects:


  1. **Choose appropriate configuration scope**: Place configuration settings at the
  level that makes the most sense for their purpose and usage pattern. Avoid overly
  granular scopes when settings could logically apply at a broader level.'
repository: elastic/elasticsearch
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 73104
---

When designing and implementing configuration options, carefully consider two key aspects:

1. **Choose appropriate configuration scope**: Place configuration settings at the level that makes the most sense for their purpose and usage pattern. Avoid overly granular scopes when settings could logically apply at a broader level.

   ```
   // Prefer index-level settings for behaviors that affect the entire index
   // Example from Discussion 1:
   "early_termination": true   // At index level, not field level
   ```

2. **Document configurations completely**: Provide clear documentation that covers all possible values, edge cases, and boundary conditions. Explicitly state limitations, especially for managed environments where configuration options may be restricted.

   ```
   // Example of improved documentation clarity:
   // Before:
   "50% of total system memory when more than 1 GB, with a maximum of 31 GB."
   
   // After:
   "50% of total system memory when 1 GB or more, with a maximum of 31 GB."
   ```

For managed or restricted environments, clearly explain which configuration options are available to users and why certain configurations might be limited or handled automatically.


[
  {
    "discussion_id": "2157620496",
    "pr_number": 129704,
    "pr_file": "docs/reference/elasticsearch/index-settings/serverless.md",
    "created_at": "2025-06-19T20:23:19+00:00",
    "commented_code": "---\nnavigation_title: Serverless index settings\napplies_to:\n  serverless: all\n---\n\n# Index settings available in {{serverless-full}} projects\n\nThis page lists the {{es}} index settings available in {{serverless-full}} projects.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2157620496",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129704,
        "pr_file": "docs/reference/elasticsearch/index-settings/serverless.md",
        "discussion_id": "2157620496",
        "commented_code": "@@ -0,0 +1,61 @@\n+---\n+navigation_title: Serverless index settings\n+applies_to:\n+  serverless: all\n+---\n+\n+# Index settings available in {{serverless-full}} projects\n+\n+This page lists the {{es}} index settings available in {{serverless-full}} projects.",
        "comment_created_at": "2025-06-19T20:23:19+00:00",
        "comment_author": "shainaraskas",
        "comment_body": "```suggestion\r\n[{{serverless-full}}](docs-content://deploy-manage/deploy/elastic-cloud/serverless.md) manages most index settings for you. This page lists the {{es}} index settings available in {{serverless-short}} projects.\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2159581100",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129704,
        "pr_file": "docs/reference/elasticsearch/index-settings/serverless.md",
        "discussion_id": "2157620496",
        "commented_code": "@@ -0,0 +1,61 @@\n+---\n+navigation_title: Serverless index settings\n+applies_to:\n+  serverless: all\n+---\n+\n+# Index settings available in {{serverless-full}} projects\n+\n+This page lists the {{es}} index settings available in {{serverless-full}} projects.",
        "comment_created_at": "2025-06-20T19:50:31+00:00",
        "comment_author": "shainaraskas",
        "comment_body": "I think we probably should just align closely with whatever PM approves in https://github.com/elastic/docs-content/pull/1728 so we don't need an extra round of approvals\r\n\r\nmaybe \r\n\r\n```suggestion\r\nIn {{serverless-full}} projects, configuration available to users is [limited](docs-content://deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md) to certain index-level settings. These restrictions help ensure the reliability of {{serverless-short}} projects.\r\n\r\nThis page lists the {{es}} index settings available in {{serverless-full}} projects.\r\n```\r\n\r\nor \r\n\r\n```suggestion\r\nIn {{serverless-full}} projects, configuration available to users is [limited](docs-content://deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md) to certain index-level settings.\r\n\r\nThis page lists the {{es}} index settings available in {{serverless-full}} projects.\r\n```\r\n\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2172153221",
    "pr_number": 127223,
    "pr_file": "docs/reference/elasticsearch/mapping-reference/dense-vector.md",
    "created_at": "2025-06-27T14:19:42+00:00",
    "commented_code": ":   In case a knn query specifies a `rescore_vector` parameter, the query `rescore_vector` parameter will be used instead.\n    :   See [oversampling and rescoring quantized vectors](docs-content://solutions/search/vector/knn.md#dense-vector-knn-search-rescoring) for details.\n:::::\n\n`early_termination`\n:   (Optional, boolean) Apply _patience_ based early termination strategy to knn queries over HNSW graphs (see [paper](https://cs.uwaterloo.ca/~jimmylin/publications/Teofili_Lin_ECIR2025.pdf)). This is expected to produce Only applicable to `hnsw`, `int8_hnsw`, `int4_hnsw` and `bbq_hnsw` index types.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2172153221",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 127223,
        "pr_file": "docs/reference/elasticsearch/mapping-reference/dense-vector.md",
        "discussion_id": "2172153221",
        "commented_code": "@@ -281,6 +281,9 @@ $$$dense-vector-index-options$$$\n     :   In case a knn query specifies a `rescore_vector` parameter, the query `rescore_vector` parameter will be used instead.\n     :   See [oversampling and rescoring quantized vectors](docs-content://solutions/search/vector/knn.md#dense-vector-knn-search-rescoring) for details.\n :::::\n+\n+`early_termination`\n+:   (Optional, boolean) Apply _patience_ based early termination strategy to knn queries over HNSW graphs (see [paper](https://cs.uwaterloo.ca/~jimmylin/publications/Teofili_Lin_ECIR2025.pdf)). This is expected to produce Only applicable to `hnsw`, `int8_hnsw`, `int4_hnsw` and `bbq_hnsw` index types.",
        "comment_created_at": "2025-06-27T14:19:42+00:00",
        "comment_author": "benwtrent",
        "comment_body": "I think this should be an index wide setting if possible. It can be dynamic there since its query time only, but having it per vector field seems like too much.",
        "pr_file_module": null
      },
      {
        "comment_id": "2172360995",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 127223,
        "pr_file": "docs/reference/elasticsearch/mapping-reference/dense-vector.md",
        "discussion_id": "2172153221",
        "commented_code": "@@ -281,6 +281,9 @@ $$$dense-vector-index-options$$$\n     :   In case a knn query specifies a `rescore_vector` parameter, the query `rescore_vector` parameter will be used instead.\n     :   See [oversampling and rescoring quantized vectors](docs-content://solutions/search/vector/knn.md#dense-vector-knn-search-rescoring) for details.\n :::::\n+\n+`early_termination`\n+:   (Optional, boolean) Apply _patience_ based early termination strategy to knn queries over HNSW graphs (see [paper](https://cs.uwaterloo.ca/~jimmylin/publications/Teofili_Lin_ECIR2025.pdf)). This is expected to produce Only applicable to `hnsw`, `int8_hnsw`, `int4_hnsw` and `bbq_hnsw` index types.",
        "comment_created_at": "2025-06-27T16:11:20+00:00",
        "comment_author": "tteofili",
        "comment_body": "I can see your point, however I can think of this setting to be either enabled or not either index or field-wise, whereas I don't think users would enable/disable it on a per query basis.",
        "pr_file_module": null
      },
      {
        "comment_id": "2172961695",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 127223,
        "pr_file": "docs/reference/elasticsearch/mapping-reference/dense-vector.md",
        "discussion_id": "2172153221",
        "commented_code": "@@ -281,6 +281,9 @@ $$$dense-vector-index-options$$$\n     :   In case a knn query specifies a `rescore_vector` parameter, the query `rescore_vector` parameter will be used instead.\n     :   See [oversampling and rescoring quantized vectors](docs-content://solutions/search/vector/knn.md#dense-vector-knn-search-rescoring) for details.\n :::::\n+\n+`early_termination`\n+:   (Optional, boolean) Apply _patience_ based early termination strategy to knn queries over HNSW graphs (see [paper](https://cs.uwaterloo.ca/~jimmylin/publications/Teofili_Lin_ECIR2025.pdf)). This is expected to produce Only applicable to `hnsw`, `int8_hnsw`, `int4_hnsw` and `bbq_hnsw` index types.",
        "comment_created_at": "2025-06-27T23:01:24+00:00",
        "comment_author": "benwtrent",
        "comment_body": ">  however I can think of this setting to be either enabled or not either index or field-wise\r\n\r\nI agree, I think it should be done at the index level. I only mention the \"query time\" nature of it to indicate that it can be a dynamic index setting.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2064735069",
    "pr_number": 127482,
    "pr_file": "docs/reference/elasticsearch/jvm-settings.md",
    "created_at": "2025-04-28T21:06:09+00:00",
    "commented_code": "::::\n\n\n## Default JVM heap sizes [default-jvm-sizes]\n\nIf heap sizes are not specifically set, {{es}} will calculate JVM heap sizing based on the total amount of system memory, depending on the node's role.\n\n* Master-only node\n  * 60% of total system memory, up to a maximum of 31 GB.\n* Machine Learning-only node\n  * 40% of the first 16 gigabytes plus 10% of memory above that when total system memory is more than 16 gigabytes, up to a maximum of 31 GB.\n* Data-only node\n  * 40% of total system memory when less than 1 GB, with a minimum of 128 MB.\n  * 50% of total system memory when more than 1 GB, with a maximum of 31 GB.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2064735069",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 127482,
        "pr_file": "docs/reference/elasticsearch/jvm-settings.md",
        "discussion_id": "2064735069",
        "commented_code": "@@ -128,6 +128,18 @@ If you are running {{es}} as a Windows service, you can change the heap size usi\n ::::\n \n \n+## Default JVM heap sizes [default-jvm-sizes]\n+\n+If heap sizes are not specifically set, {{es}} will calculate JVM heap sizing based on the total amount of system memory, depending on the node's role.\n+\n+* Master-only node\n+  * 60% of total system memory, up to a maximum of 31 GB.\n+* Machine Learning-only node\n+  * 40% of the first 16 gigabytes plus 10% of memory above that when total system memory is more than 16 gigabytes, up to a maximum of 31 GB.\n+* Data-only node\n+  * 40% of total system memory when less than 1 GB, with a minimum of 128 MB.\n+  * 50% of total system memory when more than 1 GB, with a maximum of 31 GB.",
        "comment_created_at": "2025-04-28T21:06:09+00:00",
        "comment_author": "Copilot",
        "comment_body": "The documentation for Data-only nodes distinguishes between memory amounts 'less than 1 GB' and 'more than 1 GB', but it does not specify what happens when the node has exactly 1 GB of memory. Consider adding clarification for this edge case.\n```suggestion\n  * 50% of total system memory when 1 GB or more, with a maximum of 31 GB.\n```",
        "pr_file_module": null
      }
    ]
  }
]
