---
title: Enforce least privilege
description: Always assign the minimum permissions necessary for functionality when
  implementing role-based access controls. This fundamental security principle reduces
  the potential attack surface and minimizes the impact of compromised accounts.
repository: elastic/elasticsearch
label: Security
language: Java
comments_count: 1
repository_stars: 73104
---

Always assign the minimum permissions necessary for functionality when implementing role-based access controls. This fundamental security principle reduces the potential attack surface and minimizes the impact of compromised accounts.

Key practices:
1. Start with read-only permissions by default and add specific write permissions only where justified
2. Question and verify any broad write access permissions during code reviews
3. Separate read and write privileges in role definitions to make access patterns explicit
4. Regularly audit existing role permissions against actual usage needs

Example:
```java
// Good: Explicit, minimal permissions
RoleDescriptor.IndicesPrivileges.builder()
    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)
    .privileges("read", "view_index_metadata")
    .build()

// Avoid: Unnecessarily broad permissions
RoleDescriptor.IndicesPrivileges.builder()
    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)
    .privileges("read", "view_index_metadata", "write", "maintenance")
    .build()
```

When in doubt, start with more restrictive permissions and expand only when necessary based on functional requirements. Challenge assumptions about permission needs during code reviews, as shown in the discussion where write access was initially questioned and determined to be unnecessary.


