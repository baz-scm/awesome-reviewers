---
title: Wrap threaded code properly
description: When working with threads in Rails applications, always wrap application
  code with `Rails.application.executor.wrap` to ensure thread safety and proper state
  management. Code running outside these wrappers can cause race conditions, memory
  leaks, and inconsistent application state.
repository: rails/rails
label: Concurrency
language: Markdown
comments_count: 3
repository_stars: 57027
---

When working with threads in Rails applications, always wrap application code with `Rails.application.executor.wrap` to ensure thread safety and proper state management. Code running outside these wrappers can cause race conditions, memory leaks, and inconsistent application state.

```ruby
# INCORRECT - application code outside wrapper
Thread.new do
  user = User.find(params[:id])  # Unsafe!
  Rails.application.executor.wrap do
    # Some wrapped code
  end
end

# CORRECT - all application code inside wrapper
Thread.new do
  # No application code here
  Rails.application.executor.wrap do
    user = User.find(params[:id])
    # All application code goes here
  end
end
```

This applies to all scenarios where you manually create threads, including when using thread pools from libraries like Concurrent Ruby. The Rails executor ensures that your thread has proper access to autoloading, manages database connections correctly, and handles thread-local data appropriately.

For long-running operations that may be interrupted (like during deployments), also consider implementing checkpoints to preserve progress:

```ruby
Rails.application.executor.wrap do
  records.find_each do |record|
    record.process
    # Create checkpoints regularly for interruptible work
    checkpoint! if should_checkpoint?
  end
end
```
