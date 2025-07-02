---
title: Extract for clarity
description: 'Extract complex or reused logic into focused, well-named methods with
  single responsibilities. This improves code readability, testability, and maintainability
  while reducing duplication. When refactoring:'
repository: elastic/elasticsearch
label: Code Style
language: Java
comments_count: 16
repository_stars: 73104
---

Extract complex or reused logic into focused, well-named methods with single responsibilities. This improves code readability, testability, and maintainability while reducing duplication. When refactoring:

1. Identify blocks of code that perform a distinct task or are used in multiple places
2. Extract them into appropriately named methods
3. Keep the scope of annotations like `@SuppressForbidden` minimal by extracting annotated code into dedicated helper methods
4. Consider creating separate classes for related logic sets

For example, instead of placing complex logic inline:

```java
@SuppressForbidden(
    reason = "TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993"
)
public static boolean parseBoolean(String value) {
    // complex implementation
    return Boolean.parseBoolean(value);
}
```

Extract it to minimize annotation scope:

```java
public static boolean parseBoolean(String value) {
    return parseBooleanInternal(value);
}

@SuppressForbidden(
    reason = "TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993"
)
private static boolean parseBooleanInternal(String value) {
    return Boolean.parseBoolean(value);
}
```

For complex class functionality, consider isolating related methods:

```java
// Comment from Discussion 6: 
// "A logistical suggestion would be to isolate all the InlineJoin logic into its own class 
// (could be nested), as there are a few methods here (plus this record) 
// that are dedicated just for this feature."
```

This approach makes code more maintainable, easier to understand, and simplifies future changes.


