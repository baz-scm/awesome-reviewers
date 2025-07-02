---
title: Specify explicit REST formats
description: 'Always specify explicit request formats in REST API tests rather than
  relying on default behaviors. This includes:


  1. Set appropriate Content-Type headers (typically application/json for REST APIs) '
repository: elastic/elasticsearch
label: API
language: Yaml
comments_count: 2
repository_stars: 73104
---

Always specify explicit request formats in REST API tests rather than relying on default behaviors. This includes:

1. Set appropriate Content-Type headers (typically application/json for REST APIs) 
2. Define explicit query parameters that clearly test intended functionality

Without proper format specifications, tests may fail unexpectedly or test incorrect behaviors. For example, missing Content-Type headers might cause an endpoint to default to different formats like cbor instead of JSON:

```yaml
- do:
    headers:
      Content-Type: application/json  # Explicitly specify format
    index:
      index: test
      id: 1
      body: { "field": "value" }
```

Similarly, when testing query parameters, be explicit about the expected behavior rather than using generic queries that might not fully test the intended functionality:

```yaml
retriever:
  standard:
    query:
      match_none: {}  # Explicitly testing empty results case
```

This practice improves test reliability and clarity by making the expected request format visible and intentional rather than implicit.


[
  {
    "discussion_id": "2179929463",
    "pr_number": 130325,
    "pr_file": "modules/ingest-common/src/yamlRestTest/resources/rest-api-spec/test/ingest/120_grok.yml",
    "created_at": "2025-07-02T12:29:26+00:00",
    "commented_code": "ingest.processor_grok: {}\n  - length: { patterns: 318 }\n  - match: { patterns.PATH: \"(?:%{UNIXPATH}|%{WINPATH})\" }\n\n\n---\n\"Test simulate with invalid GROK pattern\":\n  - skip:\n        features: headers\n  - do:\n      catch: bad_request\n      headers:\n        Content-Type: application/json",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2179929463",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130325,
        "pr_file": "modules/ingest-common/src/yamlRestTest/resources/rest-api-spec/test/ingest/120_grok.yml",
        "discussion_id": "2179929463",
        "commented_code": "@@ -154,3 +154,45 @@ teardown:\n       ingest.processor_grok: {}\n   - length: { patterns: 318 }\n   - match: { patterns.PATH: \"(?:%{UNIXPATH}|%{WINPATH})\" }\n+\n+\n+---\n+\"Test simulate with invalid GROK pattern\":\n+  - skip:\n+        features: headers\n+  - do:\n+      catch: bad_request\n+      headers:\n+        Content-Type: application/json",
        "comment_created_at": "2025-07-02T12:29:26+00:00",
        "comment_author": "szybia",
        "comment_body": "re. headers: existing `simulate.ingest` REST tests have skip and send a content-type header.\r\n\r\ntest either doesn't run or breaks without this, it seems without it the endpoint expects cbor by default.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2180109441",
    "pr_number": 130402,
    "pr_file": "x-pack/plugin/rank-rrf/src/yamlRestTest/resources/rest-api-spec/test/rrf/950_pinned_interaction.yml",
    "created_at": "2025-07-02T13:45:39+00:00",
    "commented_code": "retriever:\n            rrf:\n              retrievers:\n                -\n                  standard:\n                    query:\n                      match: { text: \"document\" }\n                -\n                  pinned:\n                    ids: [\"doc4\", \"doc5\"]\n                    retriever:\n                      standard:\n                        query:\n                          match: { text: \"document\" }\n\n  - match: { hits.total.value: 5 }\n  - match: { hits.hits.0._id: doc1 }\n  - lt: { hits.hits.0._score: 100.0 }\n  - match: { hits.hits.1._id: doc4 }\n  - match: { hits.hits.2._id: doc5 }\n                          match_none: {}",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2180109441",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130402,
        "pr_file": "x-pack/plugin/rank-rrf/src/yamlRestTest/resources/rest-api-spec/test/rrf/950_pinned_interaction.yml",
        "discussion_id": "2180109441",
        "commented_code": "@@ -77,22 +77,15 @@ setup:\n           retriever:\n             rrf:\n               retrievers:\n-                -\n-                  standard:\n-                    query:\n-                      match: { text: \"document\" }\n                 -\n                   pinned:\n                     ids: [\"doc4\", \"doc5\"]\n                     retriever:\n                       standard:\n                         query:\n-                          match: { text: \"document\" }\n-\n-  - match: { hits.total.value: 5 }\n-  - match: { hits.hits.0._id: doc1 }\n-  - lt: { hits.hits.0._score: 100.0 }\n-  - match: { hits.hits.1._id: doc4 }\n-  - match: { hits.hits.2._id: doc5 }\n+                          match_none: {}",
        "comment_created_at": "2025-07-02T13:45:39+00:00",
        "comment_author": "Mikep86",
        "comment_body": "I think @kderusso meant creating an `rrf` retriever with two sub-retrievers, one of which is a `match_none` query.",
        "pr_file_module": null
      },
      {
        "comment_id": "2180119064",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130402,
        "pr_file": "x-pack/plugin/rank-rrf/src/yamlRestTest/resources/rest-api-spec/test/rrf/950_pinned_interaction.yml",
        "discussion_id": "2180109441",
        "commented_code": "@@ -77,22 +77,15 @@ setup:\n           retriever:\n             rrf:\n               retrievers:\n-                -\n-                  standard:\n-                    query:\n-                      match: { text: \"document\" }\n                 -\n                   pinned:\n                     ids: [\"doc4\", \"doc5\"]\n                     retriever:\n                       standard:\n                         query:\n-                          match: { text: \"document\" }\n-\n-  - match: { hits.total.value: 5 }\n-  - match: { hits.hits.0._id: doc1 }\n-  - lt: { hits.hits.0._score: 100.0 }\n-  - match: { hits.hits.1._id: doc4 }\n-  - match: { hits.hits.2._id: doc5 }\n+                          match_none: {}",
        "comment_created_at": "2025-07-02T13:49:43+00:00",
        "comment_author": "mridula-s109",
        "comment_body": "Oh okays, looking into it.",
        "pr_file_module": null
      },
      {
        "comment_id": "2180145926",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130402,
        "pr_file": "x-pack/plugin/rank-rrf/src/yamlRestTest/resources/rest-api-spec/test/rrf/950_pinned_interaction.yml",
        "discussion_id": "2180109441",
        "commented_code": "@@ -77,22 +77,15 @@ setup:\n           retriever:\n             rrf:\n               retrievers:\n-                -\n-                  standard:\n-                    query:\n-                      match: { text: \"document\" }\n                 -\n                   pinned:\n                     ids: [\"doc4\", \"doc5\"]\n                     retriever:\n                       standard:\n                         query:\n-                          match: { text: \"document\" }\n-\n-  - match: { hits.total.value: 5 }\n-  - match: { hits.hits.0._id: doc1 }\n-  - lt: { hits.hits.0._score: 100.0 }\n-  - match: { hits.hits.1._id: doc4 }\n-  - match: { hits.hits.2._id: doc5 }\n+                          match_none: {}",
        "comment_created_at": "2025-07-02T14:01:08+00:00",
        "comment_author": "mridula-s109",
        "comment_body": "have fixed the same.",
        "pr_file_module": null
      }
    ]
  }
]
