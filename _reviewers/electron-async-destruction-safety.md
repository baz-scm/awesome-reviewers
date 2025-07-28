---
title: async destruction safety
description: When destroying objects asynchronously to avoid crashes from observer
  notifications or other synchronous destruction issues, ensure proper cleanup ordering
  and add defensive null checks to handle race conditions.
repository: electron/electron
label: Concurrency
language: Other
comments_count: 3
repository_stars: 117644
---

When destroying objects asynchronously to avoid crashes from observer notifications or other synchronous destruction issues, ensure proper cleanup ordering and add defensive null checks to handle race conditions.

Key practices:
1. **Move destruction to async context**: Use task runners to defer destruction when synchronous cleanup causes crashes due to active observers or notifications
2. **Reset pointers immediately**: After moving objects to async destruction, immediately set the original pointer to null to prevent use-after-move
3. **Add defensive null checks**: In methods that might be called during async destruction, add null checks before accessing potentially destroyed objects
4. **Explicit resource cleanup**: For resources requiring manual shutdown (like dbus::Bus), ensure cleanup methods are called before destruction

Example from the discussions:
```cpp
// Instead of synchronous destruction that crashes:
// managed_devtools_web_contents_.reset();

// Use async destruction:
embedder_message_dispatcher_.reset();
content::GetUIThreadTaskRunner({})->PostTask(
    FROM_HERE,
    base::BindOnce(
        [](std::unique_ptr<content::WebContents> web_contents) {},
        std::move(managed_devtools_web_contents_)));
managed_devtools_web_contents_ = nullptr;

// Add defensive checks in methods:
if (!GetDevToolsWebContents())
  return;
```

This pattern prevents crashes from premature destruction while maintaining system stability during async cleanup operations.