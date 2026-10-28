---
title: Graceful failure handling
description: Critical code paths (app setup, process spawning, platform integrations)
  must never panic or leave the system in an inconsistent state when inputs are unexpected
  or a dependency misbehaves. Before performing arithmetic or OS calls, validate edge
  cases (empty/zero-size regions, missing resources, unsupported platform behavior)
  and return a `Result`/error...
repository: 'cline/cline

  '
label: Error Handling
language: Rust
comments_count: 3
repository_stars: 70942
---

Critical code paths (app setup, process spawning, platform integrations) must never panic or leave the system in an inconsistent state when inputs are unexpected or a dependency misbehaves. Before performing arithmetic or OS calls, validate edge cases (empty/zero-size regions, missing resources, unsupported platform behavior) and return a `Result`/error instead of relying on invariants that may not hold at runtime. For example, clamping window bounds should reject or safely handle an empty or inverted work area rather than calling `.clamp(min, max)` with `min > max`, which panics; use a wider integer type if the domain can overflow, and add regression tests for boundary and extreme values. When an operation fails partway (e.g., a spawned process whose IPC reader thread fails to start), make sure any already-allocated resources are cleaned up (kill the child process, remove it from tracking state) before the error is propagated, so no process or state leaks on failure. If a code path is based on an environment capability that cannot be guaranteed across configurations (e.g., forcing a Windows taskbar icon via `WM_SETICON`), don't ship an unreliable "best effort" path—prefer removing it and clearly degrade to a supported, consistent alternative (e.g., the system tray icon) rather than leaving users with unpredictable behavior. In all cases, failures in setup or background logic should be logged and the application should continue in a degraded but functional state instead of crashing or silently corrupting state.