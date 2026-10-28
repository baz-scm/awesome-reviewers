---
title: Fail closed on uncertainty
description: When an operation's outcome cannot be positively confirmed (a timeout
  waiting for an ack, an ambiguous terminal/host response, a runner that can't answer
  in time, a socket that may or may not have actually stopped), treat it as a failure
  rather than assuming success or falling back to pre-existing risky behavior. Never
  let a caller observe "success" for...
repository: ogulcancelik/herdr#canary966c66ad
label: Error Handling
language: Rust
comments_count: 11
repository_stars: 46332
---

When an operation's outcome cannot be positively confirmed (a timeout waiting for an ack, an ambiguous terminal/host response, a runner that can't answer in time, a socket that may or may not have actually stopped), treat it as a failure rather than assuming success or falling back to pre-existing risky behavior. Never let a caller observe "success" for work that did not verifiably complete: a `write()` that may have been silently truncated by the kernel must be refused up front instead of reported as delivered; a `session stop` command must not print `"stopped": true` unless the socket is actually confirmed down after the wait; a host capability probe that returns an unexpected status must be rejected rather than optimistically accepted. Complementing this, when a fallible operation has already produced side effects (a staged file, a spawned process, a registered task) and then fails, the error path must clean those side effects up before returning the error, so a failure never leaves orphaned state behind for later confusion. If two things fail together (e.g. the primary operation and its cleanup), keep the primary error as the surfaced cause and attach the secondary failure as context rather than letting the lower-priority error mask the real one.

Example pattern to follow:
```rust
let result = (|| {
    // ... attempt the operation, may create temp state ...
    verify_precondition()?;
    do_work()?;
    Ok(())
})();
if let Err(err) = &result {
    cleanup_any_partial_state(); // never leave partial state behind on error
}
result // only Ok() reaches the caller as success
```
Apply this standard whenever a function reports completion/success to a caller: confirm the condition that justifies "success" was actually observed, not merely assumed from the absence of an error or the passage of a timeout, and ensure any resources created along a now-failing path are released as part of handling that failure.