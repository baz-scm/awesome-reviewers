---
title: Use controlled concurrency patterns
description: Implement proper concurrency control mechanisms to prevent resource exhaustion
  and ensure thread-safe operations. Use sync.Once for thread-safe initialization
  to avoid memory leaks, and employ goroutine pools or semaphores to limit concurrent
  operations instead of spawning unlimited goroutines.
repository: volcano-sh/volcano
label: Concurrency
language: Go
comments_count: 2
repository_stars: 4899
---

Implement proper concurrency control mechanisms to prevent resource exhaustion and ensure thread-safe operations. Use sync.Once for thread-safe initialization to avoid memory leaks, and employ goroutine pools or semaphores to limit concurrent operations instead of spawning unlimited goroutines.

For initialization that should happen only once:
```go
var volumeBindingPlugin *vbcap.VolumeBinding
var once sync.Once

once.Do(func() {
    plugin, err := vbcap.New(context.TODO(), vbArgs.VolumeBindingArgs, handle, features)
    if err == nil {
        volumeBindingPlugin = plugin.(*vbcap.VolumeBinding)
    }
})
```

For controlled concurrent processing:
```go
// Use goroutine pool instead of unlimited goroutines
semaphore := make(chan struct{}, 16)
var wg sync.WaitGroup

for _, taskInfo := range job.TaskStatusIndex[status] {
    wg.Add(1)
    semaphore <- struct{}{} // Acquire semaphore
    go func(task *TaskInfo) {
        defer func() {
            <-semaphore // Release semaphore
            wg.Done()
        }()
        // Process task
    }(taskInfo)
}
wg.Wait()
```

This approach prevents memory leaks from repeated initialization, avoids overwhelming the system with too many concurrent operations, and ensures predictable resource usage patterns.