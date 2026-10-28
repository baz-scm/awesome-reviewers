---
title: Graceful failure and cleanup
description: 'When an operation can fail partway through, avoid panics and avoid leaving
  the system in an inconsistent state. Convert fallible arithmetic or logic that could
  panic (e.g. clamp operations on unexpected/edge-case inputs like a zero-size work
  area) into recoverable errors: return a `Result`, log the failure, and let the caller
  degrade gracefully (e.g. still...'
repository: "cline/cline\r\n"
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70946
---

When an operation can fail partway through, avoid panics and avoid leaving the system in an inconsistent state. Convert fallible arithmetic or logic that could panic (e.g. clamp operations on unexpected/edge-case inputs like a zero-size work area) into recoverable errors: return a `Result`, log the failure, and let the caller degrade gracefully (e.g. still show the window with default bounds) instead of crashing the whole app. Likewise, if a multi-step setup fails partway (e.g. spawning a PTY succeeds but starting its reader thread fails), make sure any resources already acquired are torn down—kill the spawned process and remove its session entry—before propagating the error, so failures don't leak processes, handles, or stale state. Finally, if an underlying platform API cannot provide a reliable guarantee in all environments (e.g. overriding the Windows taskbar icon), don't ship a code path that silently "succeeds" but doesn't actually work for users; remove the unreliable path and scope the feature to the surface that can be reliably guaranteed. In short: prefer explicit, recoverable error returns over panics, always clean up partially-acquired resources on the failure path, and never leave users with a misleading appearance of success.