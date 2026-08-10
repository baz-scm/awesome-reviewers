---
title: Normalize host IPs
description: When performing security checks on hosts/IPs (e.g., blocking private/loopback
  access), don’t rely on brittle string equality. Normalize `URL.hostname` first,
  because IPv6 literals are often returned in bracket form (e.g., `"[::1]"`, `"[::]"`),
  causing dead-code comparisons like `hostname === "::1"`.
repository: supermemoryai/supermemory
label: Security
language: TypeScript
comments_count: 1
repository_stars: 28844
---

When performing security checks on hosts/IPs (e.g., blocking private/loopback access), don’t rely on brittle string equality. Normalize `URL.hostname` first, because IPv6 literals are often returned in bracket form (e.g., `"[::1]"`, `"[::]"`), causing dead-code comparisons like `hostname === "::1"`.

Apply:
- Strip IPv6 brackets before comparing.
- Prefer parsing to an IP address and using tested range checks for: loopback/unspecified, private/link-local, and IPv4-mapped IPv6.

Example:
```ts
function normalizeHost(hostname: string) {
  // If URL.hostname is an IPv6 literal, it may be bracketed: "[::1]"
  return hostname.replace(/^\[|\]$/g, "");
}

function isPrivateHost(hostname: string): boolean {
  const h = normalizeHost(hostname.toLowerCase());

  // Safe exact matches (after normalization)
  if (h === 'localhost' || h === '127.0.0.1' || h === '0.0.0.0' || h === '::1' || h === '::') {
    return true;
  }

  // Prefer a real IP parser + CIDR/range checks for:
  // - fc00::/7 (ULA)
  // - fe80::/10 (link-local)
  // - IPv4-mapped IPv6 like ::ffff:169.254.x.x
  return false;
}
```