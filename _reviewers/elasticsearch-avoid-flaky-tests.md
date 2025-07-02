---
title: Avoid flaky tests
description: Design tests to be deterministic and reliable across different environments.
  Tests that occasionally fail due to timing, race conditions, or environmental differences
  waste development time and reduce confidence in the test suite.
repository: elastic/elasticsearch
label: Testing
language: Yaml
comments_count: 2
repository_stars: 73104
---

Design tests to be deterministic and reliable across different environments. Tests that occasionally fail due to timing, race conditions, or environmental differences waste development time and reduce confidence in the test suite.

When testing values that may vary based on environment conditions (like scores influenced by shard counts), use relative comparisons, before/after validations, or approximation matchers rather than exact values:

```yaml
# Instead of relying on exact scores which can vary:
- match: { hits.hits.0._score: 1.8918664 }

# Better - validate scores are different before/after modification:
- do:
    search:
      index: test-index
      body:
        query:
          match:
            field: "query text"
- set: { hits.hits.0._score: base_score }

- do:
    search:
      index: test-index
      body:
        query:
          match:
            field: 
              query: "query text"
              boost: 5.0
- gt: { hits.hits.0._score: $base_score }
```

Avoid "hacky" approaches that depend on timing. Instead, focus on testing that functionality exists without creating timing dependencies:

```yaml
# Avoid unreliable wait mechanisms:
- do:
    catch: request_timeout
    cluster.health:
      wait_for_nodes: 10
      timeout: "2s"

# Better - verify functionality exists without timing dependencies:
- do:
    cat.shards:
      index: foo
      h: refresh.is_search_idle
- match:
    $body: /^(false|true)\s*\n?$/
```


