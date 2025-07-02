---
title: Prevent redundant operations
description: 'In distributed database systems, prevent redundant operations that can
  overload cluster resources. When implementing update operations that might be triggered
  simultaneously from multiple nodes:'
repository: elastic/elasticsearch
label: Database
language: Java
comments_count: 5
repository_stars: 73104
---

In distributed database systems, prevent redundant operations that can overload cluster resources. When implementing update operations that might be triggered simultaneously from multiple nodes:

1. Add conditional checks to avoid redundant processing when the state hasn't changed:

```java
// Before applying mapping updates, check if they're identical to existing mappings
if (existingMapper != null && sourceToMerge.equals(existingMapper.mappingSource())) {
    context.resetForNoopMappingUpdateRetry(initialMappingVersion);
    return true;
}
```

2. Consider sequencing operations when high concurrency is expected, especially for resource-intensive updates:
   - Execute updates sequentially rather than allowing parallel execution
   - For critical operations, consider coordinating through a single node (like the master node)
   - Use appropriate locking or versioning mechanisms to prevent conflicting updates

3. Use direct access methods to avoid constructing unnecessary intermediate objects:
   - Access metadata directly with methods like `getProjectMetadata()` instead of constructing full state objects
   - Preserve important properties like query boost and name parameters when transforming queries

These optimizations are particularly important when multiple data nodes might be issuing similar updates (like dynamic mappings) or when working near capacity limits of the system.


