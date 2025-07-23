---
title: Thread-safe message dispatching
description: When implementing communication between multiple threads, ensure that
  messages are correctly routed to their intended recipients. Avoid designs where
  all worker threads consume from a single shared queue when messages are intended
  for specific threads, as this creates race conditions where messages can be processed
  by the wrong thread.
repository: Aider-AI/aider
label: Concurrency
language: Python
comments_count: 2
repository_stars: 35856
---

When implementing communication between multiple threads, ensure that messages are correctly routed to their intended recipients. Avoid designs where all worker threads consume from a single shared queue when messages are intended for specific threads, as this creates race conditions where messages can be processed by the wrong thread.

Instead, consider one of these approaches:
1. Use separate queues for each recipient thread
2. Implement a central dispatcher that routes messages to the correct recipient
3. Use an event-based pattern with callbacks or futures

Example of problematic code:
```python
def _server_loop(self, server: McpServer, loop: asyncio.AbstractEventLoop) -> None:
    while True:
        # All threads compete for the same messages
        msg: CallArguments = self.message_queue.get()
        
        # If message not for this server, discard it
        if msg.server_name != server.name:
            self.message_queue.task_done()
            continue
            
        # Process the message...
```

Better implementation:
```python
class McpManager:
    def __init__(self):
        # One queue per server for proper message routing
        self.server_queues = {}  # server_name -> queue
        self.result_queue = queue.Queue()
        
    def add_server(self, server_name):
        self.server_queues[server_name] = queue.Queue()
        
    def _call(self, io, server_name, function, args={}):
        # Route message to specific server queue
        if server_name in self.server_queues:
            self.server_queues[server_name].put(CallArguments(server_name, function, args))
            result = self.result_queue.get()
            return result.response
        return None
        
    def _server_loop(self, server: McpServer, loop: asyncio.AbstractEventLoop) -> None:
        # Each server only processes its own messages
        server_queue = self.server_queues[server.name]
        while True:
            msg = server_queue.get()
            # Process message...
```

This pattern prevents race conditions and ensures messages are always processed by their intended recipients.