[
  {
    "discussion_id": "2163585024",
    "pr_number": 129662,
    "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/security/authz/store/ReservedRolesStore.java",
    "created_at": "2025-06-24T10:36:11+00:00",
    "commented_code": "ReservedRolesStore.LISTS_ITEMS_INDEX,\n                        ReservedRolesStore.ALERTS_LEGACY_INDEX_REINDEXED_V8,\n                        ReservedRolesStore.LISTS_INDEX_REINDEXED_V8,\n                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8\n                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8,\n                        ReservedRolesStore.ASSET_CRITICALITY_INDEX\n                    )\n                    .privileges(\"read\", \"view_index_metadata\", \"write\", \"maintenance\")\n                    .build(),\n                // Security - Entity Store is view only\n                RoleDescriptor.IndicesPrivileges.builder()\n                    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)\n                    .privileges(\"read\", \"view_index_metadata\")",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2163585024",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129662,
        "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/security/authz/store/ReservedRolesStore.java",
        "discussion_id": "2163585024",
        "commented_code": "@@ -842,10 +848,16 @@ private static RoleDescriptor buildEditorRoleDescriptor() {\n                         ReservedRolesStore.LISTS_ITEMS_INDEX,\n                         ReservedRolesStore.ALERTS_LEGACY_INDEX_REINDEXED_V8,\n                         ReservedRolesStore.LISTS_INDEX_REINDEXED_V8,\n-                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8\n+                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8,\n+                        ReservedRolesStore.ASSET_CRITICALITY_INDEX\n                     )\n                     .privileges(\"read\", \"view_index_metadata\", \"write\", \"maintenance\")\n                     .build(),\n+                // Security - Entity Store is view only\n+                RoleDescriptor.IndicesPrivileges.builder()\n+                    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)\n+                    .privileges(\"read\", \"view_index_metadata\")",
        "comment_created_at": "2025-06-24T10:36:11+00:00",
        "comment_author": "richard-dennehy",
        "comment_body": "Just to double check - Serverless Editor appears to have write access to these indices - is this difference intentional?",
        "pr_file_module": null
      },
      {
        "comment_id": "2164316642",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129662,
        "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/security/authz/store/ReservedRolesStore.java",
        "discussion_id": "2163585024",
        "commented_code": "@@ -842,10 +848,16 @@ private static RoleDescriptor buildEditorRoleDescriptor() {\n                         ReservedRolesStore.LISTS_ITEMS_INDEX,\n                         ReservedRolesStore.ALERTS_LEGACY_INDEX_REINDEXED_V8,\n                         ReservedRolesStore.LISTS_INDEX_REINDEXED_V8,\n-                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8\n+                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8,\n+                        ReservedRolesStore.ASSET_CRITICALITY_INDEX\n                     )\n                     .privileges(\"read\", \"view_index_metadata\", \"write\", \"maintenance\")\n                     .build(),\n+                // Security - Entity Store is view only\n+                RoleDescriptor.IndicesPrivileges.builder()\n+                    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)\n+                    .privileges(\"read\", \"view_index_metadata\")",
        "comment_created_at": "2025-06-24T15:23:47+00:00",
        "comment_author": "opauloh",
        "comment_body": "Thanks for bringing it to my attention! \r\n\r\nI will tag @hop-dev and @jaredburgettelastic to help on that. Mark / Jared, from what I could see, users don't really need to write directly into the Entity Store index, but do you happen to know a use case where they would need? Like running the API to clean the Entity Store or something else?",
        "pr_file_module": null
      },
      {
        "comment_id": "2174986836",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129662,
        "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/security/authz/store/ReservedRolesStore.java",
        "discussion_id": "2163585024",
        "commented_code": "@@ -842,10 +848,16 @@ private static RoleDescriptor buildEditorRoleDescriptor() {\n                         ReservedRolesStore.LISTS_ITEMS_INDEX,\n                         ReservedRolesStore.ALERTS_LEGACY_INDEX_REINDEXED_V8,\n                         ReservedRolesStore.LISTS_INDEX_REINDEXED_V8,\n-                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8\n+                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8,\n+                        ReservedRolesStore.ASSET_CRITICALITY_INDEX\n                     )\n                     .privileges(\"read\", \"view_index_metadata\", \"write\", \"maintenance\")\n                     .build(),\n+                // Security - Entity Store is view only\n+                RoleDescriptor.IndicesPrivileges.builder()\n+                    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)\n+                    .privileges(\"read\", \"view_index_metadata\")",
        "comment_created_at": "2025-06-30T12:43:58+00:00",
        "comment_author": "hop-dev",
        "comment_body": "No I think this was a mistake in the original PR apologies!",
        "pr_file_module": null
      },
      {
        "comment_id": "2175678919",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129662,
        "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/security/authz/store/ReservedRolesStore.java",
        "discussion_id": "2163585024",
        "commented_code": "@@ -842,10 +848,16 @@ private static RoleDescriptor buildEditorRoleDescriptor() {\n                         ReservedRolesStore.LISTS_ITEMS_INDEX,\n                         ReservedRolesStore.ALERTS_LEGACY_INDEX_REINDEXED_V8,\n                         ReservedRolesStore.LISTS_INDEX_REINDEXED_V8,\n-                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8\n+                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8,\n+                        ReservedRolesStore.ASSET_CRITICALITY_INDEX\n                     )\n                     .privileges(\"read\", \"view_index_metadata\", \"write\", \"maintenance\")\n                     .build(),\n+                // Security - Entity Store is view only\n+                RoleDescriptor.IndicesPrivileges.builder()\n+                    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)\n+                    .privileges(\"read\", \"view_index_metadata\")",
        "comment_created_at": "2025-06-30T18:44:09+00:00",
        "comment_author": "opauloh",
        "comment_body": "Thanks for confirming @hop-dev, so @richard-dennehy, the changes on this PR are correct, we will follow up on reducing the extra permissions on Serverless editor role to keep it consistent!",
        "pr_file_module": null
      },
      {
        "comment_id": "2176832830",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129662,
        "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/security/authz/store/ReservedRolesStore.java",
        "discussion_id": "2163585024",
        "commented_code": "@@ -842,10 +848,16 @@ private static RoleDescriptor buildEditorRoleDescriptor() {\n                         ReservedRolesStore.LISTS_ITEMS_INDEX,\n                         ReservedRolesStore.ALERTS_LEGACY_INDEX_REINDEXED_V8,\n                         ReservedRolesStore.LISTS_INDEX_REINDEXED_V8,\n-                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8\n+                        ReservedRolesStore.LISTS_ITEMS_INDEX_REINDEXED_V8,\n+                        ReservedRolesStore.ASSET_CRITICALITY_INDEX\n                     )\n                     .privileges(\"read\", \"view_index_metadata\", \"write\", \"maintenance\")\n                     .build(),\n+                // Security - Entity Store is view only\n+                RoleDescriptor.IndicesPrivileges.builder()\n+                    .indices(ReservedRolesStore.ENTITY_STORE_V1_LATEST_INDEX)\n+                    .privileges(\"read\", \"view_index_metadata\")",
        "comment_created_at": "2025-07-01T08:33:31+00:00",
        "comment_author": "hop-dev",
        "comment_body": "@opauloh sorry I have just thought, because the transform runs as the user who enabled the entity store, I believe we do need write permissions? Have I got that wrong? ",
        "pr_file_module": null
      }
    ]
  }
]
