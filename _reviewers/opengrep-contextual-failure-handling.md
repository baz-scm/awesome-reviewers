---
title: contextual failure handling
description: Implement intelligent failure handling that makes contextual decisions
  about retry, cleanup, and error propagation based on the type and likelihood of
  recovery from specific failures.
repository: opengrep/opengrep
label: Error Handling
language: Shell
comments_count: 3
repository_stars: 1546
---

Implement intelligent failure handling that makes contextual decisions about retry, cleanup, and error propagation based on the type and likelihood of recovery from specific failures.

Consider these key principles:
- **Analyze failure context**: Use HTTP response codes and error types to determine if retry is appropriate (e.g., retry on rate limits/timeouts, but fail fast on 404s for missing resources)
- **Implement bounded retries**: Avoid infinite retry loops that could cause thundering herd problems during outages
- **Clean up on failure**: Remove partial state or broken installations when operations fail to prevent corrupted system state
- **Use strict error handling**: Enable proper error propagation with mechanisms like `set -euo pipefail` in bash scripts

Example implementation:
```bash
#!/usr/bin/env bash
set -euo pipefail

retry_with_context() {
    local url="$1"
    local temp_file="$2"
    local max_attempts=3
    
    for attempt in $(seq 1 $max_attempts); do
        if curl --fail --location "$url" > "$temp_file"; then
            return 0
        fi
        
        # Get HTTP code to decide if retry makes sense
        http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
        case $http_code in
            404|403) 
                echo "Resource not found (HTTP $http_code), not retrying"
                return 1
                ;;
            429|5*) 
                echo "Temporary failure (HTTP $http_code), retrying in 2s..."
                sleep 2
                ;;
        esac
    done
    
    # Cleanup on final failure
    rm -f "$temp_file"
    return 1
}
```

This approach balances user experience with system reliability by making informed decisions about when failures are recoverable versus when they indicate fundamental problems that shouldn't be retried.