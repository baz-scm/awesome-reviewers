---
title: Log message quality
description: Ensure all log messages are consistent in formatting and clear in purpose.
  Complete sentences in logs should end with proper punctuation (especially periods),
  and messages should precisely describe what is happening in the system. When logging
  phase transitions or significant events, explicitly state where one phase ends and
  another begins rather than using...
repository: chef/chef
label: Logging
language: Markdown
comments_count: 2
repository_stars: 7860
---

Ensure all log messages are consistent in formatting and clear in purpose. Complete sentences in logs should end with proper punctuation (especially periods), and messages should precisely describe what is happening in the system. When logging phase transitions or significant events, explicitly state where one phase ends and another begins rather than using vague descriptions.

Example:
```ruby
# Poor logging
logger.info("Processing data")
logger.info("Infra Phase and Compliance Phase improved")

# Better logging
logger.info("Processing data.")
logger.info("Transitioning from Infra Phase to Compliance Phase.")
```

This standard improves log readability during troubleshooting and ensures documentation accurately reflects system behavior.


[
  {
    "discussion_id": "697656336",
    "pr_number": 11976,
    "pr_file": "RELEASE_NOTES.md",
    "created_at": "2021-08-27T18:56:24+00:00",
    "commented_code": "This file holds \"in progress\" release notes for the current release under development and is intended for consumption by the Chef Documentation team. Please see <https://docs.chef.io/release_notes/> for the official Chef release notes.\n\n## What's New in 17.4\n## What's New in 17.4.38\n\n### Bug fixes\n\n- Resolved a regression introduced in Chef Infra Client 17.4 that would cause HWRP-style resources inheriting from LWRPBase to fail.\n\n### Enhancements\n\n- Log output has been improved to better deliniate when the Infra Phase and Compliance Phase start and end.\n- Ohai data collection of Amazon EC2 metadata has been improved to collect additional data for some configurations.\n- Removed ERROR logs when retrying failed communication with the Chef Infra Server",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "697656336",
        "repo_full_name": "chef/chef",
        "pr_number": 11976,
        "pr_file": "RELEASE_NOTES.md",
        "discussion_id": "697656336",
        "commented_code": "@@ -1,6 +1,35 @@\n This file holds \"in progress\" release notes for the current release under development and is intended for consumption by the Chef Documentation team. Please see <https://docs.chef.io/release_notes/> for the official Chef release notes.\n \n-## What's New in 17.4\n+## What's New in 17.4.38\n+\n+### Bug fixes\n+\n+- Resolved a regression introduced in Chef Infra Client 17.4 that would cause HWRP-style resources inheriting from LWRPBase to fail.\n+\n+### Enhancements\n+\n+- Log output has been improved to better deliniate when the Infra Phase and Compliance Phase start and end.\n+- Ohai data collection of Amazon EC2 metadata has been improved to collect additional data for some configurations.\n+- Removed ERROR logs when retrying failed communication with the Chef Infra Server",
        "comment_created_at": "2021-08-27T18:56:24+00:00",
        "comment_author": "IanMadd",
        "comment_body": "```suggestion\r\n- Removed ERROR logs when retrying failed communication with the Chef Infra Server.\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "697659082",
    "pr_number": 11976,
    "pr_file": "RELEASE_NOTES.md",
    "created_at": "2021-08-27T19:01:11+00:00",
    "commented_code": "This file holds \"in progress\" release notes for the current release under development and is intended for consumption by the Chef Documentation team. Please see <https://docs.chef.io/release_notes/> for the official Chef release notes.\n\n## What's New in 17.4\n## What's New in 17.4.38\n\n### Bug fixes\n\n- Resolved a regression introduced in Chef Infra Client 17.4 that would cause HWRP-style resources inheriting from LWRPBase to fail.\n\n### Enhancements\n\n- Log output has been improved to better deliniate when the Infra Phase and Compliance Phase start and end.",
    "repo_full_name": "chef/chef",
    "discussion_comments": [
      {
        "comment_id": "697659082",
        "repo_full_name": "chef/chef",
        "pr_number": 11976,
        "pr_file": "RELEASE_NOTES.md",
        "discussion_id": "697659082",
        "commented_code": "@@ -1,6 +1,35 @@\n This file holds \"in progress\" release notes for the current release under development and is intended for consumption by the Chef Documentation team. Please see <https://docs.chef.io/release_notes/> for the official Chef release notes.\n \n-## What's New in 17.4\n+## What's New in 17.4.38\n+\n+### Bug fixes\n+\n+- Resolved a regression introduced in Chef Infra Client 17.4 that would cause HWRP-style resources inheriting from LWRPBase to fail.\n+\n+### Enhancements\n+\n+- Log output has been improved to better deliniate when the Infra Phase and Compliance Phase start and end.",
        "comment_created_at": "2021-08-27T19:01:11+00:00",
        "comment_author": "kagarmoe",
        "comment_body": "```suggestion\r\n- Improved log output to clearly define where the Infra Phase ends and the Compliance Phase begins.\r\n```",
        "pr_file_module": null
      }
    ]
  }
]
