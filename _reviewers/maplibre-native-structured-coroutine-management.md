---
title: Structured coroutine management
description: Always bind coroutine scopes to appropriate lifecycles and follow consistent
  patterns for asynchronous operations. Prefer suspending functions over class-based
  approaches when possible, and ensure proper job cancellation to prevent memory leaks.
repository: maplibre/maplibre-native
label: Concurrency
language: Kotlin
comments_count: 4
repository_stars: 1411
---

Always bind coroutine scopes to appropriate lifecycles and follow consistent patterns for asynchronous operations. Prefer suspending functions over class-based approaches when possible, and ensure proper job cancellation to prevent memory leaks.

For internal Kotlin code without Java interoperability requirements:
```kotlin
// Preferred: suspending function approach
suspend fun requestLocalUrl(url: String): ByteArray? = withContext(Dispatchers.IO) {
    loadFile(...)
}

// Instead of class-based approach with callback
class RequestTask(private val scope: CoroutineScope, private val onCompletion: ((ByteArray?) -> Unit)?) {
    fun execute(url: String) {
        scope.launch(Dispatchers.IO) { ... }
    }
}
```

When a class-based approach is necessary:
1. Document the intended lifecycle of the coroutine scope
2. Implement proper cancellation mechanism
3. Tie the scope to an appropriate lifecycle object
4. Consider returning the Job from launch operations for granular control

```kotlin
class AsyncOperation(lifecycleOwner: LifecycleOwner) {
    // Scope tied to lifecycle
    private val scope = lifecycleOwner.lifecycleScope
    
    fun execute(): Job = scope.launch(Dispatchers.IO) {
        // Work here
    }
    
    // Or with SupervisorJob for managing multiple concurrent tasks
    private val job = SupervisorJob()
    private val scope = CoroutineScope(Dispatchers.IO + job)
    
    fun cancel() {
        job.cancel() // Cancels all child jobs
    }
}
```

For any asynchronous work, maintain consistency by using coroutines with appropriate dispatchers rather than raw threads.