---
title: Precise testing dependency versioning
description: When specifying testing library dependencies, always use explicit minimum
  patch versions rather than development branches or broad version constraints. This
  practice ensures consistent and reproducible test environments across development,
  CI systems, and production builds.
repository: laravel/framework
label: Testing
language: Json
comments_count: 2
repository_stars: 33763
---

When specifying testing library dependencies, always use explicit minimum patch versions rather than development branches or broad version constraints. This practice ensures consistent and reproducible test environments across development, CI systems, and production builds.

Example of good practice:
```json
"dependencies": {
  "phpunit/phpunit": "^10.5.35|^11.3.6|^12.0.1",
  "orchestra/testbench-core": "^9.9.3"
}
```

Example of practices to avoid:
```json
"dependencies": {
  "phpunit/phpunit": "^10.5|^11.0", // Too broad, may include versions with issues
  "orchestra/testbench-core": "9.x-dev" // Development branch, not stable
}
```

This standard helps prevent subtle test failures due to dependency changes and makes test behavior more predictable across all environments. Using precise version constraints is particularly important for testing frameworks as unexpected behavior in these dependencies can lead to false positives or negatives in your test results.


[
  {
    "discussion_id": "1938439791",
    "pr_number": 54316,
    "pr_file": "composer.json",
    "created_at": "2025-02-02T09:02:38+00:00",
    "commented_code": "\"league/flysystem-read-only\": \"^3.25.1\",\n        \"league/flysystem-sftp-v3\": \"^3.25.1\",\n        \"mockery/mockery\": \"^1.6.10\",\n        \"orchestra/testbench-core\": \"^9.6\",\n        \"orchestra/testbench-core\": \"9.x-dev\",",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1938439791",
        "repo_full_name": "laravel/framework",
        "pr_number": 54316,
        "pr_file": "composer.json",
        "discussion_id": "1938439791",
        "commented_code": "@@ -111,11 +111,11 @@\n         \"league/flysystem-read-only\": \"^3.25.1\",\n         \"league/flysystem-sftp-v3\": \"^3.25.1\",\n         \"mockery/mockery\": \"^1.6.10\",\n-        \"orchestra/testbench-core\": \"^9.6\",\n+        \"orchestra/testbench-core\": \"9.x-dev\",",
        "comment_created_at": "2025-02-02T09:02:38+00:00",
        "comment_author": "crynobone",
        "comment_body": "```suggestion\r\n        \"orchestra/testbench-core\": \"^9.9.3\",\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1946329442",
    "pr_number": 54316,
    "pr_file": "src/Illuminate/Testing/composer.json",
    "created_at": "2025-02-07T10:41:38+00:00",
    "commented_code": "\"illuminate/database\": \"Required to assert databases (^11.0).\",\n        \"illuminate/http\": \"Required to assert responses (^11.0).\",\n        \"mockery/mockery\": \"Required to use mocking (^1.6).\",\n        \"phpunit/phpunit\": \"Required to use assertions and run tests (^10.5|^11.0).\"\n        \"phpunit/phpunit\": \"Required to use assertions and run tests (^10.5.35|^11.3.6|^12.0).\"",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1946329442",
        "repo_full_name": "laravel/framework",
        "pr_number": 54316,
        "pr_file": "src/Illuminate/Testing/composer.json",
        "discussion_id": "1946329442",
        "commented_code": "@@ -37,7 +37,7 @@\n         \"illuminate/database\": \"Required to assert databases (^11.0).\",\n         \"illuminate/http\": \"Required to assert responses (^11.0).\",\n         \"mockery/mockery\": \"Required to use mocking (^1.6).\",\n-        \"phpunit/phpunit\": \"Required to use assertions and run tests (^10.5|^11.0).\"\n+        \"phpunit/phpunit\": \"Required to use assertions and run tests (^10.5.35|^11.3.6|^12.0).\"",
        "comment_created_at": "2025-02-07T10:41:38+00:00",
        "comment_author": "crynobone",
        "comment_body": "```suggestion\r\n        \"phpunit/phpunit\": \"Required to use assertions and run tests (^10.5.35|^11.3.6|^12.0.1).\"\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
