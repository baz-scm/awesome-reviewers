---
title: Disable coverage in workflows
description: Keep code coverage tools disabled in CI/CD workflows unless they're specifically
  needed for generating coverage reports. Enabling coverage tools like xdebug in GitHub
  Actions can significantly slow down pipeline execution without providing value when
  reports aren't being collected or analyzed.
repository: laravel/framework
label: Testing
language: Yaml
comments_count: 4
repository_stars: 33763
---

Keep code coverage tools disabled in CI/CD workflows unless they're specifically needed for generating coverage reports. Enabling coverage tools like xdebug in GitHub Actions can significantly slow down pipeline execution without providing value when reports aren't being collected or analyzed.

When configuring PHP environments in workflows, explicitly set `coverage: none` and avoid including coverage extensions like xdebug unless they serve a specific purpose:

```yaml
uses: shivammathur/setup-php@v2
with:
  php-version: 8.2
  extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr
  tools: composer:v2
  coverage: none  # Keep coverage disabled for better performance
```

Reserve coverage tools for dedicated testing jobs that specifically generate and process coverage reports. This helps maintain faster CI pipelines while still allowing coverage analysis when needed.


[
  {
    "discussion_id": "1856408580",
    "pr_number": 53648,
    "pr_file": ".github/workflows/queues.yml",
    "created_at": "2024-11-25T11:05:37+00:00",
    "commented_code": "uses: shivammathur/setup-php@v2\n        with:\n          php-version: 8.2\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n          tools: composer:v2\n          coverage: none\n          coverage: xdebug",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1856408580",
        "repo_full_name": "laravel/framework",
        "pr_number": 53648,
        "pr_file": ".github/workflows/queues.yml",
        "discussion_id": "1856408580",
        "commented_code": "@@ -147,9 +147,9 @@ jobs:\n         uses: shivammathur/setup-php@v2\n         with:\n           php-version: 8.2\n-          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n+          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n           tools: composer:v2\n-          coverage: none\n+          coverage: xdebug",
        "comment_created_at": "2024-11-25T11:05:37+00:00",
        "comment_author": "crynobone",
        "comment_body": "```suggestion\r\n          coverage: none\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1856409108",
    "pr_number": 53648,
    "pr_file": ".github/workflows/queues.yml",
    "created_at": "2024-11-25T11:06:02+00:00",
    "commented_code": "uses: shivammathur/setup-php@v2\n        with:\n          php-version: 8.2\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n          tools: composer:v2\n          coverage: none\n          coverage: xdebug",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1856409108",
        "repo_full_name": "laravel/framework",
        "pr_number": 53648,
        "pr_file": ".github/workflows/queues.yml",
        "discussion_id": "1856409108",
        "commented_code": "@@ -107,9 +107,9 @@ jobs:\n         uses: shivammathur/setup-php@v2\n         with:\n           php-version: 8.2\n-          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n+          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n           tools: composer:v2\n-          coverage: none\n+          coverage: xdebug",
        "comment_created_at": "2024-11-25T11:06:02+00:00",
        "comment_author": "crynobone",
        "comment_body": "```suggestion\r\n          coverage: none\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1856409578",
    "pr_number": 53648,
    "pr_file": ".github/workflows/queues.yml",
    "created_at": "2024-11-25T11:06:21+00:00",
    "commented_code": "uses: shivammathur/setup-php@v2\n        with:\n          php-version: 8.2\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n          tools: composer:v2\n          coverage: none\n          coverage: xdebug",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1856409578",
        "repo_full_name": "laravel/framework",
        "pr_number": 53648,
        "pr_file": ".github/workflows/queues.yml",
        "discussion_id": "1856409578",
        "commented_code": "@@ -59,9 +59,9 @@ jobs:\n         uses: shivammathur/setup-php@v2\n         with:\n           php-version: 8.2\n-          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n+          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n           tools: composer:v2\n-          coverage: none\n+          coverage: xdebug",
        "comment_created_at": "2024-11-25T11:06:21+00:00",
        "comment_author": "crynobone",
        "comment_body": "```suggestion\r\n          coverage: none\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1856413883",
    "pr_number": 53648,
    "pr_file": ".github/workflows/databases.yml",
    "created_at": "2024-11-25T11:09:22+00:00",
    "commented_code": "uses: shivammathur/setup-php@v2\n        with:\n          php-version: 8.3\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n          tools: composer:v2\n          coverage: none\n          coverage: xdebug",
    "repo_full_name": "laravel/framework",
    "discussion_comments": [
      {
        "comment_id": "1856413883",
        "repo_full_name": "laravel/framework",
        "pr_number": 53648,
        "pr_file": ".github/workflows/databases.yml",
        "discussion_id": "1856413883",
        "commented_code": "@@ -35,9 +35,9 @@ jobs:\n         uses: shivammathur/setup-php@v2\n         with:\n           php-version: 8.3\n-          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, :php-psr\n+          extensions: dom, curl, libxml, mbstring, zip, pcntl, pdo, pdo_mysql, xml, xdebug, :php-psr\n           tools: composer:v2\n-          coverage: none\n+          coverage: xdebug",
        "comment_created_at": "2024-11-25T11:09:22+00:00",
        "comment_author": "crynobone",
        "comment_body": "```suggestion\r\n          coverage: none\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
