---
title: Document security requirements explicitly
description: 'Always document security-related configurations, permissions, and behaviors
  explicitly and comprehensively. When documenting security features:


  1. Clearly specify required permissions and roles'
repository: elastic/elasticsearch
label: Security
language: Other
comments_count: 2
repository_stars: 73104
---

Always document security-related configurations, permissions, and behaviors explicitly and comprehensively. When documenting security features:

1. Clearly specify required permissions and roles
2. Note version-specific security behavior changes 
3. Explicitly state configuration inheritance rules and exceptions
4. Highlight security-critical settings with warnings or notes

For example, when documenting an API that interacts with protected resources:

```
IMPORTANT: This action requires specific permissions. In {es} 8.1 and later, the superuser 
role doesn't have write access to system indices. If you execute this request as a 
user with the superuser role, you must have an additional role with the 
`allow_restricted_indices` privilege set to `true` to delete system indices.
```

For configuration documentation:

```
NOTE: Transport profiles do not inherit TLS/SSL settings from the default transport.
The `xpack.security.transport.ssl.enabled` setting is an exception that controls
SSL for both default transport and any transport profiles.
```

Clear and complete security documentation prevents misconfigurations that could lead to vulnerabilities or access issues.


[
  {
    "discussion_id": "920428509",
    "pr_number": 88438,
    "pr_file": "docs/reference/features/apis/reset-features-api.asciidoc",
    "created_at": "2022-07-13T19:26:57+00:00",
    "commented_code": "Return a cluster to the same state as a new installation by resetting the feature state for all {es} features. This deletes all state information stored in system indices.\n\nIMPORTANT: This action deletes system indices and [starting from 8.1](https://github.com/elastic/elasticsearch/pull/81400) system index write-access has been removed from the superuser role. So, if you are performing this action from a user with the superuser role, you need to ensure that the user has another role with the `allow_restricted_indices` set to `true` to be able to delete all system indices.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "920428509",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 88438,
        "pr_file": "docs/reference/features/apis/reset-features-api.asciidoc",
        "discussion_id": "920428509",
        "commented_code": "@@ -26,6 +26,8 @@ POST /_features/_reset\n \n Return a cluster to the same state as a new installation by resetting the feature state for all {es} features. This deletes all state information stored in system indices.\n \n+IMPORTANT: This action deletes system indices and [starting from 8.1](https://github.com/elastic/elasticsearch/pull/81400) system index write-access has been removed from the superuser role. So, if you are performing this action from a user with the superuser role, you need to ensure that the user has another role with the `allow_restricted_indices` set to `true` to be able to delete all system indices.\n+",
        "comment_created_at": "2022-07-13T19:26:57+00:00",
        "comment_author": "lockewritesdocs",
        "comment_body": "```suggestion\r\nIMPORTANT: This action deletes system indices. In {es} 8.1 and later, the superuser\r\nrole doesn't have write access to system indices. If you execute this request as a\r\nuser with the superuser role, you must have an additional role with the\r\n`allow_restricted_indices` privilege set to `true` to delete all system indices.\r\n\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "920431057",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 88438,
        "pr_file": "docs/reference/features/apis/reset-features-api.asciidoc",
        "discussion_id": "920428509",
        "commented_code": "@@ -26,6 +26,8 @@ POST /_features/_reset\n \n Return a cluster to the same state as a new installation by resetting the feature state for all {es} features. This deletes all state information stored in system indices.\n \n+IMPORTANT: This action deletes system indices and [starting from 8.1](https://github.com/elastic/elasticsearch/pull/81400) system index write-access has been removed from the superuser role. So, if you are performing this action from a user with the superuser role, you need to ensure that the user has another role with the `allow_restricted_indices` set to `true` to be able to delete all system indices.\n+",
        "comment_created_at": "2022-07-13T19:30:32+00:00",
        "comment_author": "lockewritesdocs",
        "comment_body": "Here's a suggested rewording of your original text. Let me know if this change makes sense \ud83d\udca1 ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1183541072",
    "pr_number": 86048,
    "pr_file": "docs/reference/settings/security-settings.asciidoc",
    "created_at": "2023-05-03T11:02:43+00:00",
    "commented_code": "[[ssl-tls-profile-settings]]\n[discrete]\n===== Transport profile TLS/SSL settings\nNOTE: Transport profiles do not inherit TLS/SSL settings\nfrom the default transport. \n\nThe same settings that are available for the <<transport-tls-ssl-settings, default transport>>\nare also available for each transport profile. By default, the settings for a\ntransport profile will be the same as the default transport unless they\nare specified.\nare also available for each transport profile.",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1183541072",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 86048,
        "pr_file": "docs/reference/settings/security-settings.asciidoc",
        "discussion_id": "1183541072",
        "commented_code": "@@ -2345,10 +2345,11 @@ include::ssl-settings.asciidoc[]\n [[ssl-tls-profile-settings]]\n [discrete]\n ===== Transport profile TLS/SSL settings\n+NOTE: Transport profiles do not inherit TLS/SSL settings\n+from the default transport. \n+\n The same settings that are available for the <<transport-tls-ssl-settings, default transport>>\n-are also available for each transport profile. By default, the settings for a\n-transport profile will be the same as the default transport unless they\n-are specified.\n+are also available for each transport profile. ",
        "comment_created_at": "2023-05-03T11:02:43+00:00",
        "comment_author": "ywangd",
        "comment_body": "The `xpack.security.transport.ssl.enabled` setting is an exception:\r\n1. It controls whether SSL is enabled for both the default transport and any transport profiles.\r\n2. Transport profiles do not have a corresponding setting for it. ",
        "pr_file_module": null
      }
    ]
  }
]
