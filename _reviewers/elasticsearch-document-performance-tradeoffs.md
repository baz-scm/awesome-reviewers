---
title: Document performance tradeoffs
description: 'Always explicitly document the performance implications of API parameters,
  limit changes, and features that could significantly impact resource usage. When
  introducing functionality that offers a tradeoff between capabilities and performance,
  provide clear warnings and specific details about:'
repository: elastic/elasticsearch
label: Performance Optimization
language: Other
comments_count: 2
repository_stars: 73104
---

Always explicitly document the performance implications of API parameters, limit changes, and features that could significantly impact resource usage. When introducing functionality that offers a tradeoff between capabilities and performance, provide clear warnings and specific details about:

1. Memory consumption impacts
2. Response time implications
3. Scaling considerations for different cluster sizes

For example:

```asciidoc
`include_empty_fields`::
  (Optional, Boolean) If `false`, fields that never had a value in any shards are not included in the response.
  *WARNING*: Setting this parameter to `false` may significantly increase response times on large datasets due to
  additional field existence checks across all documents. Consider using the default value in performance-sensitive
  applications.
```

or

```asciidoc
NOTE: Synonyms sets consume heap memory proportional to their size. While the system supports up to 100,000 
synonym rules per set, large synonym sets may impact query performance and memory usage, especially on smaller
clusters. Monitor heap usage when working with large synonym sets.
```

This practice helps users make informed decisions about performance-sensitive configurations and prevents unexpected resource usage issues in production environments.


