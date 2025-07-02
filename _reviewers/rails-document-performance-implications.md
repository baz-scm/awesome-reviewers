---
title: Document performance implications
description: Clearly document the performance implications of features and configurations
  to help users make informed decisions. Avoid overstating or understating performance
  impacts. Instead, provide specific context about when certain features might impact
  performance and in what environments they are appropriate.
repository: rails/rails
label: Performance Optimization
language: Markdown
comments_count: 3
repository_stars: 57027
---

Clearly document the performance implications of features and configurations to help users make informed decisions. Avoid overstating or understating performance impacts. Instead, provide specific context about when certain features might impact performance and in what environments they are appropriate.

For example, when adding a feature with potential performance impact:

```ruby
# GOOD
# In documentation:
# The :source_location option can slow down query execution, so consider its impact
# if using in production environments where query volume is high.

# BAD
# WARNING: Never use :source_location in production! It will destroy performance!

# BETTER
# When implementing configurable features:
config.feature.enabled = true # in development.rb
config.feature.enabled = false # in production.rb (default)
```

Consider providing environment-specific defaults for performance-impacting features, making them opt-in for production rather than requiring users to opt-out. When performance tradeoffs exist (like between different checksum algorithms or between observability and optimization), document these tradeoffs to help users select the most appropriate option for their specific use case.


