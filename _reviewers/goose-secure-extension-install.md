---
title: Secure extension install
description: 'When publishing extension/server install options (especially deep-links
  or Install buttons), default to a secure-by-default path: require explicit/manual
  installation for binary-first or otherwise security-sensitive extensions. Only enable
  an automated install/deeplink if the target is explicitly allowlisted.'
repository: aaif-goose/goose
label: Security
language: Json
comments_count: 1
repository_stars: 51876
---

When publishing extension/server install options (especially deep-links or Install buttons), default to a secure-by-default path: require explicit/manual installation for binary-first or otherwise security-sensitive extensions. Only enable an automated install/deeplink if the target is explicitly allowlisted.

Apply it like this:
- Disable the install button/deeplink for these entries (e.g., set `show_install_link` to `false`).
- Replace it with clear manual installation instructions.
- If an Install button is required, add/extend the deeplink allowlist in `deeplink.ts` with a narrow entry for the exact server/extension (no broad or dynamic matching).

Example (pattern):
```json
{
  "id": "nika",
  "name": "Nika",
  "description": "...",
  "command": "nika mcp",
  "show_install_link": false
}
```
Then document manual install, e.g.:
- `goose session --with-extension "nika mcp"`
- Settings → Extensions