[
  {
    "discussion_id": "1627639397",
    "pr_number": 109390,
    "pr_file": "docs/reference/synonyms/apis/put-synonyms-set.asciidoc",
    "created_at": "2024-06-05T12:09:05+00:00",
    "commented_code": "Creates or updates a synonyms set.\n\nNOTE: Synonyms sets are limited to a maximum of 10,000 synonym rules per set.\nSynonym sets with more than 10,000 synonym rules will provide inconsistent search results.\nNOTE: Synonyms sets are limited to a maximum of 100,000 synonym rules per set.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1627639397",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "docs/reference/synonyms/apis/put-synonyms-set.asciidoc",
        "discussion_id": "1627639397",
        "commented_code": "@@ -7,8 +7,7 @@\n \n Creates or updates a synonyms set.\n \n-NOTE: Synonyms sets are limited to a maximum of 10,000 synonym rules per set.\n-Synonym sets with more than 10,000 synonym rules will provide inconsistent search results.\n+NOTE: Synonyms sets are limited to a maximum of 100,000 synonym rules per set.",
        "comment_created_at": "2024-06-05T12:09:05+00:00",
        "comment_author": "pmpailis",
        "comment_body": "Do we expect this increase to allowed rules to have any adverse side-effect in terms of performance? ",
        "pr_file_module": null
      },
      {
        "comment_id": "1629432494",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "docs/reference/synonyms/apis/put-synonyms-set.asciidoc",
        "discussion_id": "1627639397",
        "commented_code": "@@ -7,8 +7,7 @@\n \n Creates or updates a synonyms set.\n \n-NOTE: Synonyms sets are limited to a maximum of 10,000 synonym rules per set.\n-Synonym sets with more than 10,000 synonym rules will provide inconsistent search results.\n+NOTE: Synonyms sets are limited to a maximum of 100,000 synonym rules per set.",
        "comment_created_at": "2024-06-06T12:23:58+00:00",
        "comment_author": "carlosdelest",
        "comment_body": "It will have an impact on heap when retrieving them - I need to perform some testing in order to check that we're not having too much memory usage for small clusters.\r\n\r\nOn non-API related operations, this should be no different than using file-based synonyms - and there's no limit set there.",
        "pr_file_module": null
      },
      {
        "comment_id": "1633470327",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "docs/reference/synonyms/apis/put-synonyms-set.asciidoc",
        "discussion_id": "1627639397",
        "commented_code": "@@ -7,8 +7,7 @@\n \n Creates or updates a synonyms set.\n \n-NOTE: Synonyms sets are limited to a maximum of 10,000 synonym rules per set.\n-Synonym sets with more than 10,000 synonym rules will provide inconsistent search results.\n+NOTE: Synonyms sets are limited to a maximum of 100,000 synonym rules per set.",
        "comment_created_at": "2024-06-10T15:44:34+00:00",
        "comment_author": "kderusso",
        "comment_body": "Should we add a note that we recommend less than 10,000?",
        "pr_file_module": null
      },
      {
        "comment_id": "1633550286",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "docs/reference/synonyms/apis/put-synonyms-set.asciidoc",
        "discussion_id": "1627639397",
        "commented_code": "@@ -7,8 +7,7 @@\n \n Creates or updates a synonyms set.\n \n-NOTE: Synonyms sets are limited to a maximum of 10,000 synonym rules per set.\n-Synonym sets with more than 10,000 synonym rules will provide inconsistent search results.\n+NOTE: Synonyms sets are limited to a maximum of 100,000 synonym rules per set.",
        "comment_created_at": "2024-06-10T16:48:32+00:00",
        "comment_author": "carlosdelest",
        "comment_body": "That makes sense - I'll be adding that.",
        "pr_file_module": null
      },
      {
        "comment_id": "1636546585",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "docs/reference/synonyms/apis/put-synonyms-set.asciidoc",
        "discussion_id": "1627639397",
        "commented_code": "@@ -7,8 +7,7 @@\n \n Creates or updates a synonyms set.\n \n-NOTE: Synonyms sets are limited to a maximum of 10,000 synonym rules per set.\n-Synonym sets with more than 10,000 synonym rules will provide inconsistent search results.\n+NOTE: Synonyms sets are limited to a maximum of 100,000 synonym rules per set.",
        "comment_created_at": "2024-06-12T14:08:12+00:00",
        "comment_author": "carlosdelest",
        "comment_body": "Thinking about this again - I guess we're mainly limited by heap size on this. It's hard to put a limit on this for example and not on file-based synonyms, which would have the same problem.\r\n\r\nI'll try and do some memory usage tests and come back later with a proposal for the users.",
        "pr_file_module": null
      },
      {
        "comment_id": "1650948165",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "docs/reference/synonyms/apis/put-synonyms-set.asciidoc",
        "discussion_id": "1627639397",
        "commented_code": "@@ -7,8 +7,7 @@\n \n Creates or updates a synonyms set.\n \n-NOTE: Synonyms sets are limited to a maximum of 10,000 synonym rules per set.\n-Synonym sets with more than 10,000 synonym rules will provide inconsistent search results.\n+NOTE: Synonyms sets are limited to a maximum of 100,000 synonym rules per set.",
        "comment_created_at": "2024-06-24T12:27:14+00:00",
        "comment_author": "mayya-sharipova",
        "comment_body": "May be we should avoid any recommendation in terms of sizing, just put a note that for a large synonyms sets put extra demand on memory. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1542709397",
    "pr_number": 106861,
    "pr_file": "docs/reference/search/field-caps.asciidoc",
    "created_at": "2024-03-28T10:58:21+00:00",
    "commented_code": "Defaults to `false`.\n\n`include_empty_fields`::\n  (Optional, Boolean) If `false`, fields that never had a value in any shards are not included in the response. Fields that are not empty are always included. This flag does not consider deletions and updates.  If a field was non-empty and all the documents containing that field were deleted or the field was removed by updates,  it will still be returned even if the flag is `false`.\n  (Optional, Boolean) If `false`, fields that never had a value in any shards are not included in the response. Fields that are not empty are always included. This flag does not consider deletions and updates.  If a field was non-empty and all the documents containing that field were deleted or the field was removed by updates,  it will still be returned even if the flag is `false`. To be used with caution, if set to `false` it gives accurate results at the cost of longer response times compared to the default behavior.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1542709397",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 106861,
        "pr_file": "docs/reference/search/field-caps.asciidoc",
        "discussion_id": "1542709397",
        "commented_code": "@@ -78,7 +78,7 @@ include::{es-repo-dir}/rest-api/common-parms.asciidoc[tag=index-ignore-unavailab\n   Defaults to `false`.\n \n `include_empty_fields`::\n-  (Optional, Boolean) If `false`, fields that never had a value in any shards are not included in the response. Fields that are not empty are always included. This flag does not consider deletions and updates.  If a field was non-empty and all the documents containing that field were deleted or the field was removed by updates,  it will still be returned even if the flag is `false`.\n+  (Optional, Boolean) If `false`, fields that never had a value in any shards are not included in the response. Fields that are not empty are always included. This flag does not consider deletions and updates.  If a field was non-empty and all the documents containing that field were deleted or the field was removed by updates,  it will still be returned even if the flag is `false`. To be used with caution, if set to `false` it gives accurate results at the cost of longer response times compared to the default behavior.",
        "comment_created_at": "2024-03-28T10:58:21+00:00",
        "comment_author": "javanna",
        "comment_body": "Could you expand on what the factor is that causes longer response times, so users have the knowledge to decide and adequately test?\r\n\r\nI wonder if we should have a warning flag like we do in other cases, that makes it more evident compared to a note in the text.",
        "pr_file_module": null
      }
    ]
  }
]
