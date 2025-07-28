---
title: leverage framework cache mechanisms
description: When implementing caching functionality, prefer using framework-provided
  cache mechanisms over manual cache management. Frameworks typically offer optimized
  cache handling that includes automatic error propagation, efficient multi-level
  cache checking, and built-in performance optimizations that are difficult to replicate
  manually.
repository: facebook/react-native
label: Caching
language: Kotlin
comments_count: 3
repository_stars: 123178
---

When implementing caching functionality, prefer using framework-provided cache mechanisms over manual cache management. Frameworks typically offer optimized cache handling that includes automatic error propagation, efficient multi-level cache checking, and built-in performance optimizations that are difficult to replicate manually.

Manual cache checking often leads to inefficient implementations that duplicate work, miss optimization opportunities, and require custom error handling. Framework mechanisms handle these complexities automatically and provide better performance characteristics.

For example, instead of manually checking cache availability:

```kotlin
// Avoid: Manual cache checking
val imagePipeline = Fresco.getImagePipeline()
val dataSource = imagePipeline.isInDiskCache(uri)
dataSource.subscribe(object : BaseDataSubscriber<Boolean>() {
  override fun onNewResultImpl(dataSource: DataSource<Boolean>) {
    val isInCache: Boolean = dataSource.getResult() ?: false
    if (isInCache) {
      setupImageRequest(uri, cacheControl, postprocessor, resizeOptions)
    } else {
      // Custom error handling needed
    }
  }
})

// Prefer: Framework cache mechanism
val requestLevel = if (cacheControl == ImageCacheControl.ONLY_IF_CACHED) 
  RequestLevel.DISK_CACHE else RequestLevel.FULL_FETCH

val imageRequestBuilder = ImageRequestBuilder.newBuilderWithSource(uri)
  .setLowestPermittedRequestLevel(requestLevel)
```

This approach leverages the framework's comprehensive cache checking (bitmap, encoded memory, and disk caches), automatic error propagation, and avoids duplicate cache reads while ensuring optimal performance.