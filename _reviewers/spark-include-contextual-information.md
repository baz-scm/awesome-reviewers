---
title: Include contextual information
description: Log messages should include comprehensive contextual information to support
  debugging and system monitoring. This includes relevant identifiers, operation details,
  and state information that help developers understand what happened and why.
repository: apache/spark
label: Logging
language: Other
comments_count: 5
repository_stars: 41554
---

Log messages should include comprehensive contextual information to support debugging and system monitoring. This includes relevant identifiers, operation details, and state information that help developers understand what happened and why.

Key practices:
- Include relevant IDs (task ID, provider ID, query run ID, etc.)
- Explain the purpose or context of operations, especially for non-obvious cases like "version + 1" representing the current operating version
- Add quantitative information when available (e.g., "how many were closed and how many were readded")
- Use structured formatting with field names for clarity: `StateStoreProviderId[ storeId=$storeId, queryRunId=$queryRunId ]`
- Provide context for temporary or placeholder states to avoid confusion

Example of good contextual logging:
```scala
logInfo(log"Task thread trigger maintenance to close provider " +
  log"${MDC(TASK_ID, taskId)} for ${MDC(STATE_STORE_PROVIDER_ID, providerId)} " +
  log"- provider removed from loadedProviders")
```

Balance completeness with readability - include essential context but avoid excessive noise that makes logs harder to parse. Focus on information that would be valuable for debugging, monitoring, or understanding system behavior.