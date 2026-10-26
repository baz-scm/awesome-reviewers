---
title: Behavior-Accurate CLI Docs
description: 'When documenting CLI commands and outputs, ensure the docs exactly match
  the implemented parsing and machine-consumable contracts.


  Apply these rules:'
repository: cline/cline#v29
label: Documentation
language: Other
comments_count: 3
repository_stars: 70893
---

When documenting CLI commands and outputs, ensure the docs exactly match the implemented parsing and machine-consumable contracts.

Apply these rules:
- Verify argument/flag ordering: if a subcommand forwards “everything after X” to a connector/provider, examples must place flags before X so they reach the CLI.
- Match real semantics: document what actually happens (interactive vs non-interactive, ordering of results like `--limit`, etc.). Don’t describe missing/ignored options—either fix behavior or remove the claim.
- Make JSON output docs parse-focused: state the line format (e.g., one JSON object per line), required fields (e.g., `type`, `ts`), and document only the event/object types that scripts should handle; omit or clarify status lines that consumers need not act on.

Example (flag placement):
```bash
# Good: options before channel/argument so the CLI can interpret them
cline connect telegram --restart -k <BOT-TOKEN>

# Bad (common pitfall): flags after channel may be forwarded to the connector
cline connect telegram --restart -k <BOT-TOKEN>
```

Example (JSON schema scope):
- Document the per-line contract (`type`, `ts`, and payload shape for relevant `type`s).
- Add guidance like: “Skip types you don’t parse,” and only list types that scripts are expected to handle.