---
title: Least privilege networking
description: Restrict network access to only what's necessary for your application
  to function, using explicit allowlisting rather than trying to block malicious traffic.
  Network traffic should be denied by default and only specifically required destinations
  should be allowed.
repository: anthropics/claude-code
label: Security
language: Shell
comments_count: 1
repository_stars: 25432
---

Restrict network access to only what's necessary for your application to function, using explicit allowlisting rather than trying to block malicious traffic. Network traffic should be denied by default and only specifically required destinations should be allowed.

When implementing network restrictions:
1. Start with a default deny policy for all traffic
2. Explicitly allowlist only necessary domains and IP ranges
3. Use fallback mechanisms for critical security controls
4. Verify your restrictions work as expected

For example, when configuring container firewalls:
```bash
# Create default deny policy
iptables -P OUTPUT DROP

# Create allowlist for domains
ipset create allowed-domains hash:net

# Add only necessary domains
for domain in "api.required-service.com" "cdn.dependencies.org"; do
    ips=$(dig +short A "$domain")
    for ip in $ips; do
        ipset add allowed-domains "$ip"
    done
done

# Allow only traffic to allowlisted destinations
iptables -A OUTPUT -m set --match-set allowed-domains dst -j ACCEPT

# Test the configuration works as expected
if curl --connect-timeout 5 https://blocked-domain.com >/dev/null 2>&1; then
    echo "ERROR: Firewall verification failed"
fi
```

Remember that network restrictions should be combined with other security controls (defense in depth). As shown in the discussion about S3 access, network allowlisting can be paired with credential restrictions to provide multiple layers of security.