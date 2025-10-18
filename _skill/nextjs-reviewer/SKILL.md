---
name: nextjs-reviewer
description: "Guidelines for reviewing and improving code contributions in Next.js, focusing on stability (robust error handling) and performance (non-blocking telemetry)."
license: CC-BY-4.0
---

# Next.js Code Review Guidelines

## Observability and Performance
Next.js operations should not be blocked by observability tasks. For example, telemetry and status checks must run in the background so they don’t delay critical flows[1]. Use detached processes or asynchronous calls for logging and analytics during shutdown or restart procedures, rather than waiting synchronously[2]. Likewise, perform health checks via dedicated endpoints (e.g. `/__nextjs_server_status`) instead of calls that might be disrupted by the operations being observed[3]. This ensures telemetry data is collected without degrading the user experience, maintaining responsiveness even during critical lifecycle events[4].

## Robust Error Handling
Always implement explicit and thorough error handling in Next.js components to ensure stability[5]. Check for error conditions (such as API response errors) before proceeding with normal logic[6]. Use try/catch blocks around operations that may throw exceptions (API calls, data parsing, etc.) so you can handle failures gracefully and provide fallback UI or default behavior[5][6]. Avoid silently ignoring errors or relying on implicit error handling, as that can lead to unpredictable behavior and make debugging difficult[5]. By catching and handling errors (and displaying error information when appropriate), Next.js applications remain predictable and user-friendly even when something goes wrong[7].
