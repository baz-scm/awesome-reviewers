---
title: Secure-by-default integrations
description: When adding configurable external services/integrations (e.g., registries,
  MCP servers, plugins), apply security-by-default and supply-chain controls—especially
  when the integration can access credentials.
repository: awslabs/aidlc-workflows
label: Security
language: Json
comments_count: 1
repository_stars: 3849
---

When adding configurable external services/integrations (e.g., registries, MCP servers, plugins), apply security-by-default and supply-chain controls—especially when the integration can access credentials.

Apply:
- Default-off: Do not enable external/incoming server entries by default. Require an explicit opt-in (e.g., config flag, environment variable, or explicit allowlist).
- No mutable releases: Avoid using tags like `@latest` (or other non-deterministic references). Pin to an exact version (and ideally verify integrity/checksum).
- Credential awareness: If the integration can use local AWS/other credentials, make that behavior explicit and least-privilege; require explicit enablement/authorization.
- Document rationale: Record the security decision (why enabled, which credentials, which pinned versions) so future changes preserve the security posture.

Example (pattern):
```json
{
  "mcpServers": {
    "aws-mcp": {
      "enabled": false,
      "command": "uvx",
      "args": ["mcp-proxy-for-aws@1.2.3"],
      "notes": "Disabled by default; requires explicit opt-in due to credential usage."
    }
  }
}
```
If you need a registry to be enabled, document the exact reason, threat model, and pinned dependency versions—and ensure credentials are not implicitly accessible without explicit consent.