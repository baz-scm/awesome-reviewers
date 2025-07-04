---
title: Isolate concurrent resources
description: Create separate instances of non-thread-safe resources for each thread
  or process in concurrent applications rather than sharing a single instance. Many
  objects that maintain state or shared metadata (like sessions, connections, or context-dependent
  resources) are not thread-safe and can cause race conditions or unpredictable behavior
  when accessed...
repository: boto/boto3
label: Concurrency
language: Other
comments_count: 4
repository_stars: 9417
---

Create separate instances of non-thread-safe resources for each thread or process in concurrent applications rather than sharing a single instance. Many objects that maintain state or shared metadata (like sessions, connections, or context-dependent resources) are not thread-safe and can cause race conditions or unpredictable behavior when accessed concurrently.

For example, when using a library with both thread-safe and non-thread-safe components:

```python
import threading
import boto3.session

class MyTask(threading.Thread):
    def run(self):
        # Create a new session per thread
        session = boto3.session.Session()
        
        # Create resource using thread's session
        s3 = session.resource('s3')
        
        # Put your thread-safe code here
        # ...

# Create and start multiple threads
threads = [MyTask() for _ in range(5)]
for thread in threads:
    thread.start()
```

For thread-safe components (like certain clients), you may create them once and share across threads, but be aware of limitations:
1. Check documentation to confirm thread safety guarantees
2. Be cautious with any metadata attributes which may not be thread-safe to modify
3. Avoid sharing any objects across processes even if they're thread-safe
4. Consider potential performance impacts of excessive object creation