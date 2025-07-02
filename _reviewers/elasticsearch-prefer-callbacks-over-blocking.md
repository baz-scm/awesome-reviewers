---
title: Prefer callbacks over blocking
description: Always structure concurrent code to use asynchronous callbacks instead
  of blocking operations. Blocking calls like CountDownLatch, Thread.join(), or Future.get()
  can lead to thread starvation, reduced throughput, and complex deadlock scenarios.
repository: elastic/elasticsearch
label: Concurrency
language: Java
comments_count: 6
repository_stars: 73104
---

Always structure concurrent code to use asynchronous callbacks instead of blocking operations. Blocking calls like CountDownLatch, Thread.join(), or Future.get() can lead to thread starvation, reduced throughput, and complex deadlock scenarios.

Replace blocking patterns with callback-based approaches:

```java
// AVOID: Blocking with CountDownLatch
CountDownLatch latch = new CountDownLatch(1);
final AtomicBoolean result = new AtomicBoolean(false);
service.getResource(id, new ActionListener<>() {
    @Override
    public void onResponse(Resource resource) {
        result.set(true);
        latch.countDown();
    }
    @Override
    public void onFailure(Exception e) {
        logger.error("Failed: {}", e.getMessage());
        latch.countDown();
    }
});
latch.await(5, TimeUnit.SECONDS); // BLOCKS thread!
return result.get();

// PREFER: Fully asynchronous with listeners
void getResourceAsync(String id, ActionListener<Boolean> listener) {
    service.getResource(id, ActionListener.wrap(
        resource -> listener.onResponse(Boolean.TRUE),
        exception -> {
            if (exception instanceof ResourceNotFoundException) {
                listener.onResponse(Boolean.FALSE);
            } else {
                listener.onFailure(exception);
            }
        }
    ));
}
```

Similarly, for testing asynchronous code, avoid spawning threads and waiting with Thread.join(). Instead, use futures or test-friendly abstractions that allow controlling when callbacks are triggered.


