---
title: Fail-Closed Input Sanitization
description: All externally supplied values must be validated/escaped for the *exact*
  security-sensitive context they’re interpolated into, and security checks must be
  fail-closed (no bypass via fallbacks, parse differences, redirects, caches, or policy
  typos).
repository: awslabs/mcp
label: Security
language: Python
comments_count: 9
repository_stars: 9545
---

All externally supplied values must be validated/escaped for the *exact* security-sensitive context they’re interpolated into, and security checks must be fail-closed (no bypass via fallbacks, parse differences, redirects, caches, or policy typos).

Practical rules:
1) **URL/SSRF boundaries:** reject unsafe schemes/control characters/userinfo and avoid resolution behaviors that can dereference external references (e.g., OpenAPI `$ref`). Validate *before* any resolver/fetch and ensure prescan parsing can’t be skipped by parse/fallback quirks.
2) **Query/DSL interpolation:** if you build SQL/regex/Logs Insights strings, escape user-controlled fragments for that DSL (at minimum: backslash + double-quotes) or use strict allowlists.
3) **Fail-closed security checks:** on “can’t verify” or “security probe didn’t run”, block under enforce/default. Don’t allow exceptions to be silently swallowed, and don’t let connection-caching/key reconstruction bypass eviction.
4) **Bound untrusted work:** cap query result sizes and command lists to prevent DoS.
5) **Secrets hygiene:** never expose secrets as tool parameters or into the agent/LLM context; redact before returning.

Example (escape before building a Logs Insights filter):
```python
def _escape_insights_string(s: str) -> str:
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '').replace('\r', '')

# When interpolating into: ... field = "{value}"
value = _escape_insights_string(page_url)
query = f'... metadata.pageUrl = "{value}"'
```

Example (fail-closed privilege probe):
```python
try:
    rows = await db_connection.execute_query(POSTGRES_PRIVILEGE_QUERY)
except Exception as e:
    if policy == 'enforce':
        raise ConnectionValidationError('Rejecting connection (fail-closed)')
    # warn/off handling only after connectivity is proven as appropriate
```

Teams should add regression tests specifically for the bypass class (e.g., redirect/ref prescan fallback, cache eviction key mismatch, quote-breaking in DSL interpolation, and tool-schema secret leakage).