[
  {
    "discussion_id": "1651609389",
    "pr_number": 109949,
    "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
    "created_at": "2024-06-24T21:05:28+00:00",
    "commented_code": "long version,\n        UpdateHelper.Result updateResult\n    ) {\n        final var mapperService = primary.mapperService();\n        try {\n            final var sourceToMerge = new CompressedXContent(result.getRequiredMappingUpdate());\n            final var mapperService = primary.mapperService();\n            final long initialMappingVersion = mapperService.mappingVersion();\n            final var existingMapper = mapperService.documentMapper();\n            if (existingMapper != null && sourceToMerge.equals(existingMapper.mappingSource())) {\n                context.resetForNoopMappingUpdateRetry(initialMappingVersion);\n                return true;\n            }",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1651609389",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1651609389",
        "commented_code": "@@ -405,16 +403,24 @@ private static boolean handleMappingUpdateRequired(\n         long version,\n         UpdateHelper.Result updateResult\n     ) {\n-        final var mapperService = primary.mapperService();\n         try {\n+            final var sourceToMerge = new CompressedXContent(result.getRequiredMappingUpdate());\n+            final var mapperService = primary.mapperService();\n+            final long initialMappingVersion = mapperService.mappingVersion();\n+            final var existingMapper = mapperService.documentMapper();\n+            if (existingMapper != null && sourceToMerge.equals(existingMapper.mappingSource())) {\n+                context.resetForNoopMappingUpdateRetry(initialMappingVersion);\n+                return true;\n+            }",
        "comment_created_at": "2024-06-24T21:05:28+00:00",
        "comment_author": "javanna",
        "comment_body": "Do you have a scenario in mind where this will help specifically? You are comparing the dynamic mapping update with the existing mappings, when are those two going to be the same?",
        "pr_file_module": null
      },
      {
        "comment_id": "1652749658",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1651609389",
        "commented_code": "@@ -405,16 +403,24 @@ private static boolean handleMappingUpdateRequired(\n         long version,\n         UpdateHelper.Result updateResult\n     ) {\n-        final var mapperService = primary.mapperService();\n         try {\n+            final var sourceToMerge = new CompressedXContent(result.getRequiredMappingUpdate());\n+            final var mapperService = primary.mapperService();\n+            final long initialMappingVersion = mapperService.mappingVersion();\n+            final var existingMapper = mapperService.documentMapper();\n+            if (existingMapper != null && sourceToMerge.equals(existingMapper.mappingSource())) {\n+                context.resetForNoopMappingUpdateRetry(initialMappingVersion);\n+                return true;\n+            }",
        "comment_created_at": "2024-06-25T12:42:52+00:00",
        "comment_author": "original-brownbear",
        "comment_body": "Yea, after failing over to a new index when a bunch of data nodes are blasting the master all with the same update. No need to waste energy on all write threads and the master for longer than absolutely necessary IMO :)",
        "pr_file_module": null
      },
      {
        "comment_id": "1653529791",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1651609389",
        "commented_code": "@@ -405,16 +403,24 @@ private static boolean handleMappingUpdateRequired(\n         long version,\n         UpdateHelper.Result updateResult\n     ) {\n-        final var mapperService = primary.mapperService();\n         try {\n+            final var sourceToMerge = new CompressedXContent(result.getRequiredMappingUpdate());\n+            final var mapperService = primary.mapperService();\n+            final long initialMappingVersion = mapperService.mappingVersion();\n+            final var existingMapper = mapperService.documentMapper();\n+            if (existingMapper != null && sourceToMerge.equals(existingMapper.mappingSource())) {\n+                context.resetForNoopMappingUpdateRetry(initialMappingVersion);\n+                return true;\n+            }",
        "comment_created_at": "2024-06-25T20:38:44+00:00",
        "comment_author": "javanna",
        "comment_body": "I don't understand how the conditional is matched in that scenario: how can the existing mappings be exactly the same as the dynamic mapping update? The existing mappings hold all the fields that have been added until then, and the new mappings hold the updates to be made following indexing of a new document. Say that we are indexing the first doc of a new index, the dynamic mapping update would contain a lot of fields, and the existing mappings would be empty?  I am sure I am missing something, can you help me better understand?",
        "pr_file_module": null
      },
      {
        "comment_id": "1653536880",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1651609389",
        "commented_code": "@@ -405,16 +403,24 @@ private static boolean handleMappingUpdateRequired(\n         long version,\n         UpdateHelper.Result updateResult\n     ) {\n-        final var mapperService = primary.mapperService();\n         try {\n+            final var sourceToMerge = new CompressedXContent(result.getRequiredMappingUpdate());\n+            final var mapperService = primary.mapperService();\n+            final long initialMappingVersion = mapperService.mappingVersion();\n+            final var existingMapper = mapperService.documentMapper();\n+            if (existingMapper != null && sourceToMerge.equals(existingMapper.mappingSource())) {\n+                context.resetForNoopMappingUpdateRetry(initialMappingVersion);\n+                return true;\n+            }",
        "comment_created_at": "2024-06-25T20:45:02+00:00",
        "comment_author": "original-brownbear",
        "comment_body": "> I don't understand how the conditional is matched in that scenario: how can the existing mappings be exactly the same as the dynamic mapping update?\r\n\r\nI think that's when we bootstrap a new index that uses dynamic mapping updates. If you index the same kind of logs that will trigger the same mapping in parallel, you will and should get the exact same mapping here every time (like think some metrics line from Metricbeat or so).\r\n\r\n> Say that we are indexing the first doc of a new index, the dynamic mapping update would contain a lot of fields, and the existing mappings would be empty\r\n\r\nJup exactly. E.g. Elasticsearch detailed node stats I'd say :P that's a couple hundred fields that would get created in the dynamic updates. No need to ship that out from write threads more often than absolutely necessary every time we roll-over an index.\r\n",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1633466723",
    "pr_number": 109390,
    "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
    "created_at": "2024-06-10T15:41:56+00:00",
    "commented_code": "}\n\n    public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n            try {\n                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n                    WriteRequest.RefreshPolicy.IMMEDIATE\n                );\n                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n                        ? UpdateSynonymsResultStatus.CREATED\n                        : UpdateSynonymsResultStatus.UPDATED;\n\n                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n            // Count synonym rules to check if we're at maximum\n            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n                .setQuery(\n                    QueryBuilders.boolQuery()\n                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n                )\n                .setSize(0)\n                .setPreference(Preference.LOCAL.type())\n                .setTrackTotalHits(true)\n                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1633466723",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-10T15:41:56+00:00",
        "comment_author": "kderusso",
        "comment_body": "We could consider supporting updates here by adding a `must_not` clause to the query on the synonym ID? Then it would be below the max if it existed.",
        "pr_file_module": null
      },
      {
        "comment_id": "1633545813",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-10T16:44:43+00:00",
        "comment_author": "carlosdelest",
        "comment_body": "That's a good way of doing this! Again, I feel it a bit complicated for such an edge case.",
        "pr_file_module": null
      },
      {
        "comment_id": "1638117253",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-13T12:24:10+00:00",
        "comment_author": "kderusso",
        "comment_body": "I do think it's worth taking this edge case into consideration, because you know someone is going to try it and file a bug later. ",
        "pr_file_module": null
      },
      {
        "comment_id": "1638197058",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-13T13:14:54+00:00",
        "comment_author": "jimczi",
        "comment_body": "Agreed, it's not really an edge case to be at capacity and to update the existing rules. I think we need a more robust approach here like executing all updates on the master node and executing the updates sequentially.",
        "pr_file_module": null
      },
      {
        "comment_id": "1638282360",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-13T14:05:20+00:00",
        "comment_author": "carlosdelest",
        "comment_body": "> it's not really an edge case to be at capacity and to update the existing rules\r\n\r\nThis edge case happens only if we're updating an individual synonym rule when we're at max capacity. Updating rules in batch means that first we remove all the rules and apply the updates in a bulk request.\r\n\r\nIt sounds weird to me to update individual rules when we have 100k synonyms in a synonym set- at that scale, I would think that users do batch updates of rules, which effectively replace the existing ones.\r\n\r\nBut if y'all think this needs to be dealt with, I will! I'll update the code and ping when ready \ud83d\udc4d \r\n\r\n> I think we need a more robust approach here like executing all updates on the master node and executing the updates sequentially\r\n\r\nSo do you think that this should be a `TransportMasterNodeAction`? As this updates an index and not the cluster state, what would be the advantages of applying the action on the master node? \r\n\r\nAs we're doing a bulk request under the hood, doesn't that mean that we're applying the updates sequentially?",
        "pr_file_module": null
      },
      {
        "comment_id": "1638334270",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-13T14:36:16+00:00",
        "comment_author": "jimczi",
        "comment_body": "> Updating rules in batch means that first we remove all the rules and apply the updates in a bulk request.\r\n\r\nThis is another case of non-consistent updates, we need to ensure some ordering here.\r\n\r\n> So do you think that this should be a TransportMasterNodeAction? As this updates an index and not the cluster state, what would be the advantages of applying the action on the master node?\r\n\r\nHaving a single place where updates can occur but as you noticed that won't be enough. We also need to ensure that all updates are done sequentially, not in a single bulk request but globally when multiple synonyms updates are done in parallel. See the `MetadataMappingService` for an example of service that applies updates sequentially. \r\n\r\n",
        "pr_file_module": null
      },
      {
        "comment_id": "1638341068",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-13T14:40:13+00:00",
        "comment_author": "carlosdelest",
        "comment_body": "Thanks @jimczi , I will take a look into that.\r\n\r\nI think we should create a separate issue for ensuring updates are applied sequentially, as this is not directly related to this change?",
        "pr_file_module": null
      },
      {
        "comment_id": "1638388512",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109390,
        "pr_file": "server/src/main/java/org/elasticsearch/synonyms/SynonymsManagementAPIService.java",
        "discussion_id": "1633466723",
        "commented_code": "@@ -308,21 +355,42 @@ public void putSynonymsSet(String synonymSetId, SynonymRule[] synonymsSet, Actio\n     }\n \n     public void putSynonymRule(String synonymsSetId, SynonymRule synonymRule, ActionListener<SynonymsReloadResult> listener) {\n-        checkSynonymSetExists(synonymsSetId, listener.delegateFailure((l1, obj) -> {\n-            try {\n-                IndexRequest indexRequest = createSynonymRuleIndexRequest(synonymsSetId, synonymRule).setRefreshPolicy(\n-                    WriteRequest.RefreshPolicy.IMMEDIATE\n-                );\n-                client.index(indexRequest, l1.delegateFailure((l2, indexResponse) -> {\n-                    UpdateSynonymsResultStatus updateStatus = indexResponse.status() == RestStatus.CREATED\n-                        ? UpdateSynonymsResultStatus.CREATED\n-                        : UpdateSynonymsResultStatus.UPDATED;\n-\n-                    reloadAnalyzers(synonymsSetId, false, l2, updateStatus);\n+        checkSynonymSetExists(synonymsSetId, listener.delegateFailureAndWrap((l1, obj) -> {\n+            // Count synonym rules to check if we're at maximum\n+            client.prepareSearch(SYNONYMS_ALIAS_NAME)\n+                .setQuery(\n+                    QueryBuilders.boolQuery()\n+                        .must(QueryBuilders.termQuery(SYNONYMS_SET_FIELD, synonymsSetId))\n+                        .filter(QueryBuilders.termQuery(OBJECT_TYPE_FIELD, SYNONYM_RULE_OBJECT_TYPE))\n+                )\n+                .setSize(0)\n+                .setPreference(Preference.LOCAL.type())\n+                .setTrackTotalHits(true)\n+                .execute(l1.delegateFailureAndWrap((searchListener, searchResponse) -> {\n+                    long synonymsSetSize = searchResponse.getHits().getTotalHits().value;\n+                    if (synonymsSetSize >= MAX_SYNONYMS_SETS) {\n+                        // We could potentially update a synonym rule when we're at max capacity, but we're keeping this simple",
        "comment_created_at": "2024-06-13T15:09:25+00:00",
        "comment_author": "jimczi",
        "comment_body": "I think it's related, we cannot limit the number of synonyms without ensuring that updates are applied sequentially.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2177518712",
    "pr_number": 130387,
    "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
    "created_at": "2025-07-01T12:46:28+00:00",
    "commented_code": "return ft;\n        }\n\n        /**\n         * Does a `match` query generate all valid candidates for `==`? Meaning,\n         * if I do a match query for any string, say `foo bar baz`, then that\n         * query will find all documents that indexed the same string.\n         * <p>\n         *     This should be true for most sanely configured text fields. That's\n         *     just how we use them for search. But it's quite possible to make\n         *     the index analyzer not agree with the search analyzer, for example.\n         * </p>\n         * <p>\n         *     So this implementation is ultra-paranoid.\n         * </p>\n         */\n        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n            return index.getValue() == Boolean.TRUE\n                && analyzers.indexAnalyzer.isConfigured() == false\n                && analyzers.searchAnalyzer.isConfigured() == false;\n        }",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2177518712",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130387,
        "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
        "discussion_id": "2177518712",
        "commented_code": "@@ -422,6 +424,25 @@ private TextFieldType buildFieldType(\n             return ft;\n         }\n \n+        /**\n+         * Does a `match` query generate all valid candidates for `==`? Meaning,\n+         * if I do a match query for any string, say `foo bar baz`, then that\n+         * query will find all documents that indexed the same string.\n+         * <p>\n+         *     This should be true for most sanely configured text fields. That's\n+         *     just how we use them for search. But it's quite possible to make\n+         *     the index analyzer not agree with the search analyzer, for example.\n+         * </p>\n+         * <p>\n+         *     So this implementation is ultra-paranoid.\n+         * </p>\n+         */\n+        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n+            return index.getValue() == Boolean.TRUE\n+                && analyzers.indexAnalyzer.isConfigured() == false\n+                && analyzers.searchAnalyzer.isConfigured() == false;\n+        }",
        "comment_created_at": "2025-07-01T12:46:28+00:00",
        "comment_author": "nik9000",
        "comment_body": "==SEARCH FOLKS LOOK HERE==\r\n\r\nIs this paranoid enough? Like, could you break the `match` query with other settings I'm not checking? I'd love to default this to only working if there's nothing configured on the text field and then opt in configurations.",
        "pr_file_module": null
      },
      {
        "comment_id": "2177582793",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130387,
        "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
        "discussion_id": "2177518712",
        "commented_code": "@@ -422,6 +424,25 @@ private TextFieldType buildFieldType(\n             return ft;\n         }\n \n+        /**\n+         * Does a `match` query generate all valid candidates for `==`? Meaning,\n+         * if I do a match query for any string, say `foo bar baz`, then that\n+         * query will find all documents that indexed the same string.\n+         * <p>\n+         *     This should be true for most sanely configured text fields. That's\n+         *     just how we use them for search. But it's quite possible to make\n+         *     the index analyzer not agree with the search analyzer, for example.\n+         * </p>\n+         * <p>\n+         *     So this implementation is ultra-paranoid.\n+         * </p>\n+         */\n+        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n+            return index.getValue() == Boolean.TRUE\n+                && analyzers.indexAnalyzer.isConfigured() == false\n+                && analyzers.searchAnalyzer.isConfigured() == false;\n+        }",
        "comment_created_at": "2025-07-01T13:17:25+00:00",
        "comment_author": "jimczi",
        "comment_body": "This is paranoid indeed. Just checking if the analyzer are the same is not enough since we have morphological analyzer that can tokenize differently depending on the surrounding text (Kuromoji, Nori, ..).\r\nWe could have a list of `allowed` analyzers but that sounds like a good start that will handle 99% of the use cases. \r\nI can't think of another setting that would change this, are we matching the input as phrase query or as a conjunction of term?",
        "pr_file_module": null
      },
      {
        "comment_id": "2177603114",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130387,
        "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
        "discussion_id": "2177518712",
        "commented_code": "@@ -422,6 +424,25 @@ private TextFieldType buildFieldType(\n             return ft;\n         }\n \n+        /**\n+         * Does a `match` query generate all valid candidates for `==`? Meaning,\n+         * if I do a match query for any string, say `foo bar baz`, then that\n+         * query will find all documents that indexed the same string.\n+         * <p>\n+         *     This should be true for most sanely configured text fields. That's\n+         *     just how we use them for search. But it's quite possible to make\n+         *     the index analyzer not agree with the search analyzer, for example.\n+         * </p>\n+         * <p>\n+         *     So this implementation is ultra-paranoid.\n+         * </p>\n+         */\n+        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n+            return index.getValue() == Boolean.TRUE\n+                && analyzers.indexAnalyzer.isConfigured() == false\n+                && analyzers.searchAnalyzer.isConfigured() == false;\n+        }",
        "comment_created_at": "2025-07-01T13:24:52+00:00",
        "comment_author": "nik9000",
        "comment_body": "Conjunction of terms right now. I probably should do phrase to be honest.",
        "pr_file_module": null
      },
      {
        "comment_id": "2177608120",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130387,
        "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
        "discussion_id": "2177518712",
        "commented_code": "@@ -422,6 +424,25 @@ private TextFieldType buildFieldType(\n             return ft;\n         }\n \n+        /**\n+         * Does a `match` query generate all valid candidates for `==`? Meaning,\n+         * if I do a match query for any string, say `foo bar baz`, then that\n+         * query will find all documents that indexed the same string.\n+         * <p>\n+         *     This should be true for most sanely configured text fields. That's\n+         *     just how we use them for search. But it's quite possible to make\n+         *     the index analyzer not agree with the search analyzer, for example.\n+         * </p>\n+         * <p>\n+         *     So this implementation is ultra-paranoid.\n+         * </p>\n+         */\n+        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n+            return index.getValue() == Boolean.TRUE\n+                && analyzers.indexAnalyzer.isConfigured() == false\n+                && analyzers.searchAnalyzer.isConfigured() == false;\n+        }",
        "comment_created_at": "2025-07-01T13:26:59+00:00",
        "comment_author": "nik9000",
        "comment_body": "Do you think it's worth building a field setting that overrides our choices? A `true/false/null` thing - `true` means \"I know match is fine, push\", `false` means \"I know match isn't fine, never push\" and `null` means \"you figure it out\".\r\n\r\n> since we have morphological analyzer that can tokenize differently depending on the surrounding text (Kuromoji, Nori, ..)\r\n\r\nCan you give an example? So long as the same text tokenizes the same way that *should* be fine. We're not pushing \"contains tokens\" here - we're pushing exat string ==.",
        "pr_file_module": null
      },
      {
        "comment_id": "2177644488",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130387,
        "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
        "discussion_id": "2177518712",
        "commented_code": "@@ -422,6 +424,25 @@ private TextFieldType buildFieldType(\n             return ft;\n         }\n \n+        /**\n+         * Does a `match` query generate all valid candidates for `==`? Meaning,\n+         * if I do a match query for any string, say `foo bar baz`, then that\n+         * query will find all documents that indexed the same string.\n+         * <p>\n+         *     This should be true for most sanely configured text fields. That's\n+         *     just how we use them for search. But it's quite possible to make\n+         *     the index analyzer not agree with the search analyzer, for example.\n+         * </p>\n+         * <p>\n+         *     So this implementation is ultra-paranoid.\n+         * </p>\n+         */\n+        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n+            return index.getValue() == Boolean.TRUE\n+                && analyzers.indexAnalyzer.isConfigured() == false\n+                && analyzers.searchAnalyzer.isConfigured() == false;\n+        }",
        "comment_created_at": "2025-07-01T13:43:11+00:00",
        "comment_author": "jimczi",
        "comment_body": "> Can you give an example? So long as the same text tokenizes the same way that should be fine. We're not pushing \"contains tokens\" here - we're pushing exat string ==.\r\n\r\nAh right sorry, the input must be exactly the same. So then another test, to remove the analyzer restriction, would be to use a memory index and verify that the search analyzer query can find the input indexed with the index analyzer?\r\n\r\n> Do you think it's worth building a field setting that overrides our choices?\r\n\r\nI wonder if that should be pushed down to mappings directly. We have `termQuery`, `phraseQuery` defined by the field mappers now so we could delegate the decision there with an `exactQuery`? That would help with fields like `match_only_text` to avoid doing two verifications on the content? ",
        "pr_file_module": null
      },
      {
        "comment_id": "2177655532",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130387,
        "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
        "discussion_id": "2177518712",
        "commented_code": "@@ -422,6 +424,25 @@ private TextFieldType buildFieldType(\n             return ft;\n         }\n \n+        /**\n+         * Does a `match` query generate all valid candidates for `==`? Meaning,\n+         * if I do a match query for any string, say `foo bar baz`, then that\n+         * query will find all documents that indexed the same string.\n+         * <p>\n+         *     This should be true for most sanely configured text fields. That's\n+         *     just how we use them for search. But it's quite possible to make\n+         *     the index analyzer not agree with the search analyzer, for example.\n+         * </p>\n+         * <p>\n+         *     So this implementation is ultra-paranoid.\n+         * </p>\n+         */\n+        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n+            return index.getValue() == Boolean.TRUE\n+                && analyzers.indexAnalyzer.isConfigured() == false\n+                && analyzers.searchAnalyzer.isConfigured() == false;\n+        }",
        "comment_created_at": "2025-07-01T13:47:59+00:00",
        "comment_author": "jimczi",
        "comment_body": "cc @javanna ",
        "pr_file_module": null
      },
      {
        "comment_id": "2179888009",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130387,
        "pr_file": "server/src/main/java/org/elasticsearch/index/mapper/TextFieldMapper.java",
        "discussion_id": "2177518712",
        "commented_code": "@@ -422,6 +424,25 @@ private TextFieldType buildFieldType(\n             return ft;\n         }\n \n+        /**\n+         * Does a `match` query generate all valid candidates for `==`? Meaning,\n+         * if I do a match query for any string, say `foo bar baz`, then that\n+         * query will find all documents that indexed the same string.\n+         * <p>\n+         *     This should be true for most sanely configured text fields. That's\n+         *     just how we use them for search. But it's quite possible to make\n+         *     the index analyzer not agree with the search analyzer, for example.\n+         * </p>\n+         * <p>\n+         *     So this implementation is ultra-paranoid.\n+         * </p>\n+         */\n+        private boolean matchQueryYieldsCandidateMatchesForEquality() {\n+            return index.getValue() == Boolean.TRUE\n+                && analyzers.indexAnalyzer.isConfigured() == false\n+                && analyzers.searchAnalyzer.isConfigured() == false;\n+        }",
        "comment_created_at": "2025-07-02T12:09:04+00:00",
        "comment_author": "nik9000",
        "comment_body": "I think ESQL might indeed deserve some more query methods on `MappedFieldType`. I've been adding methods to, like, `TextFieldMapper` that help me decide what query to build. But I think it'd be cleaner to put these into the `MappedFieldType`. Also, it'd be more possible for, well, more fields to link into ESQL.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2172861734",
    "pr_number": 129282,
    "pr_file": "x-pack/plugin/inference/src/main/java/org/elasticsearch/xpack/inference/queries/SemanticMatchQueryRewriteInterceptor.java",
    "created_at": "2025-06-27T20:54:05+00:00",
    "commented_code": "boolQueryBuilder.should(\n            createSemanticSubQuery(\n                indexInformation.getInferenceIndices(),\n                matchQueryBuilder.fieldName(),\n                (String) matchQueryBuilder.value()\n                matchQueryBuilder\n            )\n        );\n        boolQueryBuilder.should(createSubQueryForIndices(indexInformation.nonInferenceIndices(), matchQueryBuilder));\n        boolQueryBuilder.boost(matchQueryBuilder.boost());\n        boolQueryBuilder.queryName(matchQueryBuilder.queryName());\n        return boolQueryBuilder;",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2172861734",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129282,
        "pr_file": "x-pack/plugin/inference/src/main/java/org/elasticsearch/xpack/inference/queries/SemanticMatchQueryRewriteInterceptor.java",
        "discussion_id": "2172861734",
        "commented_code": "@@ -50,11 +50,12 @@ protected QueryBuilder buildCombinedInferenceAndNonInferenceQuery(\n         boolQueryBuilder.should(\n             createSemanticSubQuery(\n                 indexInformation.getInferenceIndices(),\n-                matchQueryBuilder.fieldName(),\n-                (String) matchQueryBuilder.value()\n+                matchQueryBuilder\n             )\n         );\n         boolQueryBuilder.should(createSubQueryForIndices(indexInformation.nonInferenceIndices(), matchQueryBuilder));\n+        boolQueryBuilder.boost(matchQueryBuilder.boost());\n+        boolQueryBuilder.queryName(matchQueryBuilder.queryName());\n         return boolQueryBuilder;",
        "comment_created_at": "2025-06-27T20:54:05+00:00",
        "comment_author": "Samiul-TheSoccerFan",
        "comment_body": "The final Query for `match` will look something like this:\r\n\r\n```\r\n{\r\n  \"bool\" : {\r\n    \"should\" : [ {\r\n      \"bool\" : {\r\n        \"should\" : [ {\r\n          \"bool\" : {\r\n            \"must\" : [ {\r\n              \"semantic\" : {\r\n                \"field\" : \"semantic1\",\r\n                \"query\" : \"wolf\",\r\n                \"lenient\" : true\r\n              }\r\n            } ],\r\n            \"filter\" : [ {\r\n              \"terms\" : {\r\n                \"_index\" : [ \"semantic-text-index\" ],\r\n                \"boost\" : 1.0\r\n              }\r\n            } ],\r\n            \"boost\" : 1.0\r\n          }\r\n        }, {\r\n          \"bool\" : {\r\n            \"must\" : [ {\r\n              \"match\" : {\r\n                \"semantic1\" : {\r\n                  \"query\" : \"wolf\",\r\n                  \"boost\" : 3.0,\r\n                  \"_name\" : \"semantic1_match\"\r\n                }\r\n              }\r\n            } ],\r\n            \"filter\" : [ {\r\n              \"terms\" : {\r\n                \"_index\" : [ \"normal-text-index\" ],\r\n                \"boost\" : 1.0\r\n              }\r\n            } ],\r\n            \"boost\" : 1.0\r\n          }\r\n        } ],\r\n        \"boost\" : 3.0,\r\n        \"_name\" : \"semantic1_match\"\r\n      }\r\n    }, {\r\n      \"bool\" : {\r\n        \"should\" : [ {\r\n          \"bool\" : {\r\n            \"must\" : [ {\r\n              \"semantic\" : {\r\n                \"field\" : \"semantic2\",\r\n                \"query\" : \"strangers\",\r\n                \"lenient\" : true\r\n              }\r\n            } ],\r\n            \"filter\" : [ {\r\n              \"terms\" : {\r\n                \"_index\" : [ \"semantic-text-index\" ],\r\n                \"boost\" : 1.0\r\n              }\r\n            } ],\r\n            \"boost\" : 1.0\r\n          }\r\n        }, {\r\n          \"bool\" : {\r\n            \"must\" : [ {\r\n              \"match\" : {\r\n                \"semantic2\" : {\r\n                  \"query\" : \"strangers\",\r\n                  \"boost\" : 2.5,\r\n                  \"_name\" : \"semantic2_match\"\r\n                }\r\n              }\r\n            } ],\r\n            \"filter\" : [ {\r\n              \"terms\" : {\r\n                \"_index\" : [ \"normal-text-index\" ],\r\n                \"boost\" : 1.0\r\n              }\r\n            } ],\r\n            \"boost\" : 1.0\r\n          }\r\n        } ],\r\n        \"boost\" : 2.5,\r\n        \"_name\" : \"semantic2_match\"\r\n      }\r\n    } ],\r\n    \"boost\" : 1.0\r\n  }\r\n}\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2167423740",
    "pr_number": 130035,
    "pr_file": "x-pack/plugin/migrate/src/main/java/org/elasticsearch/xpack/migrate/action/ReindexDataStreamIndexTransportAction.java",
    "created_at": "2025-06-25T19:07:18+00:00",
    "commented_code": "ReindexDataStreamIndexAction.Request request,\n        ActionListener<ReindexDataStreamIndexAction.Response> listener\n    ) {\n        var project = clusterService.state().projectState();\n        var project = projectResolver.getProjectState(clusterService.state());",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2167423740",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130035,
        "pr_file": "x-pack/plugin/migrate/src/main/java/org/elasticsearch/xpack/migrate/action/ReindexDataStreamIndexTransportAction.java",
        "discussion_id": "2167423740",
        "commented_code": "@@ -142,7 +146,7 @@ protected void doExecute(\n         ReindexDataStreamIndexAction.Request request,\n         ActionListener<ReindexDataStreamIndexAction.Response> listener\n     ) {\n-        var project = clusterService.state().projectState();\n+        var project = projectResolver.getProjectState(clusterService.state());",
        "comment_created_at": "2025-06-25T19:07:18+00:00",
        "comment_author": "nielsbauman",
        "comment_body": "Since we only use the `ProjectMetadata` in this method, we can avoid constructing the `ProjectState` by using `projectResolver.getProjectMetadata(clusterService.state())`.",
        "pr_file_module": null
      },
      {
        "comment_id": "2167646421",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130035,
        "pr_file": "x-pack/plugin/migrate/src/main/java/org/elasticsearch/xpack/migrate/action/ReindexDataStreamIndexTransportAction.java",
        "discussion_id": "2167423740",
        "commented_code": "@@ -142,7 +146,7 @@ protected void doExecute(\n         ReindexDataStreamIndexAction.Request request,\n         ActionListener<ReindexDataStreamIndexAction.Response> listener\n     ) {\n-        var project = clusterService.state().projectState();\n+        var project = projectResolver.getProjectState(clusterService.state());",
        "comment_created_at": "2025-06-25T21:14:27+00:00",
        "comment_author": "joegallo",
        "comment_body": "34e98085388cae88b1299732e99903b2b7df7d2c",
        "pr_file_module": null
      }
    ]
  }
]
