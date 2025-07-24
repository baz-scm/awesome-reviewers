---
title: Active service health checks
description: Replace static delays with active health checks in CI/CD workflows to
  ensure service readiness. Instead of using fixed sleep times, implement polling
  mechanisms that verify service health endpoints. This improves workflow reliability
  and reduces false negatives.
repository: appwrite/appwrite
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 51959
---

Replace static delays with active health checks in CI/CD workflows to ensure service readiness. Instead of using fixed sleep times, implement polling mechanisms that verify service health endpoints. This improves workflow reliability and reduces false negatives.

Example implementation:
```yaml
- name: Wait for service readiness
  run: |
    for i in {1..18}; do               # 18 × 5 s = 90 s timeout
      if curl -fs http://localhost/health >/dev/null; then
        break
      fi
      echo "🕒 Waiting for service to become healthy... ($i)"
      sleep 5
    done
    curl -fs http://localhost/health >/dev/null || {
      echo "❌ Service did not become healthy in time" >&2
      exit 1
    }
```

This approach:
- Actively verifies service availability
- Provides clear feedback during waiting period
- Fails fast if service is unhealthy
- Accommodates varying startup times
- Includes proper error handling