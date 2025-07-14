---
title: Thread-safe resource management patterns
description: 'Ensure thread-safe access to shared resources while following proper
  resource management patterns. When implementing concurrent operations:


  1. Prefer worker threads over process spawning for parallel tasks'
repository: nodejs/node
label: Concurrency
language: Other
comments_count: 5
repository_stars: 112178
---

Ensure thread-safe access to shared resources while following proper resource management patterns. When implementing concurrent operations:

1. Prefer worker threads over process spawning for parallel tasks
2. Use instance-based implementations instead of static instances for thread-safe access
3. Implement proper resource management using smart pointers and RAII patterns
4. Carefully manage object ownership across thread boundaries

Example of proper thread-safe resource management:

```cpp
// Instead of static instance
class NetworkResourceManager {
 private:
  std::mutex mutex_;
  std::unordered_map<std::string, std::shared_ptr<Resource>> resources_;
 
 public:
  void Put(const std::string& url, std::unique_ptr<Resource> data) {
    std::lock_guard<std::mutex> lock(mutex_);
    resources_[url] = std::move(data);
  }
  
  // For parallel processing
  void ProcessResource(const std::string& url) {
    auto worker = std::make_unique<WorkerThread>([this, url]() {
      // Thread-safe resource access
      std::lock_guard<std::mutex> lock(mutex_);
      if (auto it = resources_.find(url); it != resources_.end()) {
        it->second->process();
      }
    });
    worker->start();
  }
};
```

This pattern ensures:
- Thread-safe access to shared resources
- Proper resource cleanup through RAII
- Efficient parallel processing using worker threads
- Clear ownership semantics using smart pointers