[
  {
    "discussion_id": "1950324846",
    "pr_number": 54468,
    "pr_file": "activestorage/CHANGELOG.md",
    "created_at": "2025-02-11T06:55:40+00:00",
    "commented_code": "*   Support additional file checksum algorithms in S3 Adapter\n\n    Add support for CRC32, CRC32c, SHA1, SHA256, and CRC64NVMe to S3 service for",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1950324846",
        "repo_full_name": "rails/rails",
        "pr_number": 54468,
        "pr_file": "activestorage/CHANGELOG.md",
        "discussion_id": "1950324846",
        "commented_code": "@@ -1,3 +1,12 @@\n+*   Support additional file checksum algorithms in S3 Adapter\n+\n+    Add support for CRC32, CRC32c, SHA1, SHA256, and CRC64NVMe to S3 service for",
        "comment_created_at": "2025-02-11T06:55:40+00:00",
        "comment_author": "byroot",
        "comment_body": "I think that's where we might as misunderstood each others.\r\n\r\nI don't think there is any value in supporting 6 different checksum algorithms for S3, the goal is just to change the current MD5 for something else (and to support both concurrently to allow smooth migration).\r\n\r\nSo we shouldn't add these 5, just one of these.",
        "pr_file_module": null
      },
      {
        "comment_id": "1951047014",
        "repo_full_name": "rails/rails",
        "pr_number": 54468,
        "pr_file": "activestorage/CHANGELOG.md",
        "discussion_id": "1950324846",
        "commented_code": "@@ -1,3 +1,12 @@\n+*   Support additional file checksum algorithms in S3 Adapter\n+\n+    Add support for CRC32, CRC32c, SHA1, SHA256, and CRC64NVMe to S3 service for",
        "comment_created_at": "2025-02-11T15:17:17+00:00",
        "comment_author": "mrpasquini",
        "comment_body": "I would choose SHA256 for my original intention of making things easier for FIPS compliance. This is a different choice than raw throughput/performance, so it seemed to make sense to support multiple for the different use cases. There is not much different in the adapter itself beyond MD5 vs non-MD5.\r\n\r\nThe other thing to perhaps take into account is that multipart uploads do not currently support checksums in the s3 adapter. If this was to be added, there are some differences based on the checksum algorithm (full file vs composite checksum) as noted under \"Multipart uploads\" section [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/checking-object-integrity.html)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2133082129",
    "pr_number": 55167,
    "pr_file": "guides/source/configuring.md",
    "created_at": "2025-06-06T23:51:23+00:00",
    "commented_code": "`[ :application, :controller, :action, :job ]`. The available tags are: `:application`, `:controller`,\n`:namespaced_controller`, `:action`, `:job`, and `:source_location`.\n\nWARNING: Calculating the caller location via `:source_location` is a costly operation and should be used primarily in development (note, there is also a `config.active_record.verbose_query_logs` that serves the same purpose) or occasionally on production for debugging purposes.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "2133082129",
        "repo_full_name": "rails/rails",
        "pr_number": 55167,
        "pr_file": "guides/source/configuring.md",
        "discussion_id": "2133082129",
        "commented_code": "@@ -1488,6 +1488,8 @@ Define an `Array` specifying the key/value tags to be inserted in an SQL comment\n `[ :application, :controller, :action, :job ]`. The available tags are: `:application`, `:controller`,\n `:namespaced_controller`, `:action`, `:job`, and `:source_location`.\n \n+WARNING: Calculating the caller location via `:source_location` is a costly operation and should be used primarily in development (note, there is also a `config.active_record.verbose_query_logs` that serves the same purpose) or occasionally on production for debugging purposes.",
        "comment_created_at": "2025-06-06T23:51:23+00:00",
        "comment_author": "skipkayhil",
        "comment_body": "```suggestion\r\nWARNING: Calculating the `:source_location` of a query can be slow, so you should consider its impact if using it in a production environment.\r\n```\r\n\r\nThis is super subjective, but I think we can be more concise (more descriptive and less prescriptive). What do you think about this?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1950500813",
    "pr_number": 54492,
    "pr_file": "guides/source/debugging_rails_applications.md",
    "created_at": "2025-02-11T09:27:57+00:00",
    "commented_code": "config.active_record.query_log_tags_enabled = true\n```\n\nWARNING: Enabled query log tags (query_log_tags_enabled = true) automatically disables prepared statements.\nThis configuration is not recommended for production environments.\nPerformance degradation occurs due to both disabled prepared statement optimization and significantly increased log volume.",
    "repo_full_name": "rails/rails",
    "discussion_comments": [
      {
        "comment_id": "1950500813",
        "repo_full_name": "rails/rails",
        "pr_number": 54492,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1950500813",
        "commented_code": "@@ -264,6 +264,10 @@ To enable, add in `application.rb` or any environment initializer:\n config.active_record.query_log_tags_enabled = true\n ```\n \n+WARNING: Enabled query log tags (query_log_tags_enabled = true) automatically disables prepared statements.\n+This configuration is not recommended for production environments.\n+Performance degradation occurs due to both disabled prepared statement optimization and significantly increased log volume.",
        "comment_created_at": "2025-02-11T09:27:57+00:00",
        "comment_author": "byroot",
        "comment_body": "The performance impact really isn't that bad, and if anything, production is really where query logs are important.\r\n\r\nI think a simple note saying that prepared statements will be disabled is enough.",
        "pr_file_module": null
      },
      {
        "comment_id": "1950842261",
        "repo_full_name": "rails/rails",
        "pr_number": 54492,
        "pr_file": "guides/source/debugging_rails_applications.md",
        "discussion_id": "1950500813",
        "commented_code": "@@ -264,6 +264,10 @@ To enable, add in `application.rb` or any environment initializer:\n config.active_record.query_log_tags_enabled = true\n ```\n \n+WARNING: Enabled query log tags (query_log_tags_enabled = true) automatically disables prepared statements.\n+This configuration is not recommended for production environments.\n+Performance degradation occurs due to both disabled prepared statement optimization and significantly increased log volume.",
        "comment_created_at": "2025-02-11T13:19:23+00:00",
        "comment_author": "ChibaDaigo",
        "comment_body": "Thanks for review. I overestimated the impact of log outputs.\r\nI have made the changes. Please review again.\r\n[add note of query_log_tags_enabled](https://github.com/rails/rails/pull/54492/commits/2f6a3e5edaa713eb520b52ffc6ae8ccbc8a285fd)",
        "pr_file_module": null
      }
    ]
  }
]
