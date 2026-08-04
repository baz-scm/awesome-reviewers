---
title: Secure Auth and Secrets
description: 'Apply these rules whenever implementing auth, tokens, or security-modes:


  1) Never leak tokens/secrets

  - Don’t print full-privilege tokens to stdout, shell history, CI logs, or transcripts.'
repository: awslabs/mcp
label: Security
language: Markdown
comments_count: 4
repository_stars: 9545
---

Apply these rules whenever implementing auth, tokens, or security-modes:

1) Never leak tokens/secrets
- Don’t print full-privilege tokens to stdout, shell history, CI logs, or transcripts.
- Prefer storing tokens in a secrets store / agent memory with restricted access, and only reference them internally.

2) Never put credentials in URLs
- Avoid query-string auth like `...&u=USERNAME&p=PASSWORD` (or equivalent) because URLs are commonly logged by shells, proxies, and load balancers.
- Use header-based auth instead.

3) Apply authentication in the correct direction (inbound vs outbound)
- Inbound auth (protecting your MCP server) is not the same as outbound auth (calling an upstream API).
- For outbound calls, acquire the token as needed, then set `Authorization: Bearer <token>` on the HTTP client used for the upstream requests.

4) Enforce security mode via strict allowlists
- If the service is in read-only mode, accept only explicitly recognized read-only statements.
- Reject write-capable constructs even if nested (e.g., INSERT inside a CTE).

Example (header auth + no token echo):
```bash
TOKEN="..."
curl -sS "https://localhost:8181/api/v3/query_sql?db=DATABASE_NAME&q=SELECT+*+FROM+TABLE_NAME+LIMIT+10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"

# Do NOT: echo "$TOKEN" or pass it as a URL query parameter.
```

Example (read-only enforcement idea):
- Parse/normalize SQL, allow only: `SELECT`, `WITH` (CTEs that contain no write operations), `SHOW`, `DESCRIBE/DESC`, `EXPLAIN`, `ANALYZE`.
- If any disallowed verb/operation is detected inside the statement or within CTE bodies, reject the request.