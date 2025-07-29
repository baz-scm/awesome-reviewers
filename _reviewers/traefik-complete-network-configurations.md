---
title: Complete network configurations
description: Network configuration examples and documentation should include all essential
  networking components such as ports, protocols, timeouts, and security considerations.
  Incomplete configurations can lead to connection failures, security vulnerabilities,
  or unexpected behavior.
repository: traefik/traefik
label: Networking
language: Markdown
comments_count: 17
repository_stars: 55772
---

Network configuration examples and documentation should include all essential networking components such as ports, protocols, timeouts, and security considerations. Incomplete configurations can lead to connection failures, security vulnerabilities, or unexpected behavior.

When documenting network configurations:

1. **Include all required ports**: Specify both HTTP and HTTPS ports when TLS is configured
2. **Specify protocols explicitly**: Clearly indicate TCP/UDP protocols and default behaviors  
3. **Provide complete timeout configurations**: Include relationship warnings between related timeouts
4. **Add security warnings**: Highlight security implications of configuration options
5. **Use accurate networking terminology**: Distinguish between connections and requests, especially for TCP

Example of complete network configuration:

```yaml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"  # Include HTTPS port when TLS is configured
    tls: {}

# For Tailscale configurations, specify directory requirements
entryPoints:
  tailscale:
    tsnet:
      dir: /var/lib/tailscale  # For multiple entrypoints, use different directories
      
# Include security warnings for path sanitization
http:
  entryPoints:
    web:
      sanitizePath: false  # Warning: Can lead to unsafe routing with base64 data containing "/"
```

This ensures users have complete, working configurations and understand the security implications of their networking choices.