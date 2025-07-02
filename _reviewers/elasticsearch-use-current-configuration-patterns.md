---
title: Use current configuration patterns
description: 'Always use the current recommended configuration patterns for your project,
  avoiding deprecated approaches. When configuring tests, features, or resource access:'
repository: elastic/elasticsearch
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 73104
---

Always use the current recommended configuration patterns for your project, avoiding deprecated approaches. When configuring tests, features, or resource access:

1. For test requirements, prefer capability-based specifications over version-based skipping:
```yaml
# Instead of:
requires:
  cluster_features: ["gte_v9.1.0"]
  
# Use:
requires:
  test_runner_features: [capabilities]
  capabilities:
    - method: DELETE
      path: /{index}/_block/{block}
```

2. For resource access configurations, be precise about paths and understand the available options:
```yaml
# Be specific with paths:
files:
  - relative_path_setting: "reindex.ssl.certificate"
  
# Consider whether glob patterns are appropriate:
files:
  - relative_path_setting: "reindex.ssl.*"
```

Using current configuration patterns improves maintainability, compatibility, and ensures the system behaves as expected across environments.


[
  {
    "discussion_id": "2144994545",
    "pr_number": 129128,
    "pr_file": "rest-api-spec/src/yamlRestTest/resources/rest-api-spec/test/indices.blocks/10_basic.yml",
    "created_at": "2025-06-13T12:30:00+00:00",
    "commented_code": "index: test_index\n        body:\n          index.blocks.write: false\n\n---\n\"Test removing block via remove_block API\":\n  - requires:\n      cluster_features: [\"gte_v9.1.0\"]\n      reason:  \"index block APIs have only been made available in 9.1.0\"",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2144994545",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129128,
        "pr_file": "rest-api-spec/src/yamlRestTest/resources/rest-api-spec/test/indices.blocks/10_basic.yml",
        "discussion_id": "2144994545",
        "commented_code": "@@ -28,3 +28,43 @@\n         index: test_index\n         body:\n           index.blocks.write: false\n+\n+---\n+\"Test removing block via remove_block API\":\n+  - requires:\n+      cluster_features: [\"gte_v9.1.0\"]\n+      reason:  \"index block APIs have only been made available in 9.1.0\"",
        "comment_created_at": "2025-06-13T12:30:00+00:00",
        "comment_author": "nielsbauman",
        "comment_body": "Skipping tests based on cluster versions is no longer supported.\r\n```suggestion\r\n      test_runner_features: [capabilities]\r\n      reason:  \"index block APIs have only been made available in 9.1.0\"\r\n      capabilities:\r\n        - method: DELETE\r\n          path: /{index}/_block/{block}\r\n\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1973437329",
    "pr_number": 123599,
    "pr_file": "modules/reindex/src/main/plugin-metadata/entitlement-policy.yaml",
    "created_at": "2025-02-27T11:58:07+00:00",
    "commented_code": "ALL-UNNAMED:\n  - manage_threads\n  - outbound_network\n  - create_class_loader # needed for Painless to generate runtime classes\n  - files:\n      - relative_path: \"\"\n      - relative_path_setting: \"reindex.ssl.certificate\"",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1973437329",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 123599,
        "pr_file": "modules/reindex/src/main/plugin-metadata/entitlement-policy.yaml",
        "discussion_id": "1973437329",
        "commented_code": "@@ -1,7 +1,20 @@\n ALL-UNNAMED:\n   - manage_threads\n   - outbound_network\n+  - create_class_loader # needed for Painless to generate runtime classes\n   - files:\n-      - relative_path: \"\"\n+      - relative_path_setting: \"reindex.ssl.certificate\"",
        "comment_created_at": "2025-02-27T11:58:07+00:00",
        "comment_author": "ldematte",
        "comment_body": "@rjernst I have no idea if I'm using this correctly, as this is the first time we use it I think.\r\nWill this work with exclusive access?\r\nCan I use a glob (reindex.ssl.*) instead?\r\n`certificate_authorities` is a list; will that work with your file settings implementation?",
        "pr_file_module": null
      },
      {
        "comment_id": "1974562173",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 123599,
        "pr_file": "modules/reindex/src/main/plugin-metadata/entitlement-policy.yaml",
        "discussion_id": "1973437329",
        "commented_code": "@@ -1,7 +1,20 @@\n ALL-UNNAMED:\n   - manage_threads\n   - outbound_network\n+  - create_class_loader # needed for Painless to generate runtime classes\n   - files:\n-      - relative_path: \"\"\n+      - relative_path_setting: \"reindex.ssl.certificate\"",
        "comment_created_at": "2025-02-28T00:50:23+00:00",
        "comment_author": "rjernst",
        "comment_body": "It should work if the setting is a list, we resolve all paths, whether for a single setting, or multiple settings. It should also work with exclusive.  Also note the properties are changing per our earlier discussion, see https://github.com/elastic/elasticsearch/pull/123649.\r\n\r\nBut it's curious that we didn't need this before? I guess it would have only worked if it was relative to the config dir.",
        "pr_file_module": null
      },
      {
        "comment_id": "1974902540",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 123599,
        "pr_file": "modules/reindex/src/main/plugin-metadata/entitlement-policy.yaml",
        "discussion_id": "1973437329",
        "commented_code": "@@ -1,7 +1,20 @@\n ALL-UNNAMED:\n   - manage_threads\n   - outbound_network\n+  - create_class_loader # needed for Painless to generate runtime classes\n   - files:\n-      - relative_path: \"\"\n+      - relative_path_setting: \"reindex.ssl.certificate\"",
        "comment_created_at": "2025-02-28T06:57:25+00:00",
        "comment_author": "ldematte",
        "comment_body": "Yes, I think so!",
        "pr_file_module": null
      },
      {
        "comment_id": "1974904628",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 123599,
        "pr_file": "modules/reindex/src/main/plugin-metadata/entitlement-policy.yaml",
        "discussion_id": "1973437329",
        "commented_code": "@@ -1,7 +1,20 @@\n ALL-UNNAMED:\n   - manage_threads\n   - outbound_network\n+  - create_class_loader # needed for Painless to generate runtime classes\n   - files:\n-      - relative_path: \"\"\n+      - relative_path_setting: \"reindex.ssl.certificate\"",
        "comment_created_at": "2025-02-28T06:59:22+00:00",
        "comment_author": "ldematte",
        "comment_body": "> Also note the properties are changing per our earlier discussion, see https://github.com/elastic/elasticsearch/pull/123649.\r\n\r\nThanks! So `reindex.ssl.*` should work? I'll try it/look at logs/debug what it resolves to. Or maybe I'll write a test for it.\r\nI'll update this to use the new properties after that is merged.",
        "pr_file_module": null
      }
    ]
  }
]
