---
title: validate connection timeouts
description: Always validate network connection states and implement explicit timeout
  handling to prevent zombie connections and ensure robust network operations. Connection
  objects can appear valid while actually being disconnected, and network operations
  without timeouts can hang indefinitely.
repository: browser-use/browser-use
label: Networking
language: Python
comments_count: 2
repository_stars: 69139
---

Always validate network connection states and implement explicit timeout handling to prevent zombie connections and ensure robust network operations. Connection objects can appear valid while actually being disconnected, and network operations without timeouts can hang indefinitely.

When working with browser contexts or network connections, actively verify the connection state rather than assuming validity:

```python
# Validate browser connection state
if self.browser_context:
    try:
        _ = self.browser_context.pages
        if self.browser_context.browser and not self.browser_context.browser.is_connected():
            self.browser_context = None
    except Exception:
        self.browser_context = None
```

For network operations, always specify explicit timeouts with reasonable defaults:

```python
# Add timeout parameter to network operations
await page.goto(params.url, timeout=int((params.timeout or 30)*1000))
```

This prevents hanging operations and provides predictable failure modes when network conditions are poor or connections are unstable.