[
  {
    "discussion_id": "2166743201",
    "pr_number": 128917,
    "pr_file": "x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/session/EsqlSession.java",
    "created_at": "2025-06-25T13:37:18+00:00",
    "commented_code": "LogicalPlan optimizedPlan,\n        ActionListener<Result> listener\n    ) {\n        PhysicalPlan physicalPlan = logicalPlanToPhysicalPlan(optimizedPlan, request);\n        // TODO: this could be snuck into the underlying listener\n        EsqlCCSUtils.updateExecutionInfoAtEndOfPlanning(executionInfo);\n        // execute any potential subplans\n        executeSubPlans(physicalPlan, planRunner, executionInfo, request, listener);\n        executeSubPlans(optimizedPlan, planRunner, executionInfo, request, listener);\n    }\n\n    private record PlanTuple(PhysicalPlan physical, LogicalPlan logical) {}\n    private record LogicalPlanTuple(LogicalPlan nonStubbedSubPlan, LogicalPlan originalSubPlan) {}\n\n    private void executeSubPlans(\n        PhysicalPlan physicalPlan,\n        LogicalPlan optimizedPlan,\n        PlanRunner runner,\n        EsqlExecutionInfo executionInfo,\n        EsqlQueryRequest request,\n        ActionListener<Result> listener\n    ) {\n        List<PlanTuple> subplans = new ArrayList<>();\n\n        // Currently the inlinestats are limited and supported as streaming operators, thus present inside the fragment as logical plans\n        // Below they get collected, translated into a separate, coordinator based plan and the results 'broadcasted' as a local relation\n        physicalPlan.forEachUp(FragmentExec.class, f -> {\n            f.fragment().forEachUp(InlineJoin.class, ij -> {\n                // extract the right side of the plan and replace its source\n                LogicalPlan subplan = InlineJoin.replaceStub(ij.left(), ij.right());\n                // mark the new root node as optimized\n                subplan.setOptimized();\n                PhysicalPlan subqueryPlan = logicalPlanToPhysicalPlan(subplan, request);\n                subplans.add(new PlanTuple(subqueryPlan, ij.right()));\n            });\n        });\n\n        Iterator<PlanTuple> iterator = subplans.iterator();\n        var subPlan = firstSubPlan(optimizedPlan);\n\n        // TODO: merge into one method\n        if (subplans.size() > 0) {\n        if (subPlan != null) {\n            // code-path to execute subplans\n            executeSubPlan(new DriverCompletionInfo.Accumulator(), physicalPlan, iterator, executionInfo, runner, listener);\n            executeSubPlan(new DriverCompletionInfo.Accumulator(), optimizedPlan, subPlan, executionInfo, runner, request, listener);\n        } else {\n            PhysicalPlan physicalPlan = logicalPlanToPhysicalPlan(optimizedPlan, request);\n            // execute main plan\n            runner.run(physicalPlan, listener);\n        }\n    }\n\n    private LogicalPlanTuple firstSubPlan(LogicalPlan optimizedPlan) {\n        Holder<LogicalPlanTuple> subPlan = new Holder<>();\n        // Collect the first inlinejoin (bottom up in the tree)\n        optimizedPlan.forEachUp(InlineJoin.class, ij -> {\n            // extract the right side of the plan and replace its source\n            if (subPlan.get() == null && ij.right().anyMatch(p -> p instanceof StubRelation)) {\n                var p = InlineJoin.replaceStub(ij.left(), ij.right());\n                p.setOptimized();\n                subPlan.set(new LogicalPlanTuple(p, ij.right()));\n            }\n        });\n        return subPlan.get();\n    }\n\n    private void executeSubPlan(\n        DriverCompletionInfo.Accumulator completionInfoAccumulator,\n        PhysicalPlan plan,\n        Iterator<PlanTuple> subPlanIterator,\n        LogicalPlan optimizedPlan,\n        LogicalPlanTuple subPlans,\n        EsqlExecutionInfo executionInfo,\n        PlanRunner runner,\n        EsqlQueryRequest request,\n        ActionListener<Result> listener\n    ) {\n        PlanTuple tuple = subPlanIterator.next();\n        // Create a physical plan out of the logical sub-plan\n        var physicalSubPlan = logicalPlanToPhysicalPlan(subPlans.nonStubbedSubPlan, request);\n\n        runner.run(tuple.physical, listener.delegateFailureAndWrap((next, result) -> {\n        runner.run(physicalSubPlan, listener.delegateFailureAndWrap((next, result) -> {\n            try {\n                // Translate the subquery into a separate, coordinator based plan and the results 'broadcasted' as a local relation\n                completionInfoAccumulator.accumulate(result.completionInfo());\n                LocalRelation resultWrapper = resultToPlan(tuple.logical, result);\n                LocalRelation resultWrapper = resultToPlan(subPlans.nonStubbedSubPlan, result);",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2166743201",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 128917,
        "pr_file": "x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/session/EsqlSession.java",
        "discussion_id": "2166743201",
        "commented_code": "@@ -207,85 +206,85 @@ public void executeOptimizedPlan(\n         LogicalPlan optimizedPlan,\n         ActionListener<Result> listener\n     ) {\n-        PhysicalPlan physicalPlan = logicalPlanToPhysicalPlan(optimizedPlan, request);\n         // TODO: this could be snuck into the underlying listener\n         EsqlCCSUtils.updateExecutionInfoAtEndOfPlanning(executionInfo);\n         // execute any potential subplans\n-        executeSubPlans(physicalPlan, planRunner, executionInfo, request, listener);\n+        executeSubPlans(optimizedPlan, planRunner, executionInfo, request, listener);\n     }\n \n-    private record PlanTuple(PhysicalPlan physical, LogicalPlan logical) {}\n+    private record LogicalPlanTuple(LogicalPlan nonStubbedSubPlan, LogicalPlan originalSubPlan) {}\n \n     private void executeSubPlans(\n-        PhysicalPlan physicalPlan,\n+        LogicalPlan optimizedPlan,\n         PlanRunner runner,\n         EsqlExecutionInfo executionInfo,\n         EsqlQueryRequest request,\n         ActionListener<Result> listener\n     ) {\n-        List<PlanTuple> subplans = new ArrayList<>();\n-\n-        // Currently the inlinestats are limited and supported as streaming operators, thus present inside the fragment as logical plans\n-        // Below they get collected, translated into a separate, coordinator based plan and the results 'broadcasted' as a local relation\n-        physicalPlan.forEachUp(FragmentExec.class, f -> {\n-            f.fragment().forEachUp(InlineJoin.class, ij -> {\n-                // extract the right side of the plan and replace its source\n-                LogicalPlan subplan = InlineJoin.replaceStub(ij.left(), ij.right());\n-                // mark the new root node as optimized\n-                subplan.setOptimized();\n-                PhysicalPlan subqueryPlan = logicalPlanToPhysicalPlan(subplan, request);\n-                subplans.add(new PlanTuple(subqueryPlan, ij.right()));\n-            });\n-        });\n-\n-        Iterator<PlanTuple> iterator = subplans.iterator();\n+        var subPlan = firstSubPlan(optimizedPlan);\n \n         // TODO: merge into one method\n-        if (subplans.size() > 0) {\n+        if (subPlan != null) {\n             // code-path to execute subplans\n-            executeSubPlan(new DriverCompletionInfo.Accumulator(), physicalPlan, iterator, executionInfo, runner, listener);\n+            executeSubPlan(new DriverCompletionInfo.Accumulator(), optimizedPlan, subPlan, executionInfo, runner, request, listener);\n         } else {\n+            PhysicalPlan physicalPlan = logicalPlanToPhysicalPlan(optimizedPlan, request);\n             // execute main plan\n             runner.run(physicalPlan, listener);\n         }\n     }\n \n+    private LogicalPlanTuple firstSubPlan(LogicalPlan optimizedPlan) {\n+        Holder<LogicalPlanTuple> subPlan = new Holder<>();\n+        // Collect the first inlinejoin (bottom up in the tree)\n+        optimizedPlan.forEachUp(InlineJoin.class, ij -> {\n+            // extract the right side of the plan and replace its source\n+            if (subPlan.get() == null && ij.right().anyMatch(p -> p instanceof StubRelation)) {\n+                var p = InlineJoin.replaceStub(ij.left(), ij.right());\n+                p.setOptimized();\n+                subPlan.set(new LogicalPlanTuple(p, ij.right()));\n+            }\n+        });\n+        return subPlan.get();\n+    }\n+\n     private void executeSubPlan(\n         DriverCompletionInfo.Accumulator completionInfoAccumulator,\n-        PhysicalPlan plan,\n-        Iterator<PlanTuple> subPlanIterator,\n+        LogicalPlan optimizedPlan,\n+        LogicalPlanTuple subPlans,\n         EsqlExecutionInfo executionInfo,\n         PlanRunner runner,\n+        EsqlQueryRequest request,\n         ActionListener<Result> listener\n     ) {\n-        PlanTuple tuple = subPlanIterator.next();\n+        // Create a physical plan out of the logical sub-plan\n+        var physicalSubPlan = logicalPlanToPhysicalPlan(subPlans.nonStubbedSubPlan, request);\n \n-        runner.run(tuple.physical, listener.delegateFailureAndWrap((next, result) -> {\n+        runner.run(physicalSubPlan, listener.delegateFailureAndWrap((next, result) -> {\n             try {\n+                // Translate the subquery into a separate, coordinator based plan and the results 'broadcasted' as a local relation\n                 completionInfoAccumulator.accumulate(result.completionInfo());\n-                LocalRelation resultWrapper = resultToPlan(tuple.logical, result);\n+                LocalRelation resultWrapper = resultToPlan(subPlans.nonStubbedSubPlan, result);",
        "comment_created_at": "2025-06-25T13:37:18+00:00",
        "comment_author": "bpintea",
        "comment_body": "Not related to this change, but: `resultToPlan` could be made static as well.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2167048244",
    "pr_number": 128917,
    "pr_file": "x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/plan/logical/local/CopyingLocalSupplier.java",
    "created_at": "2025-06-25T15:45:27+00:00",
    "commented_code": "/*\n * Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one\n * or more contributor license agreements. Licensed under the Elastic License\n * 2.0; you may not use this file except in compliance with the Elastic License\n * 2.0.\n */\n\npackage org.elasticsearch.xpack.esql.plan.logical.local;\n\nimport org.elasticsearch.compute.data.Block;\nimport org.elasticsearch.compute.data.BlockUtils;\nimport org.elasticsearch.xpack.esql.planner.PlannerUtils;\n\n/**\n * A {@link LocalSupplier} that allways creates a new copy of the {@link Block}s initially provided at creation time.\n */\npublic class CopyingLocalSupplier extends ImmediateLocalSupplier {\n\n    public CopyingLocalSupplier(Block[] blocks) {\n        super(blocks);\n    }\n\n    @Override\n    public Block[] get() {",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2167048244",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 128917,
        "pr_file": "x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/plan/logical/local/CopyingLocalSupplier.java",
        "discussion_id": "2167048244",
        "commented_code": "@@ -0,0 +1,31 @@\n+/*\n+ * Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one\n+ * or more contributor license agreements. Licensed under the Elastic License\n+ * 2.0; you may not use this file except in compliance with the Elastic License\n+ * 2.0.\n+ */\n+\n+package org.elasticsearch.xpack.esql.plan.logical.local;\n+\n+import org.elasticsearch.compute.data.Block;\n+import org.elasticsearch.compute.data.BlockUtils;\n+import org.elasticsearch.xpack.esql.planner.PlannerUtils;\n+\n+/**\n+ * A {@link LocalSupplier} that allways creates a new copy of the {@link Block}s initially provided at creation time.\n+ */\n+public class CopyingLocalSupplier extends ImmediateLocalSupplier {\n+\n+    public CopyingLocalSupplier(Block[] blocks) {\n+        super(blocks);\n+    }\n+\n+    @Override\n+    public Block[] get() {",
        "comment_created_at": "2025-06-25T15:45:27+00:00",
        "comment_author": "bpintea",
        "comment_body": "Should this method be made a util in `BlockUtils`? There's a few possible uses of one, as called by `BlockUtils#deepCopyOf`. Then you could use a plain lambda supplier directly in `ReplaceRowAsLocalRelation` when building the `LocalRelation` (and wouldn't need this extra supplier).",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2169174964",
    "pr_number": 128917,
    "pr_file": "x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/session/EsqlSession.java",
    "created_at": "2025-06-26T14:11:34+00:00",
    "commented_code": "LogicalPlan optimizedPlan,\n        ActionListener<Result> listener\n    ) {\n        PhysicalPlan physicalPlan = logicalPlanToPhysicalPlan(optimizedPlan, request);\n        if (explainMode) {",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2169174964",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 128917,
        "pr_file": "x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/session/EsqlSession.java",
        "discussion_id": "2169174964",
        "commented_code": "@@ -217,8 +217,8 @@ public void executeOptimizedPlan(\n         LogicalPlan optimizedPlan,\n         ActionListener<Result> listener\n     ) {\n-        PhysicalPlan physicalPlan = logicalPlanToPhysicalPlan(optimizedPlan, request);\n         if (explainMode) {",
        "comment_created_at": "2025-06-26T14:11:34+00:00",
        "comment_author": "bpintea",
        "comment_body": "Nit: would it be worth extracting this case into an own method?",
        "pr_file_module": null
      },
      {
        "comment_id": "2172308567",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 128917,
        "pr_file": "x-pack/plugin/esql/src/main/java/org/elasticsearch/xpack/esql/session/EsqlSession.java",
        "discussion_id": "2169174964",
        "commented_code": "@@ -217,8 +217,8 @@ public void executeOptimizedPlan(\n         LogicalPlan optimizedPlan,\n         ActionListener<Result> listener\n     ) {\n-        PhysicalPlan physicalPlan = logicalPlanToPhysicalPlan(optimizedPlan, request);\n         if (explainMode) {",
        "comment_created_at": "2025-06-27T15:41:11+00:00",
        "comment_author": "astefan",
        "comment_body": "I've added a TODO to revisit this. `explain` in EsqlSession needs a second look, some things do not feel like they belong here.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2180043409",
    "pr_number": 129902,
    "pr_file": "server/src/main/java/org/elasticsearch/action/termvectors/TransportEnsureDocsSearchableAction.java",
    "created_at": "2025-07-02T13:17:00+00:00",
    "commented_code": "/*\n * Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one\n * or more contributor license agreements. Licensed under the \"Elastic License\n * 2.0\", the \"GNU Affero General Public License v3.0 only\", and the \"Server Side\n * Public License v 1\"; you may not use this file except in compliance with, at\n * your election, the \"Elastic License 2.0\", the \"GNU Affero General Public\n * License v3.0 only\", or the \"Server Side Public License, v 1\".\n *\n * This file was contributed to by generative AI\n */\n\npackage org.elasticsearch.action.termvectors;\n\nimport org.apache.logging.log4j.LogManager;\nimport org.apache.logging.log4j.Logger;\nimport org.elasticsearch.ElasticsearchException;\nimport org.elasticsearch.action.ActionListener;\nimport org.elasticsearch.action.ActionRequestValidationException;\nimport org.elasticsearch.action.ActionResponse;\nimport org.elasticsearch.action.ActionType;\nimport org.elasticsearch.action.NoShardAvailableActionException;\nimport org.elasticsearch.action.admin.indices.refresh.TransportShardRefreshAction;\nimport org.elasticsearch.action.support.ActionFilters;\nimport org.elasticsearch.action.support.ActiveShardCount;\nimport org.elasticsearch.action.support.replication.BasicReplicationRequest;\nimport org.elasticsearch.action.support.single.shard.SingleShardRequest;\nimport org.elasticsearch.action.support.single.shard.TransportSingleShardAction;\nimport org.elasticsearch.client.internal.node.NodeClient;\nimport org.elasticsearch.cluster.ProjectState;\nimport org.elasticsearch.cluster.metadata.IndexNameExpressionResolver;\nimport org.elasticsearch.cluster.node.DiscoveryNode;\nimport org.elasticsearch.cluster.node.DiscoveryNodeRole;\nimport org.elasticsearch.cluster.project.ProjectResolver;\nimport org.elasticsearch.cluster.routing.ShardIterator;\nimport org.elasticsearch.cluster.service.ClusterService;\nimport org.elasticsearch.common.io.stream.StreamInput;\nimport org.elasticsearch.common.io.stream.StreamOutput;\nimport org.elasticsearch.common.io.stream.Writeable;\nimport org.elasticsearch.index.IndexService;\nimport org.elasticsearch.index.mapper.Uid;\nimport org.elasticsearch.index.shard.IndexShard;\nimport org.elasticsearch.index.shard.ShardId;\nimport org.elasticsearch.indices.IndicesService;\nimport org.elasticsearch.injection.guice.Inject;\nimport org.elasticsearch.threadpool.ThreadPool;\nimport org.elasticsearch.transport.TransportService;\n\nimport java.io.IOException;\nimport java.util.List;\n\n/**\n * This action is used in serverless to ensure that documents are searchable on the search tier before processing\n * term vector requests. It is an intermediate action that is executed on the indexing node and responds\n * with a no-op (the search node can proceed to process the term vector request). The action may trigger an external refresh\n * to ensure the search shards are up to date before returning the no-op.\n */\npublic class TransportEnsureDocsSearchableAction extends TransportSingleShardAction<",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2180043409",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129902,
        "pr_file": "server/src/main/java/org/elasticsearch/action/termvectors/TransportEnsureDocsSearchableAction.java",
        "discussion_id": "2180043409",
        "commented_code": "@@ -0,0 +1,224 @@\n+/*\n+ * Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one\n+ * or more contributor license agreements. Licensed under the \"Elastic License\n+ * 2.0\", the \"GNU Affero General Public License v3.0 only\", and the \"Server Side\n+ * Public License v 1\"; you may not use this file except in compliance with, at\n+ * your election, the \"Elastic License 2.0\", the \"GNU Affero General Public\n+ * License v3.0 only\", or the \"Server Side Public License, v 1\".\n+ *\n+ * This file was contributed to by generative AI\n+ */\n+\n+package org.elasticsearch.action.termvectors;\n+\n+import org.apache.logging.log4j.LogManager;\n+import org.apache.logging.log4j.Logger;\n+import org.elasticsearch.ElasticsearchException;\n+import org.elasticsearch.action.ActionListener;\n+import org.elasticsearch.action.ActionRequestValidationException;\n+import org.elasticsearch.action.ActionResponse;\n+import org.elasticsearch.action.ActionType;\n+import org.elasticsearch.action.NoShardAvailableActionException;\n+import org.elasticsearch.action.admin.indices.refresh.TransportShardRefreshAction;\n+import org.elasticsearch.action.support.ActionFilters;\n+import org.elasticsearch.action.support.ActiveShardCount;\n+import org.elasticsearch.action.support.replication.BasicReplicationRequest;\n+import org.elasticsearch.action.support.single.shard.SingleShardRequest;\n+import org.elasticsearch.action.support.single.shard.TransportSingleShardAction;\n+import org.elasticsearch.client.internal.node.NodeClient;\n+import org.elasticsearch.cluster.ProjectState;\n+import org.elasticsearch.cluster.metadata.IndexNameExpressionResolver;\n+import org.elasticsearch.cluster.node.DiscoveryNode;\n+import org.elasticsearch.cluster.node.DiscoveryNodeRole;\n+import org.elasticsearch.cluster.project.ProjectResolver;\n+import org.elasticsearch.cluster.routing.ShardIterator;\n+import org.elasticsearch.cluster.service.ClusterService;\n+import org.elasticsearch.common.io.stream.StreamInput;\n+import org.elasticsearch.common.io.stream.StreamOutput;\n+import org.elasticsearch.common.io.stream.Writeable;\n+import org.elasticsearch.index.IndexService;\n+import org.elasticsearch.index.mapper.Uid;\n+import org.elasticsearch.index.shard.IndexShard;\n+import org.elasticsearch.index.shard.ShardId;\n+import org.elasticsearch.indices.IndicesService;\n+import org.elasticsearch.injection.guice.Inject;\n+import org.elasticsearch.threadpool.ThreadPool;\n+import org.elasticsearch.transport.TransportService;\n+\n+import java.io.IOException;\n+import java.util.List;\n+\n+/**\n+ * This action is used in serverless to ensure that documents are searchable on the search tier before processing\n+ * term vector requests. It is an intermediate action that is executed on the indexing node and responds\n+ * with a no-op (the search node can proceed to process the term vector request). The action may trigger an external refresh\n+ * to ensure the search shards are up to date before returning the no-op.\n+ */\n+public class TransportEnsureDocsSearchableAction extends TransportSingleShardAction<",
        "comment_created_at": "2025-07-02T13:17:00+00:00",
        "comment_author": "tlrx",
        "comment_body": "Could we have only the ActionType and the request in `server`, and the rest lies into the serverless code base? Similarly to StatelessPrimaryRelocationAction?",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2177395073",
    "pr_number": 130364,
    "pr_file": "x-pack/plugin/deprecation/src/main/java/org/elasticsearch/xpack/deprecation/ClusterDeprecationChecker.java",
    "created_at": "2025-07-01T11:51:17+00:00",
    "commented_code": "import org.apache.logging.log4j.LogManager;\nimport org.apache.logging.log4j.Logger;\nimport org.elasticsearch.cluster.ClusterState;\nimport org.elasticsearch.common.TriConsumer;\nimport org.elasticsearch.xcontent.NamedXContentRegistry;\nimport org.elasticsearch.xpack.core.deprecation.DeprecationIssue;\nimport org.elasticsearch.xpack.core.transform.transforms.TransformConfig;\n\nimport java.io.IOException;\nimport java.util.ArrayList;\nimport java.util.List;\nimport java.util.function.BiConsumer;\n\n/**\n * Cluster-specific deprecation checks, this is used to populate the {@code cluster_settings} field\n */\npublic class ClusterDeprecationChecker {\n\n    private static final Logger logger = LogManager.getLogger(ClusterDeprecationChecker.class);\n    private final List<TriConsumer<ClusterState, List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(\n        this::checkTransformSettings\n    );\n    private final List<BiConsumer<List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(this::checkTransformSettings);\n    private final NamedXContentRegistry xContentRegistry;\n\n    ClusterDeprecationChecker(NamedXContentRegistry xContentRegistry) {\n        this.xContentRegistry = xContentRegistry;\n    }\n\n    public List<DeprecationIssue> check(ClusterState clusterState, List<TransformConfig> transformConfigs) {\n    public List<DeprecationIssue> check(List<TransformConfig> transformConfigs) {\n        List<DeprecationIssue> allIssues = new ArrayList<>();\n        CHECKS.forEach(check -> check.apply(clusterState, transformConfigs, allIssues));\n        CHECKS.forEach(check -> check.accept(transformConfigs, allIssues));",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2177395073",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130364,
        "pr_file": "x-pack/plugin/deprecation/src/main/java/org/elasticsearch/xpack/deprecation/ClusterDeprecationChecker.java",
        "discussion_id": "2177395073",
        "commented_code": "@@ -9,42 +9,35 @@\n \n import org.apache.logging.log4j.LogManager;\n import org.apache.logging.log4j.Logger;\n-import org.elasticsearch.cluster.ClusterState;\n-import org.elasticsearch.common.TriConsumer;\n import org.elasticsearch.xcontent.NamedXContentRegistry;\n import org.elasticsearch.xpack.core.deprecation.DeprecationIssue;\n import org.elasticsearch.xpack.core.transform.transforms.TransformConfig;\n \n import java.io.IOException;\n import java.util.ArrayList;\n import java.util.List;\n+import java.util.function.BiConsumer;\n \n /**\n  * Cluster-specific deprecation checks, this is used to populate the {@code cluster_settings} field\n  */\n public class ClusterDeprecationChecker {\n \n     private static final Logger logger = LogManager.getLogger(ClusterDeprecationChecker.class);\n-    private final List<TriConsumer<ClusterState, List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(\n-        this::checkTransformSettings\n-    );\n+    private final List<BiConsumer<List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(this::checkTransformSettings);\n     private final NamedXContentRegistry xContentRegistry;\n \n     ClusterDeprecationChecker(NamedXContentRegistry xContentRegistry) {\n         this.xContentRegistry = xContentRegistry;\n     }\n \n-    public List<DeprecationIssue> check(ClusterState clusterState, List<TransformConfig> transformConfigs) {\n+    public List<DeprecationIssue> check(List<TransformConfig> transformConfigs) {\n         List<DeprecationIssue> allIssues = new ArrayList<>();\n-        CHECKS.forEach(check -> check.apply(clusterState, transformConfigs, allIssues));\n+        CHECKS.forEach(check -> check.accept(transformConfigs, allIssues));",
        "comment_created_at": "2025-07-01T11:51:17+00:00",
        "comment_author": "PeteGillinElastic",
        "comment_body": "Do we feel like the `CHECKS` abstraction is still pulling its weight here? There's one check hard-coded, we could just call `checkTransformSettings` directly, and it'd be more readable. If we needed to add more checks in the future, it's not clear to me that adding a method to the list would be better than adding another method call here. Plus, it's not clear to me that the `BiConsumer` would have the correct signature for a theoretical future check, either. (Presumably, at some point in the past there was a check which consumed `ClusterState`, hence the redundant parameter. A future check might need that, or might need the `ProjectMetadata`, but we can't really guess. now.)",
        "pr_file_module": null
      },
      {
        "comment_id": "2177503438",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130364,
        "pr_file": "x-pack/plugin/deprecation/src/main/java/org/elasticsearch/xpack/deprecation/ClusterDeprecationChecker.java",
        "discussion_id": "2177395073",
        "commented_code": "@@ -9,42 +9,35 @@\n \n import org.apache.logging.log4j.LogManager;\n import org.apache.logging.log4j.Logger;\n-import org.elasticsearch.cluster.ClusterState;\n-import org.elasticsearch.common.TriConsumer;\n import org.elasticsearch.xcontent.NamedXContentRegistry;\n import org.elasticsearch.xpack.core.deprecation.DeprecationIssue;\n import org.elasticsearch.xpack.core.transform.transforms.TransformConfig;\n \n import java.io.IOException;\n import java.util.ArrayList;\n import java.util.List;\n+import java.util.function.BiConsumer;\n \n /**\n  * Cluster-specific deprecation checks, this is used to populate the {@code cluster_settings} field\n  */\n public class ClusterDeprecationChecker {\n \n     private static final Logger logger = LogManager.getLogger(ClusterDeprecationChecker.class);\n-    private final List<TriConsumer<ClusterState, List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(\n-        this::checkTransformSettings\n-    );\n+    private final List<BiConsumer<List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(this::checkTransformSettings);\n     private final NamedXContentRegistry xContentRegistry;\n \n     ClusterDeprecationChecker(NamedXContentRegistry xContentRegistry) {\n         this.xContentRegistry = xContentRegistry;\n     }\n \n-    public List<DeprecationIssue> check(ClusterState clusterState, List<TransformConfig> transformConfigs) {\n+    public List<DeprecationIssue> check(List<TransformConfig> transformConfigs) {\n         List<DeprecationIssue> allIssues = new ArrayList<>();\n-        CHECKS.forEach(check -> check.apply(clusterState, transformConfigs, allIssues));\n+        CHECKS.forEach(check -> check.accept(transformConfigs, allIssues));",
        "comment_created_at": "2025-07-01T12:39:04+00:00",
        "comment_author": "nielsbauman",
        "comment_body": "I hear what you're saying. My intuition was that this `CHECKS` field makes this class more consistent with the other deprecation checkers. But I don't have strong feelings, so I'm fine with calling that method directly.",
        "pr_file_module": null
      },
      {
        "comment_id": "2177510862",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130364,
        "pr_file": "x-pack/plugin/deprecation/src/main/java/org/elasticsearch/xpack/deprecation/ClusterDeprecationChecker.java",
        "discussion_id": "2177395073",
        "commented_code": "@@ -9,42 +9,35 @@\n \n import org.apache.logging.log4j.LogManager;\n import org.apache.logging.log4j.Logger;\n-import org.elasticsearch.cluster.ClusterState;\n-import org.elasticsearch.common.TriConsumer;\n import org.elasticsearch.xcontent.NamedXContentRegistry;\n import org.elasticsearch.xpack.core.deprecation.DeprecationIssue;\n import org.elasticsearch.xpack.core.transform.transforms.TransformConfig;\n \n import java.io.IOException;\n import java.util.ArrayList;\n import java.util.List;\n+import java.util.function.BiConsumer;\n \n /**\n  * Cluster-specific deprecation checks, this is used to populate the {@code cluster_settings} field\n  */\n public class ClusterDeprecationChecker {\n \n     private static final Logger logger = LogManager.getLogger(ClusterDeprecationChecker.class);\n-    private final List<TriConsumer<ClusterState, List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(\n-        this::checkTransformSettings\n-    );\n+    private final List<BiConsumer<List<TransformConfig>, List<DeprecationIssue>>> CHECKS = List.of(this::checkTransformSettings);\n     private final NamedXContentRegistry xContentRegistry;\n \n     ClusterDeprecationChecker(NamedXContentRegistry xContentRegistry) {\n         this.xContentRegistry = xContentRegistry;\n     }\n \n-    public List<DeprecationIssue> check(ClusterState clusterState, List<TransformConfig> transformConfigs) {\n+    public List<DeprecationIssue> check(List<TransformConfig> transformConfigs) {\n         List<DeprecationIssue> allIssues = new ArrayList<>();\n-        CHECKS.forEach(check -> check.apply(clusterState, transformConfigs, allIssues));\n+        CHECKS.forEach(check -> check.accept(transformConfigs, allIssues));",
        "comment_created_at": "2025-07-01T12:42:49+00:00",
        "comment_author": "nielsbauman",
        "comment_body": "On second thought, I think I agree with you that the `CHECKS` abstraction isn't super valuable, and that goes for the other classes too. I don't think it's worth opening a PR for those other classes, but perhaps I'll remember it if I ever need to touch this code again.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2179784624",
    "pr_number": 130131,
    "pr_file": "plugins/discovery-ec2/src/test/java/org/elasticsearch/discovery/ec2/EC2RetriesTests.java",
    "created_at": "2025-07-02T11:12:54+00:00",
    "commented_code": "new NoneCircuitBreakerService(),\n                new SharedGroupFactory(Settings.EMPTY)\n            ),\n            threadPool,\n            TransportService.NOOP_TRANSPORT_INTERCEPTOR,",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2179784624",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130131,
        "pr_file": "plugins/discovery-ec2/src/test/java/org/elasticsearch/discovery/ec2/EC2RetriesTests.java",
        "discussion_id": "2179784624",
        "commented_code": "@@ -59,9 +59,7 @@ protected MockTransportService createTransportService() {\n                 new NoneCircuitBreakerService(),\n                 new SharedGroupFactory(Settings.EMPTY)\n             ),\n-            threadPool,\n-            TransportService.NOOP_TRANSPORT_INTERCEPTOR,",
        "comment_created_at": "2025-07-02T11:12:54+00:00",
        "comment_author": "GalLalouche",
        "comment_body": "It seemed all clients passed the same `Settings.EMPTY`, interceptor, and `null` in the `clusterSettings` to this constructor (refactored to a factory method), so I've simplified the method by removing those parameters.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2156561649",
    "pr_number": 129633,
    "pr_file": "x-pack/plugin/esql/compute/gen/src/main/java/org/elasticsearch/compute/gen/GroupingAggregatorImplementer.java",
    "created_at": "2025-06-19T09:26:33+00:00",
    "commented_code": "}\n        builder.beginControlFlow(\"for (int groupPosition = 0; groupPosition < groups.getPositionCount(); groupPosition++)\");\n        {",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2156561649",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129633,
        "pr_file": "x-pack/plugin/esql/compute/gen/src/main/java/org/elasticsearch/compute/gen/GroupingAggregatorImplementer.java",
        "discussion_id": "2156561649",
        "commented_code": "@@ -610,7 +611,18 @@ private MethodSpec addIntermediateInput() {\n         }\n         builder.beginControlFlow(\"for (int groupPosition = 0; groupPosition < groups.getPositionCount(); groupPosition++)\");\n         {",
        "comment_created_at": "2025-06-19T09:26:33+00:00",
        "comment_author": "Copilot",
        "comment_body": "[nitpick] The addIntermediateInput method contains duplicated logic for handling block types versus non-block types; consider refactoring to extract the common behavior and reduce code duplication.\n```suggestion\n        {\n            String groupIdAssignment;\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2163237789",
    "pr_number": 129684,
    "pr_file": "server/src/main/java/org/elasticsearch/index/codec/vectors/es818/ES818BinaryQuantizedVectorsFormat.java",
    "created_at": "2025-06-24T08:03:09+00:00",
    "commented_code": "*  <li>The sparse vector information, if required, mapping vector ordinal to doc ID\n  * </ul>\n */\n@SuppressForbidden(",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2163237789",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129684,
        "pr_file": "server/src/main/java/org/elasticsearch/index/codec/vectors/es818/ES818BinaryQuantizedVectorsFormat.java",
        "discussion_id": "2163237789",
        "commented_code": "@@ -85,8 +86,10 @@\n   *  <li>The sparse vector information, if required, mapping vector ordinal to doc ID\n   * </ul>\n  */\n+@SuppressForbidden(",
        "comment_created_at": "2025-06-24T08:03:09+00:00",
        "comment_author": "mosche",
        "comment_body": "could you extract a little helper and suppress there, so we don't accidentally suppress more than intended",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2163241519",
    "pr_number": 129684,
    "pr_file": "server/src/main/java/org/elasticsearch/search/SearchService.java",
    "created_at": "2025-06-24T08:05:06+00:00",
    "commented_code": "* @param threadPool     with context where to write the new header\n     * @return the wrapped action listener\n     */\n    @SuppressForbidden(\n        reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n    )",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2163241519",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129684,
        "pr_file": "server/src/main/java/org/elasticsearch/search/SearchService.java",
        "discussion_id": "2163241519",
        "commented_code": "@@ -589,6 +590,9 @@ protected void doClose() {\n      * @param threadPool     with context where to write the new header\n      * @return the wrapped action listener\n      */\n+    @SuppressForbidden(\n+        reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n+    )",
        "comment_created_at": "2025-06-24T08:05:06+00:00",
        "comment_author": "mosche",
        "comment_body": "could you extract a little helper and suppress there, so we don't accidentally suppress more than intended",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2163296345",
    "pr_number": 129684,
    "pr_file": "modules/transport-netty4/src/main/java/org/elasticsearch/transport/netty4/NettyAllocator.java",
    "created_at": "2025-06-24T08:29:59+00:00",
    "commented_code": "import org.elasticsearch.common.util.PageCacheRecycler;\nimport org.elasticsearch.core.Assertions;\nimport org.elasticsearch.core.Booleans;\nimport org.elasticsearch.core.SuppressForbidden;\nimport org.elasticsearch.monitor.jvm.JvmInfo;\n\nimport java.util.Arrays;\nimport java.util.concurrent.atomic.AtomicBoolean;\n\n@SuppressForbidden(\n    reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n)",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2163296345",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129684,
        "pr_file": "modules/transport-netty4/src/main/java/org/elasticsearch/transport/netty4/NettyAllocator.java",
        "discussion_id": "2163296345",
        "commented_code": "@@ -26,11 +26,15 @@\n import org.elasticsearch.common.util.PageCacheRecycler;\n import org.elasticsearch.core.Assertions;\n import org.elasticsearch.core.Booleans;\n+import org.elasticsearch.core.SuppressForbidden;\n import org.elasticsearch.monitor.jvm.JvmInfo;\n \n import java.util.Arrays;\n import java.util.concurrent.atomic.AtomicBoolean;\n \n+@SuppressForbidden(\n+    reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n+)",
        "comment_created_at": "2025-06-24T08:29:59+00:00",
        "comment_author": "mosche",
        "comment_body": "could you extract a little helper and suppress there, so we don't accidentally suppress more than intended",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2163301148",
    "pr_number": 129684,
    "pr_file": "server/src/main/java/org/elasticsearch/common/network/NetworkUtils.java",
    "created_at": "2025-06-24T08:31:25+00:00",
    "commented_code": "* Utilities for network interfaces / addresses binding and publishing.\n * Its only intended for that purpose, not general purpose usage!!!!\n */\n@SuppressForbidden(\n    reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n)",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2163301148",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129684,
        "pr_file": "server/src/main/java/org/elasticsearch/common/network/NetworkUtils.java",
        "discussion_id": "2163301148",
        "commented_code": "@@ -32,6 +33,9 @@\n  * Utilities for network interfaces / addresses binding and publishing.\n  * Its only intended for that purpose, not general purpose usage!!!!\n  */\n+@SuppressForbidden(\n+    reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n+)",
        "comment_created_at": "2025-06-24T08:31:25+00:00",
        "comment_author": "mosche",
        "comment_body": "could you extract a little helper and suppress there, so we don't accidentally suppress more than intended",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2163302186",
    "pr_number": 129684,
    "pr_file": "server/src/main/java/org/elasticsearch/index/codec/tsdb/es819/ES819TSDBDocValuesFormat.java",
    "created_at": "2025-06-24T08:31:54+00:00",
    "commented_code": "*     cpu resources.</li>\n * </ul>\n */\n@SuppressForbidden(\n    reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n)",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2163302186",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129684,
        "pr_file": "server/src/main/java/org/elasticsearch/index/codec/tsdb/es819/ES819TSDBDocValuesFormat.java",
        "discussion_id": "2163302186",
        "commented_code": "@@ -28,6 +29,9 @@\n  *     cpu resources.</li>\n  * </ul>\n  */\n+@SuppressForbidden(\n+    reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n+)",
        "comment_created_at": "2025-06-24T08:31:54+00:00",
        "comment_author": "mosche",
        "comment_body": "could you extract a little helper and suppress there, so we don't accidentally suppress more than intended",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2171122552",
    "pr_number": 129684,
    "pr_file": "modules/lang-painless/src/main/java/org/elasticsearch/painless/PainlessScriptEngine.java",
    "created_at": "2025-06-27T08:00:12+00:00",
    "commented_code": "}\n    }\n\n    @SuppressForbidden(\n        reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n    )",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2171122552",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129684,
        "pr_file": "modules/lang-painless/src/main/java/org/elasticsearch/painless/PainlessScriptEngine.java",
        "discussion_id": "2171122552",
        "commented_code": "@@ -391,6 +392,9 @@ ScriptScope compile(Compiler compiler, Loader loader, String scriptName, String\n         }\n     }\n \n+    @SuppressForbidden(\n+        reason = \"TODO Deprecate any lenient usage of Boolean#parseBoolean https://github.com/elastic/elasticsearch/issues/128993\"\n+    )",
        "comment_created_at": "2025-06-27T08:00:12+00:00",
        "comment_author": "mosche",
        "comment_body": "please also extract a small helper here to minimize the scope of @SuppressForbidden",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2171175467",
    "pr_number": 129684,
    "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/ml/inference/trainedmodel/PredictionFieldType.java",
    "created_at": "2025-06-27T08:17:14+00:00",
    "commented_code": "return name().toLowerCase(Locale.ROOT);\n    }\n\n    @SuppressForbidden(reason = \"accept lenient boolean field values\")",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2171175467",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 129684,
        "pr_file": "x-pack/plugin/core/src/main/java/org/elasticsearch/xpack/core/ml/inference/trainedmodel/PredictionFieldType.java",
        "discussion_id": "2171175467",
        "commented_code": "@@ -45,6 +46,7 @@ public String toString() {\n         return name().toLowerCase(Locale.ROOT);\n     }\n \n+    @SuppressForbidden(reason = \"accept lenient boolean field values\")",
        "comment_created_at": "2025-06-27T08:17:14+00:00",
        "comment_author": "mosche",
        "comment_body": "please also extract a small helper here to minimize the scope of @SuppressForbidden",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1646778366",
    "pr_number": 109949,
    "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
    "created_at": "2024-06-20T00:22:25+00:00",
    "commented_code": "request.getAutoGeneratedTimestamp(),\n                request.isRetry()\n            );\n\n            if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n                return handleMappingUpdateRequired(\n                    context,\n                    mappingUpdater,\n                    waitForMappingUpdate,\n                    itemDoneListener,\n                    result,\n                    primary,\n                    version,\n                    updateResult\n                );\n            }\n        }\n        if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n\n            try {\n                Optional<CompressedXContent> mergedSource = Optional.ofNullable(\n                    primary.mapperService()\n                        .merge(\n                            MapperService.SINGLE_MAPPING_NAME,\n                            new CompressedXContent(result.getRequiredMappingUpdate()),\n                            MapperService.MergeReason.MAPPING_AUTO_UPDATE_PREFLIGHT\n                        )\n                ).map(DocumentMapper::mappingSource);\n                Optional<CompressedXContent> previousSource = Optional.ofNullable(primary.mapperService().documentMapper())\n                    .map(DocumentMapper::mappingSource);\n        onComplete(result, context, updateResult);\n        return true;\n    }\n\n                if (mergedSource.equals(previousSource)) {\n                    context.resetForNoopMappingUpdateRetry(primary.mapperService().mappingVersion());\n                    return true;\n                }\n            } catch (Exception e) {\n                logger.info(() -> format(\"%s mapping update rejected by primary\", primary.shardId()), e);\n                assert result.getId() != null;\n                onComplete(exceptionToResult(e, primary, isDelete, version, result.getId()), context, updateResult);\n    private static boolean handleMappingUpdateRequired(",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1646778366",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1646778366",
        "commented_code": "@@ -379,64 +376,88 @@ static boolean executeBulkItemRequest(\n                 request.getAutoGeneratedTimestamp(),\n                 request.isRetry()\n             );\n-\n+            if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n+                return handleMappingUpdateRequired(\n+                    context,\n+                    mappingUpdater,\n+                    waitForMappingUpdate,\n+                    itemDoneListener,\n+                    result,\n+                    primary,\n+                    version,\n+                    updateResult\n+                );\n+            }\n         }\n-        if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n \n-            try {\n-                Optional<CompressedXContent> mergedSource = Optional.ofNullable(\n-                    primary.mapperService()\n-                        .merge(\n-                            MapperService.SINGLE_MAPPING_NAME,\n-                            new CompressedXContent(result.getRequiredMappingUpdate()),\n-                            MapperService.MergeReason.MAPPING_AUTO_UPDATE_PREFLIGHT\n-                        )\n-                ).map(DocumentMapper::mappingSource);\n-                Optional<CompressedXContent> previousSource = Optional.ofNullable(primary.mapperService().documentMapper())\n-                    .map(DocumentMapper::mappingSource);\n+        onComplete(result, context, updateResult);\n+        return true;\n+    }\n \n-                if (mergedSource.equals(previousSource)) {\n-                    context.resetForNoopMappingUpdateRetry(primary.mapperService().mappingVersion());\n-                    return true;\n-                }\n-            } catch (Exception e) {\n-                logger.info(() -> format(\"%s mapping update rejected by primary\", primary.shardId()), e);\n-                assert result.getId() != null;\n-                onComplete(exceptionToResult(e, primary, isDelete, version, result.getId()), context, updateResult);\n+    private static boolean handleMappingUpdateRequired(",
        "comment_created_at": "2024-06-20T00:22:25+00:00",
        "comment_author": "original-brownbear",
        "comment_body": "Just extracted this into its own method now that it got so big and removed the `Optional` use which was confusing and unnecessary. Sorry for mixing fix + refactoring a little here, hope it's not too confusing. Otherwise I can make this into a 2 parter.",
        "pr_file_module": null
      },
      {
        "comment_id": "1647324269",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1646778366",
        "commented_code": "@@ -379,64 +376,88 @@ static boolean executeBulkItemRequest(\n                 request.getAutoGeneratedTimestamp(),\n                 request.isRetry()\n             );\n-\n+            if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n+                return handleMappingUpdateRequired(\n+                    context,\n+                    mappingUpdater,\n+                    waitForMappingUpdate,\n+                    itemDoneListener,\n+                    result,\n+                    primary,\n+                    version,\n+                    updateResult\n+                );\n+            }\n         }\n-        if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n \n-            try {\n-                Optional<CompressedXContent> mergedSource = Optional.ofNullable(\n-                    primary.mapperService()\n-                        .merge(\n-                            MapperService.SINGLE_MAPPING_NAME,\n-                            new CompressedXContent(result.getRequiredMappingUpdate()),\n-                            MapperService.MergeReason.MAPPING_AUTO_UPDATE_PREFLIGHT\n-                        )\n-                ).map(DocumentMapper::mappingSource);\n-                Optional<CompressedXContent> previousSource = Optional.ofNullable(primary.mapperService().documentMapper())\n-                    .map(DocumentMapper::mappingSource);\n+        onComplete(result, context, updateResult);\n+        return true;\n+    }\n \n-                if (mergedSource.equals(previousSource)) {\n-                    context.resetForNoopMappingUpdateRetry(primary.mapperService().mappingVersion());\n-                    return true;\n-                }\n-            } catch (Exception e) {\n-                logger.info(() -> format(\"%s mapping update rejected by primary\", primary.shardId()), e);\n-                assert result.getId() != null;\n-                onComplete(exceptionToResult(e, primary, isDelete, version, result.getId()), context, updateResult);\n+    private static boolean handleMappingUpdateRequired(",
        "comment_created_at": "2024-06-20T10:02:50+00:00",
        "comment_author": "javanna",
        "comment_body": "given how delicate things are, I think it would be great to split this in two: refactoring  + actual change, as a safety measure. I could definitely miss things otherwise while reviewing this as-is.",
        "pr_file_module": null
      },
      {
        "comment_id": "1647381507",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1646778366",
        "commented_code": "@@ -379,64 +376,88 @@ static boolean executeBulkItemRequest(\n                 request.getAutoGeneratedTimestamp(),\n                 request.isRetry()\n             );\n-\n+            if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n+                return handleMappingUpdateRequired(\n+                    context,\n+                    mappingUpdater,\n+                    waitForMappingUpdate,\n+                    itemDoneListener,\n+                    result,\n+                    primary,\n+                    version,\n+                    updateResult\n+                );\n+            }\n         }\n-        if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n \n-            try {\n-                Optional<CompressedXContent> mergedSource = Optional.ofNullable(\n-                    primary.mapperService()\n-                        .merge(\n-                            MapperService.SINGLE_MAPPING_NAME,\n-                            new CompressedXContent(result.getRequiredMappingUpdate()),\n-                            MapperService.MergeReason.MAPPING_AUTO_UPDATE_PREFLIGHT\n-                        )\n-                ).map(DocumentMapper::mappingSource);\n-                Optional<CompressedXContent> previousSource = Optional.ofNullable(primary.mapperService().documentMapper())\n-                    .map(DocumentMapper::mappingSource);\n+        onComplete(result, context, updateResult);\n+        return true;\n+    }\n \n-                if (mergedSource.equals(previousSource)) {\n-                    context.resetForNoopMappingUpdateRetry(primary.mapperService().mappingVersion());\n-                    return true;\n-                }\n-            } catch (Exception e) {\n-                logger.info(() -> format(\"%s mapping update rejected by primary\", primary.shardId()), e);\n-                assert result.getId() != null;\n-                onComplete(exceptionToResult(e, primary, isDelete, version, result.getId()), context, updateResult);\n+    private static boolean handleMappingUpdateRequired(",
        "comment_created_at": "2024-06-20T10:49:43+00:00",
        "comment_author": "original-brownbear",
        "comment_body": "Agreed :) Here you go https://github.com/elastic/elasticsearch/pull/109961 :)",
        "pr_file_module": null
      },
      {
        "comment_id": "1648632335",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 109949,
        "pr_file": "server/src/main/java/org/elasticsearch/action/bulk/TransportShardBulkAction.java",
        "discussion_id": "1646778366",
        "commented_code": "@@ -379,64 +376,88 @@ static boolean executeBulkItemRequest(\n                 request.getAutoGeneratedTimestamp(),\n                 request.isRetry()\n             );\n-\n+            if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n+                return handleMappingUpdateRequired(\n+                    context,\n+                    mappingUpdater,\n+                    waitForMappingUpdate,\n+                    itemDoneListener,\n+                    result,\n+                    primary,\n+                    version,\n+                    updateResult\n+                );\n+            }\n         }\n-        if (result.getResultType() == Engine.Result.Type.MAPPING_UPDATE_REQUIRED) {\n \n-            try {\n-                Optional<CompressedXContent> mergedSource = Optional.ofNullable(\n-                    primary.mapperService()\n-                        .merge(\n-                            MapperService.SINGLE_MAPPING_NAME,\n-                            new CompressedXContent(result.getRequiredMappingUpdate()),\n-                            MapperService.MergeReason.MAPPING_AUTO_UPDATE_PREFLIGHT\n-                        )\n-                ).map(DocumentMapper::mappingSource);\n-                Optional<CompressedXContent> previousSource = Optional.ofNullable(primary.mapperService().documentMapper())\n-                    .map(DocumentMapper::mappingSource);\n+        onComplete(result, context, updateResult);\n+        return true;\n+    }\n \n-                if (mergedSource.equals(previousSource)) {\n-                    context.resetForNoopMappingUpdateRetry(primary.mapperService().mappingVersion());\n-                    return true;\n-                }\n-            } catch (Exception e) {\n-                logger.info(() -> format(\"%s mapping update rejected by primary\", primary.shardId()), e);\n-                assert result.getId() != null;\n-                onComplete(exceptionToResult(e, primary, isDelete, version, result.getId()), context, updateResult);\n+    private static boolean handleMappingUpdateRequired(",
        "comment_created_at": "2024-06-21T08:45:01+00:00",
        "comment_author": "javanna",
        "comment_body": "thanks!",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "908872960",
    "pr_number": 87810,
    "pr_file": "x-pack/plugin/sql/src/main/java/org/elasticsearch/xpack/sql/optimizer/Optimizer.java",
    "created_at": "2022-06-28T19:37:01+00:00",
    "commented_code": "}\n\n    public static class ConvertTypes extends OptimizerExpressionRule<ScalarFunction> {\n\n        public ConvertTypes() {\n            super(TransformDirection.DOWN);\n        }\n\n        @Override\n        public Expression rule(ScalarFunction e) {\n            if (e instanceof BinaryComparison predicate && predicate.right().foldable()) {\n                return convertBinaryComparison(predicate);\n            } else if (e instanceof Range range) {\n                return convertRange(range);\n            } else if (e instanceof In in) {\n                return convertIn(in);\n            }\n            return e;\n        }\n\n        private Expression convertIn(In in) {\n            if (in.list().isEmpty()) {\n                return in;\n            }\n            List<Expression> newRight = new ArrayList<>();\n            List<Expression> additionalConditions = new ArrayList<>();\n            DataType type = in.value().dataType();\n            boolean converted = false;\n            for (Expression exp : in.list()) {\n                if (type == exp.dataType() || exp.foldable() == false || DataTypes.areCompatible(type, exp.dataType())) {\n                    newRight.add(exp);\n                } else {\n                    converted = true;\n                    Object foldedValue = exp.fold();\n                    if (DataTypes.isDateTime(type) && DataTypes.isString(exp.dataType())) {\n                        try {\n                            // try date math first\n                            Tuple<Long, Long> range = DateFieldMapper.DateFieldType.toTimestampRange(\n                                foldedValue,\n                                foldedValue,\n                                true,\n                                true,\n                                ZoneOffset.UTC,\n                                DateUtils.DATE_MATH_PARSER,\n                                DateFieldMapper.Resolution.MILLISECONDS,\n                                () -> System.currentTimeMillis()\n                            );\n                            if (range.v1() < range.v2()) {\n                                /*\n                                treat it as a date range\n                                eg. the following\n                                something IN (<daterange>, <somethingElse1>, <somethingElse2>)\n                                becomes\n                                something BETWEEN <min(daterange)> AND <max(daterange)> OR someting IN (<somethingElse1>, <somethingElse2>)\n                                */\n                                additionalConditions.add(\n                                    new Range(\n                                        in.source(),\n                                        in.value(),\n                                        tryCast(exp, range.v1(), type),\n                                        true,\n                                        tryCast(exp, range.v2(), type),\n                                        true,\n                                        in.zoneId()\n                                    )\n                                );\n                            } else {\n                                newRight.add(tryCast(exp, foldedValue, DataTypes.DATETIME));\n                            }\n                        } catch (ElasticsearchParseException | DateTimeParseException e) {\n                            // the date parsing just failed, use the original expression\n                            newRight.add(exp);\n                        }\n                    } else {\n                        newRight.add(tryCast(exp, foldedValue, type));\n                    }\n                }\n            }\n            if (converted == false) {\n                return in;\n            }\n            if (newRight.size() == 1) {\n                additionalConditions.add(new Equals(in.source(), in.value(), newRight.remove(0)));\n            }\n\n            if (newRight.size() > 0 && additionalConditions.size() > 0) {\n                return new Or(\n                    in.source(),\n                    new In(in.source(), in.value(), newRight, in.zoneId()),\n                    toOrTree(in.source(), additionalConditions)\n                );\n            } else if (newRight.size() > 0) {\n                return new In(in.source(), in.value(), newRight, in.zoneId());\n            } else if (additionalConditions.size() > 0) {\n                return toOrTree(in.source(), additionalConditions);\n            }\n\n            return in;\n        }\n\n        private Expression toOrTree(Source source, List<Expression> items) {\n            if (items.size() == 1) {\n                return items.get(0);\n            }\n            if (items.size() == 2) {\n                return new Or(source, items.get(0), items.get(1));\n            }\n\n            int half = items.size() / 2;\n            return new Or(source, toOrTree(source, items.subList(0, half)), toOrTree(source, items.subList(half, items.size())));\n        }\n\n        private Expression convertBinaryComparison(BinaryComparison predicate) {\n            Object rightValue = predicate.right().fold();\n            if (rightValue == null && predicate instanceof NullEquals) {\n                return new IsNull(predicate.source(), predicate.left());\n            } else if (rightValue != null) {\n                try {\n                    if (DataTypes.isDateTime(predicate.left().dataType()) && DataTypes.isString(predicate.right().dataType())) {",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "908872960",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 87810,
        "pr_file": "x-pack/plugin/sql/src/main/java/org/elasticsearch/xpack/sql/optimizer/Optimizer.java",
        "discussion_id": "908872960",
        "commented_code": "@@ -1266,6 +1284,241 @@ private boolean foldable(Expression e) {\n \n     }\n \n+    public static class ConvertTypes extends OptimizerExpressionRule<ScalarFunction> {\n+\n+        public ConvertTypes() {\n+            super(TransformDirection.DOWN);\n+        }\n+\n+        @Override\n+        public Expression rule(ScalarFunction e) {\n+            if (e instanceof BinaryComparison predicate && predicate.right().foldable()) {\n+                return convertBinaryComparison(predicate);\n+            } else if (e instanceof Range range) {\n+                return convertRange(range);\n+            } else if (e instanceof In in) {\n+                return convertIn(in);\n+            }\n+            return e;\n+        }\n+\n+        private Expression convertIn(In in) {\n+            if (in.list().isEmpty()) {\n+                return in;\n+            }\n+            List<Expression> newRight = new ArrayList<>();\n+            List<Expression> additionalConditions = new ArrayList<>();\n+            DataType type = in.value().dataType();\n+            boolean converted = false;\n+            for (Expression exp : in.list()) {\n+                if (type == exp.dataType() || exp.foldable() == false || DataTypes.areCompatible(type, exp.dataType())) {\n+                    newRight.add(exp);\n+                } else {\n+                    converted = true;\n+                    Object foldedValue = exp.fold();\n+                    if (DataTypes.isDateTime(type) && DataTypes.isString(exp.dataType())) {\n+                        try {\n+                            // try date math first\n+                            Tuple<Long, Long> range = DateFieldMapper.DateFieldType.toTimestampRange(\n+                                foldedValue,\n+                                foldedValue,\n+                                true,\n+                                true,\n+                                ZoneOffset.UTC,\n+                                DateUtils.DATE_MATH_PARSER,\n+                                DateFieldMapper.Resolution.MILLISECONDS,\n+                                () -> System.currentTimeMillis()\n+                            );\n+                            if (range.v1() < range.v2()) {\n+                                /*\n+                                treat it as a date range\n+                                eg. the following\n+                                something IN (<daterange>, <somethingElse1>, <somethingElse2>)\n+                                becomes\n+                                something BETWEEN <min(daterange)> AND <max(daterange)> OR someting IN (<somethingElse1>, <somethingElse2>)\n+                                */\n+                                additionalConditions.add(\n+                                    new Range(\n+                                        in.source(),\n+                                        in.value(),\n+                                        tryCast(exp, range.v1(), type),\n+                                        true,\n+                                        tryCast(exp, range.v2(), type),\n+                                        true,\n+                                        in.zoneId()\n+                                    )\n+                                );\n+                            } else {\n+                                newRight.add(tryCast(exp, foldedValue, DataTypes.DATETIME));\n+                            }\n+                        } catch (ElasticsearchParseException | DateTimeParseException e) {\n+                            // the date parsing just failed, use the original expression\n+                            newRight.add(exp);\n+                        }\n+                    } else {\n+                        newRight.add(tryCast(exp, foldedValue, type));\n+                    }\n+                }\n+            }\n+            if (converted == false) {\n+                return in;\n+            }\n+            if (newRight.size() == 1) {\n+                additionalConditions.add(new Equals(in.source(), in.value(), newRight.remove(0)));\n+            }\n+\n+            if (newRight.size() > 0 && additionalConditions.size() > 0) {\n+                return new Or(\n+                    in.source(),\n+                    new In(in.source(), in.value(), newRight, in.zoneId()),\n+                    toOrTree(in.source(), additionalConditions)\n+                );\n+            } else if (newRight.size() > 0) {\n+                return new In(in.source(), in.value(), newRight, in.zoneId());\n+            } else if (additionalConditions.size() > 0) {\n+                return toOrTree(in.source(), additionalConditions);\n+            }\n+\n+            return in;\n+        }\n+\n+        private Expression toOrTree(Source source, List<Expression> items) {\n+            if (items.size() == 1) {\n+                return items.get(0);\n+            }\n+            if (items.size() == 2) {\n+                return new Or(source, items.get(0), items.get(1));\n+            }\n+\n+            int half = items.size() / 2;\n+            return new Or(source, toOrTree(source, items.subList(0, half)), toOrTree(source, items.subList(half, items.size())));\n+        }\n+\n+        private Expression convertBinaryComparison(BinaryComparison predicate) {\n+            Object rightValue = predicate.right().fold();\n+            if (rightValue == null && predicate instanceof NullEquals) {\n+                return new IsNull(predicate.source(), predicate.left());\n+            } else if (rightValue != null) {\n+                try {\n+                    if (DataTypes.isDateTime(predicate.left().dataType()) && DataTypes.isString(predicate.right().dataType())) {",
        "comment_created_at": "2022-06-28T19:37:01+00:00",
        "comment_author": "bpintea",
        "comment_body": "Might be worth extracting this key check into a function? (some `couldBeTimestampRange(DataType, DataType)`?)",
        "pr_file_module": null
      }
    ]
  }
]
