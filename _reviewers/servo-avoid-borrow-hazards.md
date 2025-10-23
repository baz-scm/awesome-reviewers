---
title: avoid borrow hazards
description: Prevent borrow conflicts by collecting or cloning data before operations
  that may trigger garbage collection, call into JavaScript, or create additional
  borrows. This is especially critical when holding mutable borrows (`borrow_mut()`)
  that could conflict with operations that need to access the same data.
repository: servo/servo
label: Concurrency
language: Rust
comments_count: 3
repository_stars: 32962
---

Prevent borrow conflicts by collecting or cloning data before operations that may trigger garbage collection, call into JavaScript, or create additional borrows. This is especially critical when holding mutable borrows (`borrow_mut()`) that could conflict with operations that need to access the same data.

The pattern involves identifying operations that might cause borrow conflicts and restructuring code to release borrows before those operations execute.

**Example of the problem:**
```rust
// BAD: borrow_mut is still active when calling jsval_to_webdriver (which can trigger GC)
fn WebdriverCallback(&self, cx: JSContext, val: HandleValue, realm: InRealm, can_gc: CanGc) {
    let rv = jsval_to_webdriver(cx, &self.globalscope, val, realm, can_gc);
    let opt_chan = self.webdriver_script_chan.borrow_mut().take();
    if let Some(chan) = opt_chan {
        let _ = chan.send(rv);
    }
}
```

**Corrected approach:**
```rust
// GOOD: Take the channel first, then call the potentially conflicting operation
fn WebdriverCallback(&self, cx: JSContext, value: HandleValue, realm: InRealm, can_gc: CanGc) {
    if let Some(chan) = self.webdriver_script_chan.borrow_mut().take() {
        let result = jsval_to_webdriver(cx, &self.globalscope, value, realm, can_gc);
        let _ = chan.send(result);
    }
}
```

**Another pattern - collecting before iteration:**
```rust
// GOOD: Collect vector before starting loop to avoid borrow hazards
pub(crate) fn fire_queued_messages(&self, can_gc: CanGc) {
    let messages: Vec<_> = self.queued_worker_tasks.borrow_mut().drain(..).collect();
    for msg in messages {
        // Process message with can_gc argument safely
    }
}
```

This pattern is essential in garbage-collected environments where operations can trigger collection cycles that conflict with active borrows.