[
  {
    "discussion_id": "2171945967",
    "pr_number": 130189,
    "pr_file": "server/src/internalClusterTest/java/org/elasticsearch/index/engine/MergeWithLowDiskSpaceIT.java",
    "created_at": "2025-06-27T12:32:35+00:00",
    "commented_code": "});\n    }\n\n    public void testForceMergeIsBlockedThenUnblocked() throws Exception {\n        String node = internalCluster().startNode();\n        ensureStableCluster(1);\n        setTotalSpace(node, Long.MAX_VALUE);\n        ThreadPoolMergeExecutorService threadPoolMergeExecutorService = internalCluster().getInstance(IndicesService.class, node)\n            .getThreadPoolMergeExecutorService();\n        TestTelemetryPlugin testTelemetryPlugin = getTelemetryPlugin(node);\n        // create some index\n        final String indexName = randomAlphaOfLength(10).toLowerCase(Locale.ROOT);\n        createIndex(\n            indexName,\n            Settings.builder().put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, 0).put(IndexMetadata.SETTING_NUMBER_OF_SHARDS, 1).build()\n        );\n        // get current disk space usage (for all indices on the node)\n        IndicesStatsResponse stats = indicesAdmin().prepareStats().clear().setStore(true).get();\n        long usedDiskSpaceAfterIndexing = stats.getTotal().getStore().sizeInBytes();\n        // restrict the total disk space such that the next merge does not have sufficient disk space\n        long insufficientTotalDiskSpace = usedDiskSpaceAfterIndexing + MERGE_DISK_HIGH_WATERMARK_BYTES - randomLongBetween(1L, 10L);\n        setTotalSpace(node, insufficientTotalDiskSpace);\n        // node stats' FS stats should report that there is insufficient disk space available\n        assertBusy(() -> {\n            NodesStatsResponse nodesStatsResponse = client().admin().cluster().prepareNodesStats().setFs(true).get();\n            assertThat(nodesStatsResponse.getNodes().size(), equalTo(1));\n            NodeStats nodeStats = nodesStatsResponse.getNodes().get(0);\n            assertThat(nodeStats.getFs().getTotal().getTotal().getBytes(), equalTo(insufficientTotalDiskSpace));\n            assertThat(nodeStats.getFs().getTotal().getAvailable().getBytes(), lessThan(MERGE_DISK_HIGH_WATERMARK_BYTES));\n        });\n        int indexingRounds = randomIntBetween(2, 5);\n        while (indexingRounds-- > 0) {\n            indexRandom(\n                true,\n                true,\n                true,\n                false,\n                IntStream.range(1, randomIntBetween(2, 5))\n                    .mapToObj(i -> prepareIndex(indexName).setSource(\"field\", randomAlphaOfLength(50)))\n                    .toList()\n            );\n        }\n        // start force merging (which is blocking) on a separate thread\n        Thread forceMergeThread = new Thread(",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2171945967",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130189,
        "pr_file": "server/src/internalClusterTest/java/org/elasticsearch/index/engine/MergeWithLowDiskSpaceIT.java",
        "discussion_id": "2171945967",
        "commented_code": "@@ -155,8 +170,125 @@ public void testShardCloseWhenDiskSpaceInsufficient() throws Exception {\n         });\n     }\n \n+    public void testForceMergeIsBlockedThenUnblocked() throws Exception {\n+        String node = internalCluster().startNode();\n+        ensureStableCluster(1);\n+        setTotalSpace(node, Long.MAX_VALUE);\n+        ThreadPoolMergeExecutorService threadPoolMergeExecutorService = internalCluster().getInstance(IndicesService.class, node)\n+            .getThreadPoolMergeExecutorService();\n+        TestTelemetryPlugin testTelemetryPlugin = getTelemetryPlugin(node);\n+        // create some index\n+        final String indexName = randomAlphaOfLength(10).toLowerCase(Locale.ROOT);\n+        createIndex(\n+            indexName,\n+            Settings.builder().put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, 0).put(IndexMetadata.SETTING_NUMBER_OF_SHARDS, 1).build()\n+        );\n+        // get current disk space usage (for all indices on the node)\n+        IndicesStatsResponse stats = indicesAdmin().prepareStats().clear().setStore(true).get();\n+        long usedDiskSpaceAfterIndexing = stats.getTotal().getStore().sizeInBytes();\n+        // restrict the total disk space such that the next merge does not have sufficient disk space\n+        long insufficientTotalDiskSpace = usedDiskSpaceAfterIndexing + MERGE_DISK_HIGH_WATERMARK_BYTES - randomLongBetween(1L, 10L);\n+        setTotalSpace(node, insufficientTotalDiskSpace);\n+        // node stats' FS stats should report that there is insufficient disk space available\n+        assertBusy(() -> {\n+            NodesStatsResponse nodesStatsResponse = client().admin().cluster().prepareNodesStats().setFs(true).get();\n+            assertThat(nodesStatsResponse.getNodes().size(), equalTo(1));\n+            NodeStats nodeStats = nodesStatsResponse.getNodes().get(0);\n+            assertThat(nodeStats.getFs().getTotal().getTotal().getBytes(), equalTo(insufficientTotalDiskSpace));\n+            assertThat(nodeStats.getFs().getTotal().getAvailable().getBytes(), lessThan(MERGE_DISK_HIGH_WATERMARK_BYTES));\n+        });\n+        int indexingRounds = randomIntBetween(2, 5);\n+        while (indexingRounds-- > 0) {\n+            indexRandom(\n+                true,\n+                true,\n+                true,\n+                false,\n+                IntStream.range(1, randomIntBetween(2, 5))\n+                    .mapToObj(i -> prepareIndex(indexName).setSource(\"field\", randomAlphaOfLength(50)))\n+                    .toList()\n+            );\n+        }\n+        // start force merging (which is blocking) on a separate thread\n+        Thread forceMergeThread = new Thread(",
        "comment_created_at": "2025-06-27T12:32:35+00:00",
        "comment_author": "henningandersen",
        "comment_body": "Could we avoid the `.get()` call and use `execute()` instead to avoid the thread? Assertions further down could then be about whether the future is done or not.",
        "pr_file_module": null
      },
      {
        "comment_id": "2173598204",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130189,
        "pr_file": "server/src/internalClusterTest/java/org/elasticsearch/index/engine/MergeWithLowDiskSpaceIT.java",
        "discussion_id": "2171945967",
        "commented_code": "@@ -155,8 +170,125 @@ public void testShardCloseWhenDiskSpaceInsufficient() throws Exception {\n         });\n     }\n \n+    public void testForceMergeIsBlockedThenUnblocked() throws Exception {\n+        String node = internalCluster().startNode();\n+        ensureStableCluster(1);\n+        setTotalSpace(node, Long.MAX_VALUE);\n+        ThreadPoolMergeExecutorService threadPoolMergeExecutorService = internalCluster().getInstance(IndicesService.class, node)\n+            .getThreadPoolMergeExecutorService();\n+        TestTelemetryPlugin testTelemetryPlugin = getTelemetryPlugin(node);\n+        // create some index\n+        final String indexName = randomAlphaOfLength(10).toLowerCase(Locale.ROOT);\n+        createIndex(\n+            indexName,\n+            Settings.builder().put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, 0).put(IndexMetadata.SETTING_NUMBER_OF_SHARDS, 1).build()\n+        );\n+        // get current disk space usage (for all indices on the node)\n+        IndicesStatsResponse stats = indicesAdmin().prepareStats().clear().setStore(true).get();\n+        long usedDiskSpaceAfterIndexing = stats.getTotal().getStore().sizeInBytes();\n+        // restrict the total disk space such that the next merge does not have sufficient disk space\n+        long insufficientTotalDiskSpace = usedDiskSpaceAfterIndexing + MERGE_DISK_HIGH_WATERMARK_BYTES - randomLongBetween(1L, 10L);\n+        setTotalSpace(node, insufficientTotalDiskSpace);\n+        // node stats' FS stats should report that there is insufficient disk space available\n+        assertBusy(() -> {\n+            NodesStatsResponse nodesStatsResponse = client().admin().cluster().prepareNodesStats().setFs(true).get();\n+            assertThat(nodesStatsResponse.getNodes().size(), equalTo(1));\n+            NodeStats nodeStats = nodesStatsResponse.getNodes().get(0);\n+            assertThat(nodeStats.getFs().getTotal().getTotal().getBytes(), equalTo(insufficientTotalDiskSpace));\n+            assertThat(nodeStats.getFs().getTotal().getAvailable().getBytes(), lessThan(MERGE_DISK_HIGH_WATERMARK_BYTES));\n+        });\n+        int indexingRounds = randomIntBetween(2, 5);\n+        while (indexingRounds-- > 0) {\n+            indexRandom(\n+                true,\n+                true,\n+                true,\n+                false,\n+                IntStream.range(1, randomIntBetween(2, 5))\n+                    .mapToObj(i -> prepareIndex(indexName).setSource(\"field\", randomAlphaOfLength(50)))\n+                    .toList()\n+            );\n+        }\n+        // start force merging (which is blocking) on a separate thread\n+        Thread forceMergeThread = new Thread(",
        "comment_created_at": "2025-06-29T04:59:23+00:00",
        "comment_author": "albertzaharovits",
        "comment_body": "Of course, thanks for the suggestion! (I've handled it as part of https://github.com/elastic/elasticsearch/pull/130189/commits/3452dcea85c813a38e83bdbc17af67b610e38bfd)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2171949919",
    "pr_number": 130189,
    "pr_file": "server/src/internalClusterTest/java/org/elasticsearch/index/engine/MergeWithLowDiskSpaceIT.java",
    "created_at": "2025-06-27T12:33:57+00:00",
    "commented_code": "});\n    }\n\n    public void testForceMergeIsBlockedThenUnblocked() throws Exception {\n        String node = internalCluster().startNode();\n        ensureStableCluster(1);\n        setTotalSpace(node, Long.MAX_VALUE);\n        ThreadPoolMergeExecutorService threadPoolMergeExecutorService = internalCluster().getInstance(IndicesService.class, node)\n            .getThreadPoolMergeExecutorService();\n        TestTelemetryPlugin testTelemetryPlugin = getTelemetryPlugin(node);\n        // create some index\n        final String indexName = randomAlphaOfLength(10).toLowerCase(Locale.ROOT);\n        createIndex(\n            indexName,\n            Settings.builder().put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, 0).put(IndexMetadata.SETTING_NUMBER_OF_SHARDS, 1).build()\n        );\n        // get current disk space usage (for all indices on the node)\n        IndicesStatsResponse stats = indicesAdmin().prepareStats().clear().setStore(true).get();\n        long usedDiskSpaceAfterIndexing = stats.getTotal().getStore().sizeInBytes();\n        // restrict the total disk space such that the next merge does not have sufficient disk space\n        long insufficientTotalDiskSpace = usedDiskSpaceAfterIndexing + MERGE_DISK_HIGH_WATERMARK_BYTES - randomLongBetween(1L, 10L);\n        setTotalSpace(node, insufficientTotalDiskSpace);\n        // node stats' FS stats should report that there is insufficient disk space available\n        assertBusy(() -> {\n            NodesStatsResponse nodesStatsResponse = client().admin().cluster().prepareNodesStats().setFs(true).get();\n            assertThat(nodesStatsResponse.getNodes().size(), equalTo(1));\n            NodeStats nodeStats = nodesStatsResponse.getNodes().get(0);\n            assertThat(nodeStats.getFs().getTotal().getTotal().getBytes(), equalTo(insufficientTotalDiskSpace));\n            assertThat(nodeStats.getFs().getTotal().getAvailable().getBytes(), lessThan(MERGE_DISK_HIGH_WATERMARK_BYTES));\n        });\n        int indexingRounds = randomIntBetween(2, 5);\n        while (indexingRounds-- > 0) {\n            indexRandom(\n                true,\n                true,\n                true,\n                false,\n                IntStream.range(1, randomIntBetween(2, 5))\n                    .mapToObj(i -> prepareIndex(indexName).setSource(\"field\", randomAlphaOfLength(50)))\n                    .toList()\n            );\n        }\n        // start force merging (which is blocking) on a separate thread\n        Thread forceMergeThread = new Thread(\n            // the max segments argument makes it a blocking call\n            () -> assertNoFailures(indicesAdmin().prepareForceMerge(indexName).setMaxNumSegments(1).get())\n        );\n        forceMergeThread.start();\n        assertBusy(() -> {\n            // merge executor says merging is blocked due to insufficient disk space while there is a single merge task enqueued\n            assertThat(threadPoolMergeExecutorService.getMergeTasksQueueLength(), equalTo(1));\n            assertTrue(threadPoolMergeExecutorService.isMergingBlockedDueToInsufficientDiskSpace());\n            // telemetry says that there are indeed some segments enqueued to be merged\n            testTelemetryPlugin.collect();\n            assertThat(\n                testTelemetryPlugin.getLongGaugeMeasurement(MergeMetrics.MERGE_SEGMENTS_QUEUED_USAGE).getLast().getLong(),\n                greaterThan(0L)\n            );\n            // but still no merges are currently running\n            assertThat(\n                testTelemetryPlugin.getLongGaugeMeasurement(MergeMetrics.MERGE_SEGMENTS_RUNNING_USAGE).getLast().getLong(),\n                equalTo(0L)\n            );\n            // indices stats also says that no merge is currently running (blocked merges are NOT considered as \"running\")\n            IndicesStatsResponse indicesStatsResponse = client().admin().indices().prepareStats(indexName).setMerge(true).get();\n            long currentMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getCurrent();\n            assertThat(currentMergeCount, equalTo(0L));\n        });\n        // the force merge call is still blocked\n        assertTrue(forceMergeThread.isAlive());\n        // merge executor still confirms merging is blocked due to insufficient disk space\n        assertTrue(threadPoolMergeExecutorService.isMergingBlockedDueToInsufficientDiskSpace());\n        // make disk space available in order to unblock the merge\n        if (randomBoolean()) {\n            setTotalSpace(node, Long.MAX_VALUE);\n        } else {\n            updateClusterSettings(\n                Settings.builder().put(ThreadPoolMergeExecutorService.INDICES_MERGE_DISK_HIGH_WATERMARK_SETTING.getKey(), \"0b\")\n            );\n        }\n        // assert that all the merges are now done and that the force-merge call returns\n        assertBusy(() -> {\n            IndicesStatsResponse indicesStatsResponse = client().admin().indices().prepareStats(indexName).setMerge(true).get();\n            long currentMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getCurrent();\n            // NO merging is in progress\n            assertThat(currentMergeCount, equalTo(0L));\n            long totalMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getTotal();\n            assertThat(totalMergeCount, greaterThan(0L));\n            // force merge call returned\n            assertFalse(forceMergeThread.isAlive());",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "2171949919",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130189,
        "pr_file": "server/src/internalClusterTest/java/org/elasticsearch/index/engine/MergeWithLowDiskSpaceIT.java",
        "discussion_id": "2171949919",
        "commented_code": "@@ -155,8 +170,125 @@ public void testShardCloseWhenDiskSpaceInsufficient() throws Exception {\n         });\n     }\n \n+    public void testForceMergeIsBlockedThenUnblocked() throws Exception {\n+        String node = internalCluster().startNode();\n+        ensureStableCluster(1);\n+        setTotalSpace(node, Long.MAX_VALUE);\n+        ThreadPoolMergeExecutorService threadPoolMergeExecutorService = internalCluster().getInstance(IndicesService.class, node)\n+            .getThreadPoolMergeExecutorService();\n+        TestTelemetryPlugin testTelemetryPlugin = getTelemetryPlugin(node);\n+        // create some index\n+        final String indexName = randomAlphaOfLength(10).toLowerCase(Locale.ROOT);\n+        createIndex(\n+            indexName,\n+            Settings.builder().put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, 0).put(IndexMetadata.SETTING_NUMBER_OF_SHARDS, 1).build()\n+        );\n+        // get current disk space usage (for all indices on the node)\n+        IndicesStatsResponse stats = indicesAdmin().prepareStats().clear().setStore(true).get();\n+        long usedDiskSpaceAfterIndexing = stats.getTotal().getStore().sizeInBytes();\n+        // restrict the total disk space such that the next merge does not have sufficient disk space\n+        long insufficientTotalDiskSpace = usedDiskSpaceAfterIndexing + MERGE_DISK_HIGH_WATERMARK_BYTES - randomLongBetween(1L, 10L);\n+        setTotalSpace(node, insufficientTotalDiskSpace);\n+        // node stats' FS stats should report that there is insufficient disk space available\n+        assertBusy(() -> {\n+            NodesStatsResponse nodesStatsResponse = client().admin().cluster().prepareNodesStats().setFs(true).get();\n+            assertThat(nodesStatsResponse.getNodes().size(), equalTo(1));\n+            NodeStats nodeStats = nodesStatsResponse.getNodes().get(0);\n+            assertThat(nodeStats.getFs().getTotal().getTotal().getBytes(), equalTo(insufficientTotalDiskSpace));\n+            assertThat(nodeStats.getFs().getTotal().getAvailable().getBytes(), lessThan(MERGE_DISK_HIGH_WATERMARK_BYTES));\n+        });\n+        int indexingRounds = randomIntBetween(2, 5);\n+        while (indexingRounds-- > 0) {\n+            indexRandom(\n+                true,\n+                true,\n+                true,\n+                false,\n+                IntStream.range(1, randomIntBetween(2, 5))\n+                    .mapToObj(i -> prepareIndex(indexName).setSource(\"field\", randomAlphaOfLength(50)))\n+                    .toList()\n+            );\n+        }\n+        // start force merging (which is blocking) on a separate thread\n+        Thread forceMergeThread = new Thread(\n+            // the max segments argument makes it a blocking call\n+            () -> assertNoFailures(indicesAdmin().prepareForceMerge(indexName).setMaxNumSegments(1).get())\n+        );\n+        forceMergeThread.start();\n+        assertBusy(() -> {\n+            // merge executor says merging is blocked due to insufficient disk space while there is a single merge task enqueued\n+            assertThat(threadPoolMergeExecutorService.getMergeTasksQueueLength(), equalTo(1));\n+            assertTrue(threadPoolMergeExecutorService.isMergingBlockedDueToInsufficientDiskSpace());\n+            // telemetry says that there are indeed some segments enqueued to be merged\n+            testTelemetryPlugin.collect();\n+            assertThat(\n+                testTelemetryPlugin.getLongGaugeMeasurement(MergeMetrics.MERGE_SEGMENTS_QUEUED_USAGE).getLast().getLong(),\n+                greaterThan(0L)\n+            );\n+            // but still no merges are currently running\n+            assertThat(\n+                testTelemetryPlugin.getLongGaugeMeasurement(MergeMetrics.MERGE_SEGMENTS_RUNNING_USAGE).getLast().getLong(),\n+                equalTo(0L)\n+            );\n+            // indices stats also says that no merge is currently running (blocked merges are NOT considered as \"running\")\n+            IndicesStatsResponse indicesStatsResponse = client().admin().indices().prepareStats(indexName).setMerge(true).get();\n+            long currentMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getCurrent();\n+            assertThat(currentMergeCount, equalTo(0L));\n+        });\n+        // the force merge call is still blocked\n+        assertTrue(forceMergeThread.isAlive());\n+        // merge executor still confirms merging is blocked due to insufficient disk space\n+        assertTrue(threadPoolMergeExecutorService.isMergingBlockedDueToInsufficientDiskSpace());\n+        // make disk space available in order to unblock the merge\n+        if (randomBoolean()) {\n+            setTotalSpace(node, Long.MAX_VALUE);\n+        } else {\n+            updateClusterSettings(\n+                Settings.builder().put(ThreadPoolMergeExecutorService.INDICES_MERGE_DISK_HIGH_WATERMARK_SETTING.getKey(), \"0b\")\n+            );\n+        }\n+        // assert that all the merges are now done and that the force-merge call returns\n+        assertBusy(() -> {\n+            IndicesStatsResponse indicesStatsResponse = client().admin().indices().prepareStats(indexName).setMerge(true).get();\n+            long currentMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getCurrent();\n+            // NO merging is in progress\n+            assertThat(currentMergeCount, equalTo(0L));\n+            long totalMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getTotal();\n+            assertThat(totalMergeCount, greaterThan(0L));\n+            // force merge call returned\n+            assertFalse(forceMergeThread.isAlive());",
        "comment_created_at": "2025-06-27T12:33:57+00:00",
        "comment_author": "henningandersen",
        "comment_body": "Could we instead wait for the force merge to complete first? If we go for a future, we can use `future.get()` here (or safeGet). If not, we can use `forcemergeThread.join`. That way I think we can avoid the `assertBusy`, since all the things here should hopefully be up to date.",
        "pr_file_module": null
      },
      {
        "comment_id": "2173598419",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 130189,
        "pr_file": "server/src/internalClusterTest/java/org/elasticsearch/index/engine/MergeWithLowDiskSpaceIT.java",
        "discussion_id": "2171949919",
        "commented_code": "@@ -155,8 +170,125 @@ public void testShardCloseWhenDiskSpaceInsufficient() throws Exception {\n         });\n     }\n \n+    public void testForceMergeIsBlockedThenUnblocked() throws Exception {\n+        String node = internalCluster().startNode();\n+        ensureStableCluster(1);\n+        setTotalSpace(node, Long.MAX_VALUE);\n+        ThreadPoolMergeExecutorService threadPoolMergeExecutorService = internalCluster().getInstance(IndicesService.class, node)\n+            .getThreadPoolMergeExecutorService();\n+        TestTelemetryPlugin testTelemetryPlugin = getTelemetryPlugin(node);\n+        // create some index\n+        final String indexName = randomAlphaOfLength(10).toLowerCase(Locale.ROOT);\n+        createIndex(\n+            indexName,\n+            Settings.builder().put(IndexMetadata.SETTING_NUMBER_OF_REPLICAS, 0).put(IndexMetadata.SETTING_NUMBER_OF_SHARDS, 1).build()\n+        );\n+        // get current disk space usage (for all indices on the node)\n+        IndicesStatsResponse stats = indicesAdmin().prepareStats().clear().setStore(true).get();\n+        long usedDiskSpaceAfterIndexing = stats.getTotal().getStore().sizeInBytes();\n+        // restrict the total disk space such that the next merge does not have sufficient disk space\n+        long insufficientTotalDiskSpace = usedDiskSpaceAfterIndexing + MERGE_DISK_HIGH_WATERMARK_BYTES - randomLongBetween(1L, 10L);\n+        setTotalSpace(node, insufficientTotalDiskSpace);\n+        // node stats' FS stats should report that there is insufficient disk space available\n+        assertBusy(() -> {\n+            NodesStatsResponse nodesStatsResponse = client().admin().cluster().prepareNodesStats().setFs(true).get();\n+            assertThat(nodesStatsResponse.getNodes().size(), equalTo(1));\n+            NodeStats nodeStats = nodesStatsResponse.getNodes().get(0);\n+            assertThat(nodeStats.getFs().getTotal().getTotal().getBytes(), equalTo(insufficientTotalDiskSpace));\n+            assertThat(nodeStats.getFs().getTotal().getAvailable().getBytes(), lessThan(MERGE_DISK_HIGH_WATERMARK_BYTES));\n+        });\n+        int indexingRounds = randomIntBetween(2, 5);\n+        while (indexingRounds-- > 0) {\n+            indexRandom(\n+                true,\n+                true,\n+                true,\n+                false,\n+                IntStream.range(1, randomIntBetween(2, 5))\n+                    .mapToObj(i -> prepareIndex(indexName).setSource(\"field\", randomAlphaOfLength(50)))\n+                    .toList()\n+            );\n+        }\n+        // start force merging (which is blocking) on a separate thread\n+        Thread forceMergeThread = new Thread(\n+            // the max segments argument makes it a blocking call\n+            () -> assertNoFailures(indicesAdmin().prepareForceMerge(indexName).setMaxNumSegments(1).get())\n+        );\n+        forceMergeThread.start();\n+        assertBusy(() -> {\n+            // merge executor says merging is blocked due to insufficient disk space while there is a single merge task enqueued\n+            assertThat(threadPoolMergeExecutorService.getMergeTasksQueueLength(), equalTo(1));\n+            assertTrue(threadPoolMergeExecutorService.isMergingBlockedDueToInsufficientDiskSpace());\n+            // telemetry says that there are indeed some segments enqueued to be merged\n+            testTelemetryPlugin.collect();\n+            assertThat(\n+                testTelemetryPlugin.getLongGaugeMeasurement(MergeMetrics.MERGE_SEGMENTS_QUEUED_USAGE).getLast().getLong(),\n+                greaterThan(0L)\n+            );\n+            // but still no merges are currently running\n+            assertThat(\n+                testTelemetryPlugin.getLongGaugeMeasurement(MergeMetrics.MERGE_SEGMENTS_RUNNING_USAGE).getLast().getLong(),\n+                equalTo(0L)\n+            );\n+            // indices stats also says that no merge is currently running (blocked merges are NOT considered as \"running\")\n+            IndicesStatsResponse indicesStatsResponse = client().admin().indices().prepareStats(indexName).setMerge(true).get();\n+            long currentMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getCurrent();\n+            assertThat(currentMergeCount, equalTo(0L));\n+        });\n+        // the force merge call is still blocked\n+        assertTrue(forceMergeThread.isAlive());\n+        // merge executor still confirms merging is blocked due to insufficient disk space\n+        assertTrue(threadPoolMergeExecutorService.isMergingBlockedDueToInsufficientDiskSpace());\n+        // make disk space available in order to unblock the merge\n+        if (randomBoolean()) {\n+            setTotalSpace(node, Long.MAX_VALUE);\n+        } else {\n+            updateClusterSettings(\n+                Settings.builder().put(ThreadPoolMergeExecutorService.INDICES_MERGE_DISK_HIGH_WATERMARK_SETTING.getKey(), \"0b\")\n+            );\n+        }\n+        // assert that all the merges are now done and that the force-merge call returns\n+        assertBusy(() -> {\n+            IndicesStatsResponse indicesStatsResponse = client().admin().indices().prepareStats(indexName).setMerge(true).get();\n+            long currentMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getCurrent();\n+            // NO merging is in progress\n+            assertThat(currentMergeCount, equalTo(0L));\n+            long totalMergeCount = indicesStatsResponse.getIndices().get(indexName).getPrimaries().merge.getTotal();\n+            assertThat(totalMergeCount, greaterThan(0L));\n+            // force merge call returned\n+            assertFalse(forceMergeThread.isAlive());",
        "comment_created_at": "2025-06-29T05:00:58+00:00",
        "comment_author": "albertzaharovits",
        "comment_body": "Great suggestion too, thanks! (also handled as part of https://github.com/elastic/elasticsearch/pull/130189/commits/3452dcea85c813a38e83bdbc17af67b610e38bfd)",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1559824642",
    "pr_number": 107188,
    "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
    "created_at": "2024-04-10T17:19:05+00:00",
    "commented_code": "}\n    }\n\n    protected boolean modelExists(String modelId) {",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1559824642",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 107188,
        "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
        "discussion_id": "1559824642",
        "commented_code": "@@ -228,6 +244,39 @@ private void deleteModel(DeleteTrainedModelAction.Request request, ClusterState\n         }\n     }\n \n+    protected boolean modelExists(String modelId) {",
        "comment_created_at": "2024-04-10T17:19:05+00:00",
        "comment_author": "davidkyle",
        "comment_body": "You can avoid the countdown latch and hence blocking the calling thread by using a listener. \r\n\r\nYou don't have to timeout the call to `trainedModelProvider.getTrainedModel()` if it does timeout simply out let the error propagate from the call. \r\n\r\n```\r\n    private void modelExists(String modelId, ActionListener<Boolean> listener) {\r\n        trainedModelProvider.getTrainedModel(modelId, GetTrainedModelsAction.Includes.empty(), null,\r\n            ActionListener.wrap(\r\n                model -> listener.onResponse(Boolean.TRUE),\r\n                exception -> {\r\n                    if (ExceptionsHelper.unwrapCause(exception) instanceof ResourceNotFoundException) {\r\n                        listener.onResponse(Boolean.FALSE);\r\n                    } else {\r\n                        listener.onFailure(exception);\r\n                    }\r\n                }\r\n            )\r\n        );\r\n    }\r\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "1561275004",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 107188,
        "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
        "discussion_id": "1559824642",
        "commented_code": "@@ -228,6 +244,39 @@ private void deleteModel(DeleteTrainedModelAction.Request request, ClusterState\n         }\n     }\n \n+    protected boolean modelExists(String modelId) {",
        "comment_created_at": "2024-04-11T16:04:54+00:00",
        "comment_author": "davidkyle",
        "comment_body": "After you make the `modelExists()` function async with a listener you will need to chain the various processing steps together. The best way to do this is use a [SubscribableListener](https://github.com/elastic/elasticsearch/blob/main/server/src/main/java/org/elasticsearch/action/support/SubscribableListener.java) \r\n\r\nHere's an example if it being used:\r\nhttps://github.com/elastic/elasticsearch/blob/main/x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportGetTrainedModelsStatsAction.java#L128",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1559831450",
    "pr_number": 107188,
    "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
    "created_at": "2024-04-10T17:25:50+00:00",
    "commented_code": "}\n    }\n\n    protected boolean modelExists(String modelId) {\n        CountDownLatch latch = new CountDownLatch(1);\n        final AtomicBoolean modelExists = new AtomicBoolean(false);\n\n        ActionListener<TrainedModelConfig> trainedModelListener = new ActionListener<>() {\n            @Override\n            public void onResponse(TrainedModelConfig config) {\n                modelExists.set(true);\n                latch.countDown();\n            }\n\n            @Override\n            public void onFailure(Exception e) {\n                logger.error(\"Failed to retrieve model {}: {}\", modelId, e.getMessage(), e);\n                latch.countDown();\n            }\n        };\n\n        trainedModelProvider.getTrainedModel(modelId, GetTrainedModelsAction.Includes.empty(), null, trainedModelListener);\n\n        try {\n            boolean latchReached = latch.await(5, TimeUnit.SECONDS);\n\n            if (latchReached == false) {\n                throw new ElasticsearchException(\"Timeout while waiting for trained model to be retrieved\");\n            }\n        } catch (InterruptedException e) {\n            throw new ElasticsearchException(\"Unexpected exception\", e);",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1559831450",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 107188,
        "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
        "discussion_id": "1559831450",
        "commented_code": "@@ -228,6 +244,39 @@ private void deleteModel(DeleteTrainedModelAction.Request request, ClusterState\n         }\n     }\n \n+    protected boolean modelExists(String modelId) {\n+        CountDownLatch latch = new CountDownLatch(1);\n+        final AtomicBoolean modelExists = new AtomicBoolean(false);\n+\n+        ActionListener<TrainedModelConfig> trainedModelListener = new ActionListener<>() {\n+            @Override\n+            public void onResponse(TrainedModelConfig config) {\n+                modelExists.set(true);\n+                latch.countDown();\n+            }\n+\n+            @Override\n+            public void onFailure(Exception e) {\n+                logger.error(\"Failed to retrieve model {}: {}\", modelId, e.getMessage(), e);\n+                latch.countDown();\n+            }\n+        };\n+\n+        trainedModelProvider.getTrainedModel(modelId, GetTrainedModelsAction.Includes.empty(), null, trainedModelListener);\n+\n+        try {\n+            boolean latchReached = latch.await(5, TimeUnit.SECONDS);\n+\n+            if (latchReached == false) {\n+                throw new ElasticsearchException(\"Timeout while waiting for trained model to be retrieved\");\n+            }\n+        } catch (InterruptedException e) {\n+            throw new ElasticsearchException(\"Unexpected exception\", e);",
        "comment_created_at": "2024-04-10T17:25:50+00:00",
        "comment_author": "davidkyle",
        "comment_body": "This code is not necessary if you take my suggestion but in Java it's best practice in to reset the interrupt flag with `Thread.currentThread().interrupt();`",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1559910187",
    "pr_number": 107188,
    "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
    "created_at": "2024-04-10T18:42:46+00:00",
    "commented_code": "}\n    }\n\n    protected boolean modelExists(String modelId) {\n        CountDownLatch latch = new CountDownLatch(1);\n        final AtomicBoolean modelExists = new AtomicBoolean(false);\n\n        ActionListener<TrainedModelConfig> trainedModelListener = new ActionListener<>() {\n            @Override\n            public void onResponse(TrainedModelConfig config) {\n                modelExists.set(true);\n                latch.countDown();\n            }\n\n            @Override\n            public void onFailure(Exception e) {\n                logger.error(\"Failed to retrieve model {}: {}\", modelId, e.getMessage(), e);\n                latch.countDown();\n            }\n        };\n\n        trainedModelProvider.getTrainedModel(modelId, GetTrainedModelsAction.Includes.empty(), null, trainedModelListener);",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1559910187",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 107188,
        "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
        "discussion_id": "1559910187",
        "commented_code": "@@ -228,6 +244,39 @@ private void deleteModel(DeleteTrainedModelAction.Request request, ClusterState\n         }\n     }\n \n+    protected boolean modelExists(String modelId) {\n+        CountDownLatch latch = new CountDownLatch(1);\n+        final AtomicBoolean modelExists = new AtomicBoolean(false);\n+\n+        ActionListener<TrainedModelConfig> trainedModelListener = new ActionListener<>() {\n+            @Override\n+            public void onResponse(TrainedModelConfig config) {\n+                modelExists.set(true);\n+                latch.countDown();\n+            }\n+\n+            @Override\n+            public void onFailure(Exception e) {\n+                logger.error(\"Failed to retrieve model {}: {}\", modelId, e.getMessage(), e);\n+                latch.countDown();\n+            }\n+        };\n+\n+        trainedModelProvider.getTrainedModel(modelId, GetTrainedModelsAction.Includes.empty(), null, trainedModelListener);",
        "comment_created_at": "2024-04-10T18:42:46+00:00",
        "comment_author": "maxhniebergall",
        "comment_body": "If we don't pass a parent task to this request, it wont be cancelable. I think it would be better to pass in the task from the masterOperation here. ",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "1559919796",
    "pr_number": 107188,
    "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
    "created_at": "2024-04-10T18:52:49+00:00",
    "commented_code": "}\n    }\n\n    protected boolean modelExists(String modelId) {\n        CountDownLatch latch = new CountDownLatch(1);\n        final AtomicBoolean modelExists = new AtomicBoolean(false);",
    "repo_full_name": "elastic/elasticsearch",
    "discussion_comments": [
      {
        "comment_id": "1559919796",
        "repo_full_name": "elastic/elasticsearch",
        "pr_number": 107188,
        "pr_file": "x-pack/plugin/ml/src/main/java/org/elasticsearch/xpack/ml/action/TransportDeleteTrainedModelAction.java",
        "discussion_id": "1559919796",
        "commented_code": "@@ -228,6 +244,39 @@ private void deleteModel(DeleteTrainedModelAction.Request request, ClusterState\n         }\n     }\n \n+    protected boolean modelExists(String modelId) {\n+        CountDownLatch latch = new CountDownLatch(1);\n+        final AtomicBoolean modelExists = new AtomicBoolean(false);\n+",
        "comment_created_at": "2024-04-10T18:52:49+00:00",
        "comment_author": "maxhniebergall",
        "comment_body": "To avoid using a latch and requiring a timeout, I think we could replace this function with an actionListener. What do you think? ",
        "pr_file_module": null
      }
    ]
  }
]
