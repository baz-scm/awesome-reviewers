---
title: optimize network configurations
description: Optimize network configurations by eliminating redundancy, using modern
  compression standards, and properly configuring load balancing. This includes setting
  sensible defaults to avoid duplicative parameters, leveraging efficient compression
  algorithms like zstd alongside gzip for better data transfer, and implementing proper
  load balancing with health...
repository: mastodon/mastodon
label: Networking
language: Other
comments_count: 3
repository_stars: 48691
---

Optimize network configurations by eliminating redundancy, using modern compression standards, and properly configuring load balancing. This includes setting sensible defaults to avoid duplicative parameters, leveraging efficient compression algorithms like zstd alongside gzip for better data transfer, and implementing proper load balancing with health checks for high-availability services.

Examples:
- Set crossorigin defaults to avoid repetitive `crossorigin: 'anonymous'` parameters
- Use `encode zstd gzip` for better compression (zstd supported by 70% of users)
- Configure load balancing with health checks:
```
handle /api/v1/streaming* {
    reverse_proxy localhost:4000 localhost:4001 {
        lb_policy least_conn
        health_uri /api/v1/streaming/health
    }
}
```

This approach reduces configuration bloat, improves network performance, and ensures reliable service delivery.