[
  {
    "discussion_id": "2145028439",
    "pr_number": 129282,
    "pr_file": "x-pack/plugin/inference/src/yamlRestTest/resources/rest-api-spec/test/inference/45_semantic_text_match.yml",
    "created_at": "2025-06-13T12:51:01+00:00",
    "commented_code": "query: \"inference test\"\n\n  - match: { hits.total.value: 0 }\n\n---\n\"Apply boost and query name\":\n  - requires:\n      cluster_features: \"semantic_text.query_rewrite.boost_and_query_name_fix\"\n      reason: fix boosting and query name for semantic text match queries.\n\n  - skip:\n      features: [ \"headers\", \"close_to\" ]\n\n  - do:\n      index:\n        index: test-sparse-index\n        id: doc_1\n        body:\n          inference_field: [ \"inference test\", \"another inference test\" ]\n          non_inference_field: \"non inference test\"\n        refresh: true\n\n  - do:\n      headers:\n        # Force JSON content type so that we use a parser that interprets the floating-point score as a double\n        Content-Type: application/json\n      search:\n        index: test-sparse-index\n        body:\n          query:\n            match:\n              inference_field:\n                query: \"inference test\"\n                boost: 5.0\n                _name: i-like-naming-my-queries\n\n  - match: { hits.total.value: 1 }\n  - match: { hits.hits.0._id: \"doc_1\" }\n  - close_to: { hits.hits.0._score: { value: 1.8918664E18, error: 1e15 } }",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2145028439",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129282,
        "pr_file": "x-pack/plugin/inference/src/yamlRestTest/resources/rest-api-spec/test/inference/45_semantic_text_match.yml",
        "discussion_id": "2145028439",
        "commented_code": "@@ -277,3 +277,41 @@ setup:\n                 query: \"inference test\"\n \n   - match: { hits.total.value: 0 }\n+\n+---\n+\"Apply boost and query name\":\n+  - requires:\n+      cluster_features: \"semantic_text.query_rewrite.boost_and_query_name_fix\"\n+      reason: fix boosting and query name for semantic text match queries.\n+\n+  - skip:\n+      features: [ \"headers\", \"close_to\" ]\n+\n+  - do:\n+      index:\n+        index: test-sparse-index\n+        id: doc_1\n+        body:\n+          inference_field: [ \"inference test\", \"another inference test\" ]\n+          non_inference_field: \"non inference test\"\n+        refresh: true\n+\n+  - do:\n+      headers:\n+        # Force JSON content type so that we use a parser that interprets the floating-point score as a double\n+        Content-Type: application/json\n+      search:\n+        index: test-sparse-index\n+        body:\n+          query:\n+            match:\n+              inference_field:\n+                query: \"inference test\"\n+                boost: 5.0\n+                _name: i-like-naming-my-queries\n+\n+  - match: { hits.total.value: 1 }\n+  - match: { hits.hits.0._id: \"doc_1\" }\n+  - close_to: { hits.hits.0._score: { value: 1.8918664E18, error: 1e15 } }",
        "comment_created_at": "2025-06-13T12:51:01+00:00",
        "comment_author": "kderusso",
        "comment_body": "Can you please make sure this won't run into flakey test issues due to different shard counts impacting score? Sometimes this can be an issue with tests especially in serverless.\r\n\r\nAlso for completeness it might be good to check the score before putting the boost in to validate they are different. ",
        "pr_file_module": null
      },
      {
        "comment_id": "2145394209",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129282,
        "pr_file": "x-pack/plugin/inference/src/yamlRestTest/resources/rest-api-spec/test/inference/45_semantic_text_match.yml",
        "discussion_id": "2145028439",
        "commented_code": "@@ -277,3 +277,41 @@ setup:\n                 query: \"inference test\"\n \n   - match: { hits.total.value: 0 }\n+\n+---\n+\"Apply boost and query name\":\n+  - requires:\n+      cluster_features: \"semantic_text.query_rewrite.boost_and_query_name_fix\"\n+      reason: fix boosting and query name for semantic text match queries.\n+\n+  - skip:\n+      features: [ \"headers\", \"close_to\" ]\n+\n+  - do:\n+      index:\n+        index: test-sparse-index\n+        id: doc_1\n+        body:\n+          inference_field: [ \"inference test\", \"another inference test\" ]\n+          non_inference_field: \"non inference test\"\n+        refresh: true\n+\n+  - do:\n+      headers:\n+        # Force JSON content type so that we use a parser that interprets the floating-point score as a double\n+        Content-Type: application/json\n+      search:\n+        index: test-sparse-index\n+        body:\n+          query:\n+            match:\n+              inference_field:\n+                query: \"inference test\"\n+                boost: 5.0\n+                _name: i-like-naming-my-queries\n+\n+  - match: { hits.total.value: 1 }\n+  - match: { hits.hits.0._id: \"doc_1\" }\n+  - close_to: { hits.hits.0._score: { value: 1.8918664E18, error: 1e15 } }",
        "comment_created_at": "2025-06-13T15:47:10+00:00",
        "comment_author": "Samiul-TheSoccerFan",
        "comment_body": "Good point, thank you. I did validate the scores locally, but you are right that this is not currently reflected in the YAML tests. I will update the tests to include both boosted and unboosted queries to make the difference explicit.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1678832153",
    "pr_number": 110857,
    "pr_file": "rest-api-spec/src/yamlRestTest/resources/rest-api-spec/test/cat.shards/10_basic.yml",
    "created_at": "2024-07-16T06:34:06+00:00",
    "commented_code": "- match:\n      $body: /foo \\s+ 1\\n/\n---\n\"Test cat shards with change in idle state\":\n  - requires:\n      cluster_features: [ \"gte_v8.16.0\" ]\n      reason: search idle state was added in 8.16.0\n\n  - do:\n      indices.create:\n        index: foo\n        body:\n          settings:\n            number_of_shards: \"1\"\n            number_of_replicas: \"0\"\n            search.idle.after: \"1s\"\n\n  - do:\n      index:\n        index: foo\n        body: { test: foo }\n\n  - do:\n      cat.shards:\n        index: foo\n        v: false\n        h: refresh.is_search_idle\n\n  - match:\n      $body: |\n        /^(false \\n?)$/\n\n# very hacky way of sleeping\n  - do:\n      catch: request_timeout\n      cluster.health:\n        wait_for_nodes: 10\n        timeout: \"2s\"",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1678832153",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 110857,
        "pr_file": "rest-api-spec/src/yamlRestTest/resources/rest-api-spec/test/cat.shards/10_basic.yml",
        "discussion_id": "1678832153",
        "commented_code": "@@ -267,3 +267,49 @@\n \n   - match:\n       $body: /foo \\s+ 1\\n/\n+---\n+\"Test cat shards with change in idle state\":\n+  - requires:\n+      cluster_features: [ \"gte_v8.16.0\" ]\n+      reason: search idle state was added in 8.16.0\n+\n+  - do:\n+      indices.create:\n+        index: foo\n+        body:\n+          settings:\n+            number_of_shards: \"1\"\n+            number_of_replicas: \"0\"\n+            search.idle.after: \"1s\"\n+\n+  - do:\n+      index:\n+        index: foo\n+        body: { test: foo }\n+\n+  - do:\n+      cat.shards:\n+        index: foo\n+        v: false\n+        h: refresh.is_search_idle\n+\n+  - match:\n+      $body: |\n+        /^(false \\n?)$/\n+\n+# very hacky way of sleeping\n+  - do:\n+      catch: request_timeout\n+      cluster.health:\n+        wait_for_nodes: 10\n+        timeout: \"2s\"",
        "comment_created_at": "2024-07-16T06:34:06+00:00",
        "comment_author": "DaveCTurner",
        "comment_body": "Yeah I don't think we need this hack (and I worry that it'll be quite a flaky test in practice). In a YAML test we really just need to verify that the column exists at all.",
        "pr_file_module": null
      },
      {
        "comment_id": "1679017815",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 110857,
        "pr_file": "rest-api-spec/src/yamlRestTest/resources/rest-api-spec/test/cat.shards/10_basic.yml",
        "discussion_id": "1678832153",
        "commented_code": "@@ -267,3 +267,49 @@\n \n   - match:\n       $body: /foo \\s+ 1\\n/\n+---\n+\"Test cat shards with change in idle state\":\n+  - requires:\n+      cluster_features: [ \"gte_v8.16.0\" ]\n+      reason: search idle state was added in 8.16.0\n+\n+  - do:\n+      indices.create:\n+        index: foo\n+        body:\n+          settings:\n+            number_of_shards: \"1\"\n+            number_of_replicas: \"0\"\n+            search.idle.after: \"1s\"\n+\n+  - do:\n+      index:\n+        index: foo\n+        body: { test: foo }\n+\n+  - do:\n+      cat.shards:\n+        index: foo\n+        v: false\n+        h: refresh.is_search_idle\n+\n+  - match:\n+      $body: |\n+        /^(false \\n?)$/\n+\n+# very hacky way of sleeping\n+  - do:\n+      catch: request_timeout\n+      cluster.health:\n+        wait_for_nodes: 10\n+        timeout: \"2s\"",
        "comment_created_at": "2024-07-16T08:55:34+00:00",
        "comment_author": "limotova",
        "comment_body": "\ud83d\udc4d\r\nThe first test in this file checks for that I believe",
        "pr_file_module": null
      }
    ]
  }
]
